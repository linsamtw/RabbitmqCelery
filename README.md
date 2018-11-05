# Rabbitmq & Celery



It is a Distributed queue system, you can send many jobs and many workers will do job for you. And you can monitor them.<br>

**note** : If you only have one computer, the **linode** is good support, the min calculator only need $5/month, it is enough for being worker.

*  [Install](https://github.com/f496328mm/RabbitmqCelery#install-rabbitmq)
*  [Create Account](https://github.com/f496328mm/RabbitmqCelery#create-web-account)
*  [Example](https://github.com/f496328mm/RabbitmqCelery#Example)
*  [Run](https://github.com/f496328mm/RabbitmqCelery#on-node)
*  [Set Queue Group](https://github.com/f496328mm/RabbitmqCelery#set-queue-group)
*  [Other](https://github.com/f496328mm/RabbitmqCelery/blob/master/README.md#other)
*  [Run Celery On Python3](https://github.com/f496328mm/RabbitmqCelery#run-celery-on-python3)
*  [Kill Process](https://github.com/f496328mm/RabbitmqCelery#kill-process)
*  [Git No Need Password](https://github.com/f496328mm/RabbitmqCelery#git-no-need-password)
*  [Set Watchdog](https://github.com/f496328mm/RabbitmqCelery#set-watchdog)

----------------------------

### Install RabbitMQ
    apt-get update 
    apt-get install erlang
    apt-get install rabbitmq-server
    sudo rabbitmq-plugins enable rabbitmq_management# web running

then we can connect rabbitmq on
http://IP:15672/  or http://localhost:15672/  
<!--if ERROR: node with name "rabbit" already running on "localhost"
https://www.cnblogs.com/Sisiflying/p/6386988.html -->

### Install Celery
    apt-get install python3-pip
    export LC_ALL="en_US.UTF-8"
    pip3 install celery

------------------
### Create Web Account

    cd /user/sbin
    ./rabbitmqctl set_user user password # set user and password
    ./rabbitmqctl set_user_tags user administrator # set user permission
    ./rabbitmqctl set_permissions -p / user ".*" ".*" ".*"     # set connect IP
or

    rabbitmqctl add_user user password # set user and password
    rabbitmqctl set_user_tags user administrator # set user permission
    rabbitmqctl set_permissions -p / user ".*" ".*" ".*"     # set connect IP

### Create Worker Account

    cd /user/sbin
    ./rabbitmqctl add_user worker_user worker_password
    ./rabbitmqctl set_user_tags worker_user policymaker
    ./rabbitmqctl set_permissions -p / worker_user ".*" ".*" ".*"   
or

    rabbitmqctl add_user worker_user worker_password
    rabbitmqctl set_user_tags worker_user policymaker
    rabbitmqctl set_permissions -p / worker_user ".*" ".*" ".*"   
    
The queues on rabbitmq web only can appear by worker user.

------------------

### Example
The Distributed queue system has three roles.

| Role | Job |
|------|-----|
|Worker|Get tasks from rabbitmq and do tasks, you maybe have more one workers.|
|Broker|Rabbitmq server, transfer tasks.|
|Producer|Push tasks to rabbitmq.|

The **worker** and **producer** should be different computers.

------------------
Create Worker.py, 

    from celery import Celery
    app = Celery("task",
                 include=["Tasks"],# tasks file name
                 broker='pyamqp://worker_user:worker_password@Rabbitmq_IP:5672/')

Create Tasks.py, 

    from Worker import app
    @app.task()
    def add(x,y):
        return x+y
        
Create Producer.py

    from Tasks import add
    add.delay(0,0)
    
------------------
### On Node
The Worker role, run this command to get tasks.

    celery -A Worker worker --loglevel=info
### On Server
The Producer and Broker role, run this command to push
    
    python3 Producer.py
-------------------------------
Server need install : rabbitmq-server, celery
<!--crontab : git clone url, python3 job-->

Node need install : celery
<!--crontab : git clone url
vim /etc/rc.local # it will run on boot-->

-------------------------------
### Set Queue Group
* Send tasks : @app.task change to @app.task( queue = **queue_group_name** )
* Login web : worker user, then queues will show tasks group by **queue_group_name**
* Get tasks : celery -A task worker --loglevel=info -Q **queue_group_name** 

-------------------------------
## Other
### Run celery on Python3

    pip3 install virtualenv 
    virtualenv celery_for_python3
    source celery_for_python3/bin/activate
### Kill Process

    ps aux | grep celery | awk '{print $2}' | xargs # print PID
    ps aux | grep celery | awk '{print $2}' | xargs kill -9 # print PID and kill Process
### Git No Need Password
Paste your SSH key from  '~/.ssh/id_rsa.pub'. If you have no id_rsa.pub, you can follow that to generate ssh key.<br>

    cd ~/.ssh/
    ssh-keygen
then, paste to gitlab or github -> option -> ssh key
### Set Watchdog
If your celery on running, but the code will be changed.
The celery process can't update, because the code has be compiled.
The Watchdog which provides watchmedo, it can re-loading code into Celery after a change.

    pip3 install watchdog
    watchmedo auto-restart -- celery -A task worker --loglevel=info


