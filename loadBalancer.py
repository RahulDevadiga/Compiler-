import socket
import sys
import traceback
from threading import Thread
import os
import concurrent.futures

loadOfServer = {}   #dictionary which maps (ip,port) to load(in terms of numbers of clients connected  eg loadOfServer[(192.168.32.89, 6000)] = 3 means 3 clients connected

serverToClientMapping = {} #dictionary which maps server to serving clients eg serverToClientMapping[(192.168.32.89, 6000)] = [(192.168.32.99, 6000), (192.168.32.87, 6000), (192.168.32.86, 6000)]

serverOfClient = {}

def start_loadbalancer():
   global loadOfServer
   global serverToClientMapping
   host = "0.0.0.0"
   port = 1234 # arbitrary non-privileged port
   soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   print("Socket created")
   try:
      soc.bind((host, port))
   except:
      print("Bind failed. Error : " + str(sys.exc_info()))
      sys.exit()
   soc.listen(6) # queue up to 6 requests
   print("Socket now listening")
   # infinite loop- do not reset for every requests
   while True:
      connection, address = soc.accept()
      ip, port = str(address[0]), str(address[1])
      print("Loadbalancer Connected with client " + ip + ":" + port)
      clientAddress = (ip, port)
      serverWithMinimumLoad = list(loadOfServer.keys())[ list(loadOfServer.values()).index(min(loadOfServer.values())) ]
      if serverWithMinimumLoad in serverToClientMapping:
          serverToClientMapping[serverWithMinimumLoad] = [clientAddress]
      else:
          serverToClientMapping[serverWithMinimumLoad].append(clientAddress)
      loadOfServer[serverWithMinimumLoad] += 1
      serverOfClient[clientAddress] = serverWithMinimumLoad
      print("Load of servers ", loadOfServer)
      print("Server to client mapping ", serverToClientMapping)  
      try:
         Thread(target=clientThread, args=(connection, ip, port)).start()
      except:
         print("Thread did not start.")
         traceback.print_exc()
   soc.close()

def serverThread(message, ip, port, max_buffer_size = 5120):
   '''connect loadbalancer to server'''

   soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   serverip = "127.0.0.1"
   serverport = 8000
   try:
      soc.connect((serverip, serverport))
      soc.sendall(message)
      outputreturned = soc.recv(5120).decode("utf8")
      print("output returned ", outputreturned)
   except:
      print("Connection Error")
      sys.exit()
   return outputreturned

def clientThread(connection, ip, port, max_buffer_size = 5120):
   '''connect client to loadbalancer'''
   global loadOfServer, serverToClientMapping, serverOfClient 
   is_active = True
   while is_active:
      serverip, serverport = serverOfClient[(ip, port)]
      client_input = receive_input(connection, max_buffer_size)
      if b"--QUIT--" in client_input:
         print("Client is requesting to quit")
         connection.close()
         print("Connection " + ip + ":" + port + " closed")
         clientAddress = (ip, port)
         associatedatedServer = serverOfClient[clientAddress]
         loadOfServer[associatedatedServer] -= 1
         serverToClientMapping[associatedatedServer].remove(clientAddress)
         print("Load of servers ", loadOfServer)
         print("Server to client mapping ", serverToClientMapping)  
         is_active = False
      else:
         print("Processed result: {}".format(client_input))
         with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(serverThread, client_input, serverip, serverport)
            returnOutput = future.result()
            print(returnOutput)
			
         
         connection.sendall(returnOutput.encode())
         
		 
def receive_input(connection, max_buffer_size):
   print("recieve input called")
   client_input = connection.recv(max_buffer_size)
   if(client_input == b'--QUIT--'):
      return client_input
   client_input_size = sys.getsizeof(client_input)
   if client_input_size > max_buffer_size:
      print("The input size is greater than expected {}".format(client_input_size))
   #from_client = client_input.decode("utf8").rstrip()
   #lang = langName[int(from_client[-1])]
   #code = from_client[:len(from_client)-1:]
   #output = getOutput(code, lang)
   #print("output ",output)
   #return output
   return client_input
   
  
noOfServers = int(input("Enter the number of servers "))
for i in range(noOfServers):
	serverIpAddress = input(f"Enter the ip address of {i+1}th server")
	serverPortNumber = input(f"Enter the port number of {i+1}th server")
	serverAddress = (serverIpAddress, serverPortNumber)
	loadOfServer[(serverIpAddress, serverPortNumber)] = 0
	serverToClientMapping[serverAddress] = []
	
	
langName = {0:"c",1:"cpp",2:"java",3:"python2",4:"python3"}
start_loadbalancer()
