# Rabbitmq & Celery



It is a Distributed queue system, you can send many jobs and many workers will do job for you. Even you can monitor them.<br>

**note** : If you only have one computer, the linode is good support, the min calculator only need $5/no, it is enough for being worker.

#### [Install](https://github.com/f496328mm/RabbitmqCelery#install-rabbitmq)
#### [Create Account](https://github.com/f496328mm/RabbitmqCelery#create-web-account)
#### [Example](https://github.com/f496328mm/RabbitmqCelery#Example)
#### [Run](https://github.com/f496328mm/RabbitmqCelery#on-node)
#### [Set Queue Group](https://github.com/f496328mm/RabbitmqCelery#set-queue-group)

----------------------------

### Install RabbitMQ
    apt-get update 
    apt-get install erlang
    apt-get install rabbitmq-server
    sudo rabbitmq-plugins enable rabbitmq_management# web running
    
then we can connect rabbitmq on
http://IP:15672/  or http://localhost:15672/  
if ERROR: node with name "rabbit" already running on "localhost"
https://www.cnblogs.com/Sisiflying/p/6386988.html 

------------------
### Create Web Account

    cd /user/sbin
    ./rabbitmqctl set_user user password # set user and password
    ./rabbitmqctl set_user_tags user administrator # set user status
    ./rabbitmqctl set_permissions -p / user ".*" ".*" ".*"     # set connect IP
or

    rabbitmqctl add_user user password # set user and password
    rabbitmqctl set_user_tags user administrator # set user status
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
|Producer|Push tasks to rabbitmq.|
|Worker|Get tasks from rabbitmq and do tasks, you maybe have more one workers.|
|Broker|Rabbitmq server, transfer tasks.|

The **worker** and **producer** must be different computers.

------------------
Create Tasks.py, 

    import os, sys
    PATH = '/'.join( os.path.abspath(__file__).split('/')[:-1] )
    sys.path.append(PATH)
    from Worker import app
    @app.task()
    def add(x,y):
        return x+y

Create Worker.py, 

    import os, sys
    PATH = '/'.join( os.path.abspath(__file__).split('/')[:-1] )
    sys.path.append(PATH)
    from celery import Celery
    app = Celery("task",
                 include=["Tasks"],# tasks file name
                 broker='pyamqp://worker_user:worker_password@Rabbitmq_IP:5672/')
Create Producer.py

    import os, sys
    PATH = '/'.join( os.path.abspath(__file__).split('/')[:-1] )
    sys.path.append(PATH)
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

<!--Set Watch
pip install watchdog

watchmedo auto-restart -- celery -A task worker --loglevel=info -Q add,add2,class-->

