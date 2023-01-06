import logging

import psycopg2 as psycopg2


class GetPassword:

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.host_name = "mcdb.cdfzbrpdwpbo.ap-northeast-1.rds.amazonaws.com"
        self.user_name = "postgres"
        self.password = "Admin.123"

    # Python Connector database creator function
    def getconn(self):
        engine = psycopg2.connect(
            database="postgres",
            user=self.user_name,
            password=self.password,
            host=self.host_name,
            port='5432'
        )
        logging.info("connected to DB!")
        return engine

    def execute(self):
        conn = self.getconn()
        conn.autocommit = True
        cursor = conn.cursor()

        sql = f"select hash_key from movie_collection_profile inner join auth_user on auth_user.id = user_id where auth_user.username='{self.name}';"

        cursor.execute(sql)
        result = cursor.fetchall()

        conn.close()
        if len(result) > 0:
            return result[0][0]


