from flask import Flask,redirect, url_for, request, render_template
import subprocess
import socket

app = Flask(__name__)
client = None
langId = {"c":0,"cpp":1,"java":2,"python2":3,"python3":4}

@app.route('/')
def home():
	global client
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(('127.0.0.1', 8080))
	return render_template('compilerclient.html')
	#return "hello"

@app.route('/compile', methods = ['GET', 'POST'])
def compile():
	global client
	code = request.form.get('code')
	lang = request.form.get('language')
	print(code,lang)
	client.send(b"".join([code.encode(), str(langId[lang]).encode()]))
	compiledOutput = client.recv(4096)
	return render_template('compilerclient.html',outputreturned = compiledOutput.decode(), codereturned = code)
	
app.run(host = '127.0.0.1', port = 5000)