import subprocess
import socket

langName = {0:"c",1:"cpp",2:"java",3:"python2",4:"python3"}
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('0.0.0.0', 8080))
serv.listen(5)


def getOutput(code, lang):
	if lang == 'java':
	
		with open("MainClass.java","w") as f:
			f.write(code)
		output = subprocess.run(["javac","MainClass.java"  ], stdout = subprocess.PIPE)
		output = subprocess.run(["java","MainClass"], stdout = subprocess.PIPE)
		
	
	elif lang == 'python2':
		with open("MainClass.py","w") as f:
			f.write(code)
		output = subprocess.run(["python","MainClass.py"  ], stdout = subprocess.PIPE)
		
		
	elif lang == 'python3':
		with open("MainClass.py","w") as f:
			f.write(code)
		output = subprocess.run(["python","MainClass.py"  ], stdout = subprocess.PIPE)
		
		
	elif lang == 'cpp':
		with open("MainClass.c","w") as f:
			f.write(code)
	
		output = subprocess.run(["gcc", "HelloWorld.c", "-o", "out1"], stdout = subprocess.PIPE)
		output = subprocess.run(["./out1"], stdout = subprocess.PIPE)
		
		
	
	else:
		with open("MainClass.cpp","w") as f:
			f.write(code)
		output = subprocess.run(["g++", "HelloWorld.c", "-o", "out1"], stdout = subprocess.PIPE)
		output = subprocess.run(["./out1"], stdout = subprocess.PIPE)
	return output.stdout

while True:
    conn, addr = serv.accept()
    from_client = b''
    while True:
        data = conn.recv(4096)
        from_client = b''.join([from_client,data])
        from_client = from_client.decode()
        
        print(from_client)
        lang = langName[int(from_client[-1])]
        code = from_client[:len(from_client)-1:]
        output = getOutput(code, lang)
        print("output ",output)
        conn.send(output)
    conn.close()
    print('client disconnected')




def getOutput(code, lang):
	if lang == 'java':
	
		with open("MainClass.java","w") as f:
			f.write(code)
		output = subprocess.run(["javac","MainClass.java"  ], stdout = subprocess.PIPE)
		output = subprocess.run(["java","MainClass"], stdout = subprocess.PIPE)
		
	
	elif lang == 'python2':
		with open("MainClass.py","w") as f:
			f.write(code)
		output = subprocess.run(["python","MainClass.py"  ], stdout = subprocess.PIPE)
		
		
	elif lang == 'python3':
		with open("MainClass.py","w") as f:
			f.write(code)
		output = subprocess.run(["python","MainClass.py"  ], stdout = subprocess.PIPE)
		
		
	elif lang == 'cpp':
		with open("MainClass.c","w") as f:
			f.write(code)
	
		output = subprocess.run(["gcc", "HelloWorld.c", "-o", "out1"], stdout = subprocess.PIPE)
		output = subprocess.run(["./out1"], stdout = subprocess.PIPE)
		
		
	
	else:
		with open("MainClass.cpp","w") as f:
			f.write(code)
		output = subprocess.run(["g++", "HelloWorld.c", "-o", "out1"], stdout = subprocess.PIPE)
		output = subprocess.run(["./out1"], stdout = subprocess.PIPE)
	return render_template('compilerclient.html',outputreturned = output.stdout.decode(), codereturned = code, langreturned = lang)
	