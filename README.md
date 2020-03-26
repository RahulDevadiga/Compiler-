# Compiler

# Description

  The resources that are needed to compile the code are installed in the server. Once server.py is run on the server machine, it starts listening for requests. 
  The code supports for multiple servers and multiple clients. Multi-threading is used to handle multiple requests. As soon as it recieves request from a new client, a new thread is created which handles the request from that particular client.

  The task of servercompiler.py file is to use the resources(like C compiler, JVM, Java compiler, C++ compiler, Python Compiler) to compile the code and returns its output.
  Note that the path of all the directories must be available in PATH environment variable. 

  The clientcompiler.py is written using Flask framework, the code can be written in any of the 5 languages and can be submitted any number of times.

  Since, we have the privilege of multiple servers, we make use of loadbalancer whose sole purpose is to assign a particular client to a particular server based on the load.
  The server which has the minimum load is assigned to the new client.

  The task assignment approach with minimum load of load balancing is used here. The number of clients can increased dynamically and loadbalancer will do its task.
  
# Installation requirements
  
  for client ->
      pip install Flask
      pip install requests
      
  for server ->
      Python2, Python3, C, Java, C++ compilers 
      
    First run servercompiler.py in all the servers  
        python3 servercompiler.py

    Run a loadbalancer by command
        python3 loadbalancer.py

    Run clientcompiler in all the client machines
        python3 clientcompiler.py
        
       


  
      
  
