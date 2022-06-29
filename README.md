# ping-log
very simple programm to log ping-reply-times

# Get Started
Just download the Repository and start the scripts as described in [Usage](#usage)  
To download the Repo you can use:  
```
git clone https://github.com/ShaikaJar/ping-log.git
```  

# Usage 
#### Logging
You can start a new [screen](https://help.ubuntu.com/community/Screen) that logs ping-results with:   
```
./start.sh
```

#### Plotting  
[./start-show.sh](./start-show.sh) will 
You can start a new screen that plots the content of the last 8 hours of data from the log-file with:
```
./start-show.sh
```
The plot will be served to http://\<device-address\>:8042  
If you run the script on the device you want to view it will be available on [localhost:8042](http://localhost:8042)

#### Example Result

![Example-Image](./ping.png)