# Rabbitmq & Celery

It is a Distributed queue system, you can send many jobs and many workers will do job for you. Even you can monitor them.

### Install RabbitMQ
    apt-get update 
    apt-get install erlang
    apt-get install rabbitmq-server
    sudo rabbitmq-plugins enable rabbitmq_management# web running
    
then we can connect rabbitmq on
http://IP:15672/  or http://localhost:15672/  

if ERROR: node with name "rabbit" already running on "localhost"
https://www.cnblogs.com/Sisiflying/p/6386988.html 

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
------------------------------------------------------------------------------------
### Test
The **worker** and **producer** must be different computers.<br>

| Role | Job |
|------|-----|
|Producer|Push tasks to rabbitmq.|
|Worker|Get tasks from rabbitmq and do tasks, you maybe have more one workers.|
|Broker|Rabbitmq server, transfer tasks.|

The Distributed queue system has three roles.

------------------------------------------------------------------------------------
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

### On Node
The Worker role, run this command to get tasks.

    celery -A Worker worker --loglevel=info
### On Server
The Producer and Broker role, run this command to push
    
    python3 Producer.py
--------------------------------------------------------------------------------
Server need install : rabbitmq-server, celery
<!--crontab : git clone url, python3 job-->

Node need install : celery
<!--crontab : git clone url
vim /etc/rc.local # it will run on boot-->

### Set Queue Group
Send tasks : @app.task change to @app.task( queue = **queue_group_name** )
login web by worker user, then queues will show tasks group by **queue_group_name**
Get tasks : celery -A task worker --loglevel=info -Q **queue_group_name** 



<!--Set Watch
pip install watchdog

watchmedo auto-restart -- celery -A task worker --loglevel=info -Q add,add2,class-->

