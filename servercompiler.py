import subprocess
import socket
import sys
import traceback
from threading import Thread
import os
	
noOfActiveClients = 0

def getOutput(code, lang):
	
	if lang == 'java':
		
		with open("MainClass.java","w") as f:
			f.write(code)
		output = subprocess.run(["javac","MainClass.java"], stdout = subprocess.PIPE)
		output = subprocess.run(["java","MainClass"], stdout = subprocess.PIPE)
		
		try:
			os.unlink("MainClass.java")
			os.unlink("MainClass.class")
		except:
			pass
		
		
	elif lang == 'python2':
		with open("MainClass.py","w") as f:
			f.write(code)
		output = subprocess.run(["python","MainClass.py"  ], stdout = subprocess.PIPE)
		os.unlink("MainClass.py")
			
	elif lang == 'python3':
		with open("MainClass.py","w") as f:
			f.write(code)
		output = subprocess.run(["python","MainClass.py"  ], stdout = subprocess.PIPE)
		os.unlink("MainClass.py")
			
			
	elif lang == 'cpp':
		with open("MainClass.cpp","w") as f:
			f.write(code)
		
		output = subprocess.run(["g++", "MainClass.cpp", "-o", "out1"], stdout = subprocess.PIPE)
		output = subprocess.run(["./out1"], stdout = subprocess.PIPE)
		os.unlink("MainClass.cpp")
			
		
	else:
		with open("MainClass.c","w") as f:
			f.write(code)
		output = subprocess.run(["gcc", "MainClass.c", "-o", "out1"], stdout = subprocess.PIPE)
		output = subprocess.run(["./out1"], stdout = subprocess.PIPE)
		os.unlink("MainClass.c")
	if(output.returncode == 1):
		return b'Error in the code'
	
	return output.stdout

def start_server():
   global noOfActiveClients
   host = "0.0.0.0"
   port = 8000 # arbitrary non-privileged port
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
      print("Connected with " + ip + ":" + port)
      noOfActiveClients += 1
      print("No of active clients ", noOfActiveClients)
      try:
         Thread(target=clientThread, args=(connection, ip, port)).start()
      except:
         print("Thread did not start.")
         traceback.print_exc()
   soc.close()

def clientThread(connection, ip, port, max_buffer_size = 5120):
   global noOfActiveClients
   is_active = True
   while is_active:
      
      client_input = receive_input(connection, max_buffer_size)
      if b"--QUIT--" in client_input:
         print("Client is requesting to quit")
         connection.close()
         print("Connection " + ip + ":" + port + " closed")
         noOfActiveClients -= 1
         print("No of active clients ", noOfActiveClients)
         is_active = False
      else:
         print("Processed result: {}".format(client_input))
         connection.sendall(client_input)
         
		 
def receive_input(connection, max_buffer_size):
   print("recieve input called")
   client_input = connection.recv(max_buffer_size)
   if(client_input == b'--QUIT--'):
      return client_input
   client_input_size = sys.getsizeof(client_input)
   if client_input_size > max_buffer_size:
      print("The input size is greater than expected {}".format(client_input_size))
   from_client = client_input.decode("utf8").rstrip()
   lang = langName[int(from_client[-1])]
   code = from_client[:len(from_client)-1:]
   output = getOutput(code, lang)
   print("output ",output)
   return output
  
   
langName = {0:"c",1:"cpp",2:"java",3:"python2",4:"python3"}
start_server()
