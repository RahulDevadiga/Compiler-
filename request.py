from flask import Flask,redirect, url_for, request, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('compilerclient.html')
	#return "hello"

@app.route('/compile', methods = ['GET', 'POST'])
def compile():
	code = request.form.get('code')
	lang = request.form.get('language')

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
	return render_template('compilerclient.html',outputreturned = output.stdout.decode(), codereturned = code)
	
app.run(host = '127.0.0.1', port = 5000)