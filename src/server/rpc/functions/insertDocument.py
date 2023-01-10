import psycopg2
from lxml import etree

def xml_validator(xml_path: str, xsd_path: str) -> bool:
    xml_doc = etree.parse(xml_path)
    xmlschema_doc = etree.parse(xsd_path)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    result = xmlschema.validate(xml_doc)
    return result


def insertDocument(xml_name, xml_file, xsd_file):

    if xml_validator(xml_file, xsd_file):

        try:
            connection = psycopg2.connect(user="is",
                                          password="is",
                                          host="localhost",
                                          port="5434",
                                          database="is")

            file = etree.parse(xml_file)
            x = etree.tostring(file, encoding="utf-8", method="xml").decode()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO imported_documents (file_name,xml) VALUES(%s,%s)", (xml_name, x))
            connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
