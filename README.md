# CESI_Test_FL_In_Nukes

**docker build -t flower-app:latest .**

If an error happens that says the docker daemon is deactivated or that cannot find a running docker you run:

**sudo systemctl status docker** 

and if it says deactivate you run 

**sudo sustemctl start docker** 

After that try to create the docker image again

The following command is to run the server. In the server computer.

**docker run --rm   --name flower-server   --network flower-net   -p 8080:8080   flower-app:latest   python server_app.py**


The following commands should be run in the different computers 

Client 1:

**sudo docker run --rm --net=flower-net --name flower-client-1 flower-app:latest python client_app.py 0 100.115.119.86**

Client 2:

**sudo docker run --rm --net=flower-net --name flower-client-2 flower-app:latest python client_app.py 0 100.115.119.86**

Client 3:

**sudo docker run --rm --net=flower-net --name flower-client-3 flower-app:latest python client_app.py 0 100.115.119.86**
