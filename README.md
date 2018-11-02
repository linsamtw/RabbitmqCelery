# RabbitmqCelery

### Install RabbitMQ
    apt-get update 
    apt-get install erlang
    apt-get install rabbitmq-server
    sudo rabbitmq-plugins enable rabbitmq_management# web running
    
then we can connect on web
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

### Test
**The worker and producer mush be different computers.**<br>
The Distributed queue system, Rabbitmq and Celery has three roles.

**Producer** : Push tasks to rabbitmq.<br>
**Worker** :  Get tasks from rabbitmq and do tasks, you maybe have more one workers.<br>
**Rabbitmq** : A broker, transfer tasks.<br>

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
Create  Producer.py

    import os, sys
    PATH = '/'.join( os.path.abspath(__file__).split('/')[:-1] )
    sys.path.append(PATH)
    from Tasks import add
    add.delay(0,0)

It must use command, run on spyder will fail

    celery -A task worker --loglevel=info
The worker, task, will wait for tasks from rabbitmq, and run tasks.
How push tasks to rabbitmq? 
Run send.py on server( rabbitmq server ), it is producer.

    from task import add
    result = add.delay(10,4)

--------------------------------------------------------------------------------
### On Server 
    Run rabbitmq and send.py, then sned.py will send tasks to rabbitmq.
    Need install : rabbitmq-server, celery
<!--crontab : git clone url, python3 job-->

### On Node 
    Run celery -A task worker --loglevel=info, it will get tasks from rabbitmq, then work tasks.
    Need install : celery
<!--crontab : git clone url
vim /etc/rc.local # it will run on boot-->
command line run this to get tasks: 

    celery -A task worker --loglevel=info 

### Set Queue Group
Send tasks : @app.task change to @app.task( queue = **queue_group_name** )
login web by worker user, then queues will show tasks group by **queue_group_name**
Get tasks : celery -A task worker --loglevel=info -Q **queue_group_name** 



<!--Set Watch
pip install watchdog

watchmedo auto-restart -- celery -A task worker --loglevel=info -Q add,add2,class-->

