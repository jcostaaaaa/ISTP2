import asyncio
import time
import uuid

import os

import psycopg2
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

from utils.to_xml_converter import converter

CSV_INPUT_PATH = "/csv"
XML_OUTPUT_PATH = "/shared/output"



def get_csv_files_in_input_folder():
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(CSV_INPUT_PATH) for f in filenames if
            os.path.splitext(f)[1] == '.csv']

def generate_unique_file_name(directory):
    return f"{directory}/{str(uuid.uuid4())}.xml"

def convert_csv_to_xml(in_path, out_path):
     converter(in_path, out_path)
 

class CSVHandler(FileSystemEventHandler):
    def __init__(self, input_path, output_path):
        self._output_path = output_path
        self._input_path = input_path
        self.db_conn = psycopg2.connect(host="db-xml",database="is",user="is",password="is")

        # generate file creation events for existing files
        for file in [os.path.join(dp, f) for dp, dn, filenames in os.walk(input_path) for f in filenames]:
            event = FileCreatedEvent(os.path.join(CSV_INPUT_PATH, file))
            event.event_type = "created"
            self.dispatch(event)

    async def convert_csv(self, csv_path):
        # here we avoid converting the same file again
        # !TODO: check converted files in the database
        if csv_path in await self.get_converted_files():
            return

        else:
            print(f"We will import the following files : '{csv_path}'")
            #print(f"We already import the following files:"+ self.db_conn)


        # we generate a unique file name for the XML file
        xml_path = generate_unique_file_name(self._output_path)

        # we do the conversion

        convert_csv_to_xml(csv_path, xml_path)
        print(f"new xml file generated: '{xml_path}'")

        # !TODO: once the conversion is done, we should updated the converted_documents tables
        file = open(xml_path,"r")
        new_xml = file.read()
        # !TODO: we should store the XML document into the imported_documents table
        xml = os.path.basename(xml_path)
        cursor = self.db_conn.cursor()
        cursor.execute("INSERT INTO imported_documents (file_name,xml) VALUES (%s,%s)",(xml,new_xml))
        self.db_conn.commit();
        cursor.close()

        # !TODO: once the conversion is done, we should updated the converted_documents tables
        file_size = os.stat(csv_path).st_size
        cursor= self.db_conn.cursor()
        cursor.execute("INSERT INTO converted_documents(src,file_size,dst) VALUES (%s,%s,%s)", (csv_path,file_size,xml_path))
        self.db_conn.commit()
        cursor.close()
    async def get_converted_files(self):
        #
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT src from converted_documents")
        converted_files = cursor.fetchall()
        cursor.close()

        return [file[0] for file in converted_files]

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".csv"):
            asyncio.run(self.convert_csv(event.src_path))


if __name__ == "__main__":

    CSV_INPUT_PATH = "/csv"
    XML_OUTPUT_PATH = "/shared/output"

    # create the file observer
    observer = Observer()
    observer.schedule(
        CSVHandler(CSV_INPUT_PATH, XML_OUTPUT_PATH),
        path=CSV_INPUT_PATH,
        recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
