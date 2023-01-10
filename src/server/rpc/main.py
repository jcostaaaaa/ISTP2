# import signal, sys
# from xmlrpc.server import SimpleXMLRPCServer
# from xmlrpc.server import SimpleXMLRPCRequestHandler
#
# from functions.string_length import string_length
# from functions.string_reverse import string_reverse
#
# PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000
#
# if __name__ == "__main__":
#     class RequestHandler(SimpleXMLRPCRequestHandler):
#         rpc_paths = ('/RPC2',)
#
#     with SimpleXMLRPCServer(('localhost', PORT), requestHandler=RequestHandler) as server:
#         server.register_introspection_functions()
#
#         def signal_handler(signum, frame):
#             print("received signal")
#             server.server_close()
#
#             # perform clean up, etc. here...
#             print("exiting, gracefully")
#             sys.exit(0)
#
#         # signals
#         signal.signal(signal.SIGTERM, signal_handler)
#         signal.signal(signal.SIGHUP, signal_handler)
#         signal.signal(signal.SIGINT, signal_handler)
#
#         # register both functions
#         server.register_function(string_reverse)
#         server.register_function(string_length)
#
#         # start the server
#         print(f"Starting the RPC Server in port {PORT}...")
#         server.serve_forever()
import signal, sys
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

#Querys
from functions.listarTodasCompetiçoes import listarTodasCompetiçoes
from functions.procurarJogosMaisGolos import procurarJogosMaisGolos
from functions.gamesByCompetition import gamesByCompetition
from functions.drawByCompetition import drawByCompetition
from functions.top10JogoscomGolos import top10JogoscomGolos
from functions.gameResult import gameResult
from functions.jogosPortugal import jogosPortugal
from functions.pesquisaEquipa import pesquisaEquipa


#Functions

from functions.deleteQuery import delete
from functions.insertDocument import insertDocument
from functions.validator import xml_validator
from functions.validator import validate
from functions.convert import converter
from functions.convert import format_data



class RequestHandler(SimpleXMLRPCRequestHandler):
   rpc_paths = ('/RPC2',)

with SimpleXMLRPCServer(('localhost', 9000), requestHandler=RequestHandler, allow_none=True) as server:
   server.register_introspection_functions()


   def signal_handler(signum, frame):
      print("received signal")
      server.server_close()

      # perform clean up, etc. here...

      print("exiting, gracefully")
      sys.exit(0)

   # signals
   signal.signal(signal.SIGTERM, signal_handler)
   signal.signal(signal.SIGHUP, signal_handler)
   signal.signal(signal.SIGINT, signal_handler)

   # register both functions

   server.register_function(listarTodasCompetiçoes)
   server.register_function(jogosPortugal)
   server.register_function(procurarJogosMaisGolos)
   server.register_function(gameResult)
   server.register_function(gamesByCompetition)
   server.register_function(drawByCompetition)
   server.register_function(pesquisaEquipa)
   server.register_function(top10JogoscomGolos)
   server.register_function(delete)
   server.register_function(insertDocument)
   server.register_function(xml_validator)
   server.register_function(validate)
   server.register_function(converter)
   server.register_function(format_data)

   # start the server
   print("Starting the RPC Server...")
   server.serve_forever()
