import psycopg2
from lxml import etree
connection = None
cursor = None


try:
     connection= psycopg2.connect(user="is",
                                  password="is",
                                  host="db-xml",
                                  database="is")

     file =etree.parse('../data/output.xml')
     x= etree.tostring(file,encoding="utf-8",method="xml").decode()
     cursor = connection.cursor()
     cursor.execute("INSERT INTO imported_documents (file_name,xml) VALUES(%s,%s)",("output",x))
     connection.commit()



except (Exception, psycopg2.Error) as error:
    print("Failed to fetch data", error)

finally:
    if connection:
        cursor.close()
        connection.close()
