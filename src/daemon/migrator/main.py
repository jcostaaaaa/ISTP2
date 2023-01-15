import sys
import time

import psycopg2
from psycopg2 import OperationalError

POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 60


def print_psycopg2_exception(ex):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print("\npsycopg2 ERROR:", ex, "on line number:", line_num)
    print("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print("\nextensions.Diagnostics:", ex.diag)

    # print the pgcode and pgerror exceptions
    print("pgerror:", ex.pgerror)
    print("pgcode:", ex.pgcode, "\n")


if __name__ == "__main__":

    db_org = psycopg2.connect(host='db-xml', database='is', user='is', password='is')
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')

    while True:

        # Connect to both databases
        db_org = None
        db_dst = None

        try:
            db_org = psycopg2.connect(host='db-xml', database='is', user='is', password='is')
            db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
        except OperationalError as err:
            print_psycopg2_exception(err)

        if db_dst is None or db_org is None:
            continue

        print("Checking updates...")
        # !TODO: 1- Execute a SELECT query to check for any changes on the table
        cursorCheckDataBase = db_org.cursor()
        cursorCheckDataBase.execute("select count(*) from imported_documents where is_imported=false")
        count = cursorCheckDataBase.fetchone()

        if count[0] > 0:
            print("We have new imported files in the database!!")
        else:
            print("We already imported all the files to the database")

        # !TODO: 2- Execute a SELECT queries with xpath to retrieve the data we want to store in the relational db

        cursorSelectImportedDocuments = db_org.cursor()
        cursorSelectImportedDocuments.execute("select id from imported_documents where is_imported= false ")
        idsImportedDocuments = cursorSelectImportedDocuments.fetchall();
        for id in idsImportedDocuments:
            cursorOrigem= db_org.cursor()
            cursorOrigem.execute(
                "select unnest(xpath('DataSetResults/competitions/competition/@name',xml)):: text as Competition from imported_documents where id= %s",
                (id,))
            competitions = cursorOrigem.fetchall()
            cursorOrigem.close()

            # !TODO: 3- Execute INSERT queries in the destination db
            cursorDestino = db_dst.cursor()
            for competition in competitions:
                cursorDestino.execute("INSERT INTO competition (name) VALUES (%s)", (competition,))
            cursor2 = db_org.cursor()

            # !TODO: 4- Make sure we store somehow in the origin database that certain records were already migrated.
            #          Change the db structure if needed.
            cursor2.execute("UPDATE imported_documents set is_imported=true where id=%s", (id,))
            db_org.commit()
            cursorDestino.close()
        db_dst.commit()


        time.sleep(POLLING_FREQ)
