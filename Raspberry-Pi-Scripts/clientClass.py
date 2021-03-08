import socket
import ssl
import os

class Client:
    def __init__(self, address, CaPath, ClientCrt, key):
        # set up the config
        config = ssl.SSLContext()
        config.verify_mode = ssl.CERT_REQUIRED
        config.load_cert_chain(ClientCrt, key)
        config.load_verify_locations(CaPath)
        #config.verify_flags |= 0x80000

        # create unsecure socket so we can convert it to secure socket
        soc = socket.socket()
        
        # saving address for reconnection
        self.address = address

        # found santa
        self.santaStatus = -1

        # create secure socket with our configuration 
        self.secureConnection = config.wrap_socket(soc, suppress_ragged_eofs=False)

        try:
            # connect to server
            self.secureConnection.connect(address)
            # creating connection status to check if client is still connected
            self.conStatus = True
            # close the unsecure socket
            soc.close
        except:
            raise Exception("can't connect to server")
            self.conStatus = False
            exit()

    
    def __del__(self):
        self.secureConnection.shutdown(socket.SHUT_RDWR)
        self.secureConnection.close()
        
    
    def Reconnect(self):
        try:
            # connect to server
            self.secureConnection.connect(self.address)
            self.conStatus = True
        except:
            print("can't connect to server")
            self.conStatus = False
    
    def foundSanta(self):
        if(self.santaStatus != 1):
            try:
                self.secureConnection.send('{"santa":true}'.encode())
                self.santaStatus = 1
            except:
                print("can't send data to server")
                # try to reconnect
                self.Reconnect()

    def noSanta(self):
        if(self.santaStatus != 0):
            try:
                self.secureConnection.send('{"santa":false}'.encode())
                self.santaStatus = 0
            except:
                print("can't send data to server")
                # try to reconnect
                self.Reconnect()