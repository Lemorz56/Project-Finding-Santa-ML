import ssl
import socket
import datetime
import time
import os
import httplib2

urlON = "http://192.168.1.180/toggleON"
urlOFF = "http://192.168.1.180/toggleOFF"

# create config 
context = ssl.SSLContext()
context.verify_mode = ssl.CERT_OPTIONAL
context.load_verify_locations("./CA.crt")
context.load_cert_chain(certfile="./server.crt", keyfile="./server.key")

# status of the server
serverOn = True

# accept all ips at port x
ipAddress = "0.0.0.0"
port = 15002

print("Starting: ")

# Create a unsecure server socket 
serverSocket = socket.socket()
#serverSocket.bind((ipAddress, port))

print("Creating Seclis: ")
# create secure socket
secLis = context.wrap_socket(serverSocket, server_side=True, suppress_ragged_eofs=False)
# close unsucure socket
serverSocket.close()
print(" bind:")
# bind secure socket
secLis.bind((ipAddress, port))

# Listen for incoming connections
#serverSocket.listen()
secLis.listen()
print("Server listening: ")


try:
	while(serverOn):
		# Keep accepting connections from clients
		(clientConnection, clientAddress) = secLis.accept()
		# Send current server time to the client
		print("Connection established")
		while(True):
			try:
				print("Trying to read...")
				msgReceived = clientConnection.recv()
				decoded = msgReceived.decode()

				if 'true' in decoded:
					h = httplib2.Http(".cache")
					resp, content = h.request(urlON, "GET")
				elif 'false' in decoded:
					h = httplib2.Http(".cache")
					resp, content = h.request(urlOFF, "GET")

				print(msgReceived.decode())
			except:
				print("Connection lost or Client disconnected")
				break
		print("\r\n\r\n")
		clientConnection.close()
except KeyboardInterrupt:
# Close the connection to the client
		serverOn = False
secLis.close()
