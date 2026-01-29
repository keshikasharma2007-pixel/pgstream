from psycopg2.errorcodes import UNDEFINED_OBJECT

from models.publication import publication
import psycopg2

from psycopg2 import sql
import logging

class PubRepository:
    def __init__(self, conn, logger: logging.Logger):
        self.pubs = {}
        self.conn = conn
        self.logger = logger

    # methods

    def get_all_pubs(self):
        with self.conn.cursor() as cur:
            cur.execute("select * from pg_publication")
            rows = cur.fetchall()
            # return dictionaries
            return [
                {
                    "pubname" : row[1],
                    "pubowner" : row[2],
                    "puballtables" : row[3],
                    "pubinsert" : row[4],
                    "pubupdate" : row[5],
                    "pubdelete" : row[6],
                    "pubtruncate" : row[7],
                    "pubviaroot" : row[8],
                    "pubgencols" : row[9]
                }
                for row in rows
            ]

    def get_pub_name(self, pubname):
        with self.conn.cursor() as cur:
            cur.execute("select * from pg_publication where pubname=%s", (pubname,))
            row = cur.fetchone()
            return {
                "pubname" : row[1],
                "pubowner" : row[2],
                "puballtables" : row[3],
                "pubinsert" : row[4],
                "pubupdate" : row[5],
                "pubdelete" : row[6],
                "pubtruncate" : row[7],
                "pubviaroot" : row[8],
                "pubgencols" : row[9]
            } if row else None

    def delete_pub_name(self, pubname):
            # must use RETURNING to detect deletion, else deleted will always be None
        try:
            with self.conn.cursor as cur:
                cur.execute(
                    sql.SQL("DROP PUBLICATION {};").format(sql.Identifier(pubname))
                )
            self.conn.commit()
            return True

        except psycopg2.errors.UndefinedObject:
            self.conn.rollback()
            return False

        except Exception:
            self.conn.rollback()
            raise


    def create_new_pub(self, pubname, table):

        if self.get_pub_name(pubname):
            self.conn.rollback()
            return False
        self.conn.rollback()
        with self.conn.cursor() as cur:
            cur.execute(
                (sql.SQL("create publication {} for table {};")
                .format(
                    sql.Identifier(pubname),
                    sql.Identifier(table)
                )
                )
            )
        self.conn.commit()
        return True

    def update_one_pub(self, pubname, publish_ops):
        if not self.get_pub_name(pubname):
            self.conn.rollback()
            return False

        publish_str = ", ".join(op.lower().strip() for op in publish_ops)


        with self.conn.cursor() as cur:
            cur.execute(
                sql.SQL("ALTER PUBLICATION {} SET (publish = %s);")
                .format(sql.Identifier(pubname)),
                (publish_str,)
            )
        self.conn.commit()
        return True