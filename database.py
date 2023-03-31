import time

import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.pool import SimpleConnectionPool
class DB:
    def __init__(self, dns):
        self.pool = SimpleConnectionPool(10, 100, dns, cursor_factory=DictCursor)
    def execute(self, sql, args=None, how="one"):
        with self.pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, args)
                if how == "all":
                    result = cursor.fetchall()
                else:
                    result = cursor.fetchone()
                self.pool.putconn(conn)
                return result
    def get_news(self, limit, offset=0):
        start = time.time()
        f = self.execute("SELECT * FROM news ORDER BY id DESC LIMIT %s OFFSET %s", (limit, offset), "all")
        print(time.time()-start)
        return f

    def get_info_new(self, id):
        start = time.time()
        f = self.execute("SELECT * FROM news WHERE id = %s", (id,))
        print(time.time()-start)
        return f

    def get_count_news(self):
        start = time.time()
        f = self.execute("SELECT count(*) FROM news")
        count = (f['count'] // 10) + 1
        print(time.time()-start)
        return count