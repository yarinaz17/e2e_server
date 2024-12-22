import socket
import threading
from cryptomanager import *
from connection import *
from requesthandler import *
MAX_CONNECTIONS = 5


class Server:
    connections = []
    clients = []
    pending = []

    def __init__(self, port):
        self.port = port

    def start(self):
        print("[SERVER] Starting ...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
            # bind the socket to localhost
            serversocket.bind(('127.0.0.1', self.port))
            print(f"[SERVER] Server is listening on 127.0.0.1:{self.port}")
            # start listening
            serversocket.listen(5)

            while True:
                # accept connections from outside
                (clientsocket, address) = serversocket.accept()
                if len(self.connections) >= MAX_CONNECTIONS:
                    print(
                        f"[SERVER] Denied connection from {address}. Too many clients already connected.")
                    clientsocket.close()
                    continue

                print(f"[SERVER] New connection approved from : {address}")

                # create new connection object
                crypt = CryptoManager()
                conn = Connection(clientsocket, crypt)
                # append the connection to the list of active connections
                self.connections.append(conn)
                # handle communication with client on a new thread
                ct = threading.Thread(
                    target=self.handle_client, args=(conn,))
                ct.start()

                # TODO: start another thread that probes for connected client and checks if they have a pending message in the 'pending' list

    def handle_client(self, conn: Connection):
        # while client is connected perform : (we'll break from the loop when the client disconnects)
        handler = RequestHandler()
        while True:
            try:
                request = conn.read_request()
            except Exception as ex:
                print(f"Exception {type(ex).__name__} occurred. {ex.args}")
                print("[SERVER] Connection with peer has been terminated")
                conn.close()
                self.connections.remove(conn)
                break
            response = handler.handle_request(request, client_user)
            if response != None:
                conn.send_response(response)
