# CESI_Test_FL_In_Nukes

**docker build -t flower-app:latest .**

If an error happens that says the docker daemon is deactivated or that cannot find a running docker you run:
**sudo systemctl status docker** 
and if it says deactivate you run 
**sudo sustemctl start docker** 
After that try to create the docker image again


**docker run --rm   --name flower-server   --network flower-net   -p 8080:8080   flower-app:latest   python server_app.py**

The following command is to create the tunel between the client and the server through ssh
**ssh -N -L 0.0.0.0:8080:127.0.0.1:8080 ncuser@10.191.44.101**

The following commands should be run in the different computers 
**sudo docker run --rm   --name flower-client-1   --add-host=host.docker.internal:host-gateway   flower-app:latest   python client_app.py 0 host.docker.internal**
**sudo docker run --rm   --name flower-client-2   --add-host=host.docker.internal:host-gateway   flower-app:latest   python client_app.py 0 host.docker.internal**
**sudo docker run --rm   --name flower-client-3   --add-host=host.docker.internal:host-gateway   flower-app:latest   python client_app.py 0 host.docker.internal**

The following command is the command that is used to let this port tcp to be used
**sudo ufw allow 8080/tcp**
