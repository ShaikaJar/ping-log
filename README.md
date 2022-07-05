# ping-log
A very simple program to log ping-reply-times

# Get Started  
#### Installation  
You can download the repository as a zip and unpack it or just clone it with:
```
git clone https://github.com/ShaikaJar/ping-log.git
```  
Open the new folder with:
```
cd ping-log
```  
From here you can eather choose to start the Programm [manually](https://github.com/ShaikaJar/ping-log#starting-manually) or install it as a [service](https://github.com/ShaikaJar/ping-log#creating-a-service)

#### Starting manually  
You can start the program with:
```
python3 ./show.py
```
This will start Logging Pings and serving a plot to **_http://\<device-address\>:8042_**  


#### Creating a Service
You can create a new service and register it to start on system start with:   
```
sudo python3 ./create_service.py
```
This Service will do exactly the same as the show.py

#### Starting/Stopping the Service
The Service will be Started on System Start
If you want to start or the stop the service manually, just use
```
systemctl start ping_log
```
and
```
systemctl stop ping_log
``` 

#### Example Result

![Example-Image](./ping.png)
