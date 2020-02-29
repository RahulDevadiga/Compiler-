from flask import Flask,redirect, url_for, request, render_template
import subprocess
import socket
import sys

app = Flask(__name__)
soc = None
langId = {"c":0,"cpp":1,"java":2,"python2":3,"python3":4}

@app.route('/')
def home():
	global soc
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = "127.0.0.1"
	port = 8000
	try:
		soc.connect((host, port))
	except:
		print("Connection Error")
		sys.exit()
	return render_template('compilerclient.html')
	#return "hello"

@app.route('/compile', methods = ['GET', 'POST'])
def compile():
	global soc
	code = request.form.get('code')
	lang = request.form.get('language')
	print(code,lang)
	print("Socket os",soc)
	
	soc.sendall(b"".join([code.encode(), str(langId[lang]).encode()]))
	outputreturned = soc.recv(5120).decode("utf8")
	
	print("###################output returned ",outputreturned)
	return render_template('compilerclient.html',outputreturned = outputreturned, codereturned = code, langreturned = lang)
	
app.run(host = '127.0.0.1', port = 5000)