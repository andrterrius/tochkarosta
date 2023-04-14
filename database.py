import time

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
                elif how == "update":
                    result = conn.commit()
                else:
                    result = cursor.fetchone()
                self.pool.putconn(conn)
                return result
    def get_news(self, limit, offset=0):
        return self.execute("SELECT id, header, text, images, date, cardinality(views) as views FROM news ORDER BY id DESC LIMIT %s OFFSET %s", (limit, offset), "all")

    def get_events(self, limit, offset=0):
        return self.execute("SELECT id, header, text, images, date, cardinality(views) as views FROM events ORDER BY id DESC LIMIT %s OFFSET %s", (limit, offset), "all")

    def get_images(self, limit, offset=0):
        sql = self.execute("SELECT images FROM news ORDER BY id DESC LIMIT %s OFFSET %s", (limit, offset), "all")
        if sql:
            images = []
            for imags in sql:
                for image in imags[0]:
                    images.append(image)
            return images

    def add_views_news(self, ip, limit, offset=0):
        return self.execute("UPDATE news SET views = array_append(views, %s) WHERE id IN(SELECT id FROM news ORDER BY id DESC LIMIT %s OFFSET %s) and %s != ALL(views)", (ip, limit, offset, ip), "update")

    def add_views_events(self, ip, limit, offset=0):
        return self.execute("UPDATE events SET views = array_append(views, %s) WHERE id IN(SELECT id FROM events ORDER BY id DESC LIMIT %s OFFSET %s) and %s != ALL(views)", (ip, limit, offset, ip), "update")

    def get_count_news_pages(self):
        sql = self.execute("SELECT count(*) FROM news")
        return sql['count'] // 9 if sql['count'] % 9 == 0 else (sql['count'] // 9) + 1

    def get_count_events_pages(self):
        sql = self.execute("SELECT count(*) FROM events")
        return sql['count'] // 9 if sql['count'] % 9 == 0 else (sql['count'] // 9) + 1

    def get_info_new(self, id):
        return self.execute("SELECT * FROM news WHERE id = %s", (id,))

    def get_info_event(self, id):
        return self.execute("SELECT * FROM events WHERE id = %s", (id,))
