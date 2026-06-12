# CESI_Test_FL_In_Nukes

### Setting the stage

**docker build -t flower-app:latest .**

If an error happens that says the docker daemon is deactivated or that cannot find a running docker you run (-v /home/ncuser/Desktop/CESI_Test_FL_In_Nukes/:/home/ncuser/Desktop/CESI_Test_FL_In_Nukes/ flower-app:latest python client_app.py 2 100.115.119.86
failed to connect to the docker API at unix:///var/run/docker.sock; check if the path is correct and if the daemon is running: dial unix /var/run/docker.sock: connect: no such file or directory
):

**sudo systemctl status docker** 

and if it says deactivate you run 

**sudo sustemctl start docker** 

After that try to create the docker image again

You need to create in the server and in all the client the network door for docker 

**sudo docker network create --driver bridge -o "com.docker.network.driver.mtu=1280" flower-net**

If you have already create something with the same name and you want to delete it is the command

**sudo docker network rm flower-net**

You need also to install and use the Tailscale. We do that so that the computers can be used here. All the computers need to be on the same account and run the following commands 

**sudo pacman -Syu tailscale**
**sudo systemctl enable --now tailscaled**

The following command will appear a link, go to this and make login

**sudo tailscale up**

With the following command you can see the ip

**tailscale ip -4**

-----------------------------------------
### Commands to run the server and clients

The following command is to run the server. In the server computer.

**docker run --rm --name flower-server   --network flower-net   -p 8080:8080   --privileged   -v /home/ncuser/Desktop/CESI_Test_FL_In_Nukes:/home/ncuser/Desktop/CESI_Test_FL_In_Nukes   flower-app:latest python server_app.py**

The following commands should be run in the different computers the ip in the last part of each command should change to the ip of the server. Hit the command tailscale in the server take the ip and change it here.

Client 1:

**sudo docker run --rm --net=flower-net --name flower-client-1 --privileged   -v /home/ncuser/Desktop/CESI_Test_FL_In_Nukes:/home/ncuser/Desktop/CESI_Test_FL_In_Nukes flower-app:latest python client_app.py 0 100.115.119.86**

Client 2:

**sudo docker run --rm --net=flower-net --name flower-client-2 --privileged   -v /home/ncuser/Desktop/CESI_Test_FL_In_Nukes:/home/ncuser/Desktop/CESI_Test_FL_In_Nukes flower-app:latest python client_app.py 0 100.115.119.86**

Client 3:

**sudo docker run --rm --net=flower-net --name flower-client-3 --privileged   -v /home/ncuser/Desktop/CESI_Test_FL_In_Nukes:/home/ncuser/Desktop/CESI_Test_FL_In_Nukes flower-app:latest python client_app.py 0 100.115.119.86**
