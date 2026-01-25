from models.subscriber import subscriber
import psycopg2
from psycopg2 import sql

conn = psycopg2.connect(
    database='subscriber',
    user='postgres',
    password='postgres',
    host='127.0.0.1',
    port='5432'
)
conn.autocommit = False

class SubRepository:
    def __init__(self):
        self.subs = {}

    # methods
    def get_all_subs(self):
        with conn.cursor() as cur:
            cur.execute("""
            SELECT subname, subenabled, subpublications, subconninfo, subslotname
            FROM pg_subscription
        """)
            subs = cur.fetchall()

            cur.execute("SELECT subname, state FROM pg_stat_subscription")
            stats = cur.fetchall()

        stat_map = {}
        for subname, worker_type, pid, received_lsn, latest_end_lsn in stats:
            stat_map.setdefault(subname, []).append({
                "worker_type": worker_type,
                "pid": pid,
                "received_lsn": str(received_lsn) if received_lsn is not None else None,
                "latest_end_lsn": str(latest_end_lsn) if latest_end_lsn is not None else None,
            })

        return [
            {
                "subname": subname,
                "enabled": enabled,
                "publications": publications,
                "conninfo": conninfo,
                "slot_name": slot_name,
                "running": subname in stat_map,         # simple “state”
                "workers": stat_map.get(subname, [])    # detailed info
            }
            for (subname, enabled, publications, conninfo, slot_name) in subs
        ]



