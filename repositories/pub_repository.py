from models.publication import publication
import psycopg2
from psycopg2 import sql
import json

# connection - need to put this in config file

with open("config.josn", "r") as f:
    config = json.load(f)

db_config = config["database"]

conn = psycopg2.connect(**config["database"])
conn.autocommit = False


class PubRepository:
    def __init__(self):
        self.pubs = {}

    # methods
    def get_all_pubs(self):
        with conn.cursor() as cur:
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
        with conn.cursor() as cur:
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
        with conn.cursor() as cur:
            # must use RETURNING to detect deletion, else deleted will always be None
            cur.execute("drop publication %s", (pubname,))
            deleted = cur.fetchone()
            if not deleted:
                conn.rollback()
                return False

        conn.commit()
        return True

    def create_new_pub(self, pubname, table):

        if self.get_pub_name(pubname):
            conn.rollback()
            return False
        conn.rollback()
        with conn.cursor() as cur:
            cur.execute(
                (sql.SQL("create publication {} for table {};")
                    .format(
                        sql.Identifier(pubname),
                        sql.Identifier(table)
                    )
                )
            )
        conn.commit()
        return True

    def update_one_pub(self, pubname, publish_ops):
        if not self.get_pub_name(pubname):
            conn.rollback()
            return False

        publish_str = ", ".join(op.lower().strip() for op in publish_ops)


        with conn.cursor() as cur:
            cur.execute(
                sql.SQL("ALTER PUBLICATION {} SET (publish = %s);")
                .format(sql.Identifier(pubname)),
                (publish_str,)
            )
        conn.commit()
        return True