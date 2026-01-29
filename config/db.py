import psycopg2

def get_db_connection(config: dict):
    db_config = config["database"]
    conn = psycopg2.connect(**db_config)
    conn.autocommit = False
    return conn