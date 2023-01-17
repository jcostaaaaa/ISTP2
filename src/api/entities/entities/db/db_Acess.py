import psycopg2



def connection():
        connection = psycopg2.connect(user="is",
                                      password="is",
                                      host="db-rel",
                                      database="is")
        return connection

