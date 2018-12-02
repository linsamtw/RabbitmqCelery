# Rabbitmq & Celery

It is a Distributed queue system, you can send many jobs and many workers will do job for you. And you can monitor them.<br>

**note** : If you only have one computer, the **linode** is good support, the min calculator only need $5/month, it is enough for being worker.
* [Rabbitmq & Celery](https://github.com/f496328mm/RabbitmqCelery#rabbitmq--celery-1)
    *  [Install](https://github.com/f496328mm/RabbitmqCelery#install-rabbitmq)
    *  [Create Account](https://github.com/f496328mm/RabbitmqCelery#create-web-account)
    *  [Example](https://github.com/f496328mm/RabbitmqCelery#Example)
    *  [Run](https://github.com/f496328mm/RabbitmqCelery#on-node)
    *  [Return Result](https://github.com/f496328mm/RabbitmqCelery#return-result-by-apply_async)
    *  [Set Queue Group](https://github.com/f496328mm/RabbitmqCelery#set-queue-group)
* [Folwer](https://github.com/f496328mm/RabbitmqCelery#flower)
    *  [Install](https://github.com/f496328mm/RabbitmqCelery#install)
* [Supervisor](https://github.com/f496328mm/RabbitmqCelery#supervisor)
    *  [Install](https://github.com/f496328mm/RabbitmqCelery#install-1)
* [Git](https://github.com/f496328mm/RabbitmqCelery#git)
    *  [Git No Need Password](https://github.com/f496328mm/RabbitmqCelery#git-no-need-password)
    *  [change github pull and push to no need password](https://github.com/f496328mm/RabbitmqCelery#change-github-pull-and-push-to-no-need-password)
    *  [git command](https://github.com/f496328mm/RabbitmqCelery#git-command)
*  [Other](https://github.com/f496328mm/RabbitmqCelery#other)
    *  [Run Celery On Python3](https://github.com/f496328mm/RabbitmqCelery#run-celery-on-python3)
    *  [Kill Process](https://github.com/f496328mm/RabbitmqCelery#kill-process)
    *  [Set Watchdog](https://github.com/f496328mm/RabbitmqCelery#set-watchdog)

----------------------------
## Rabbitmq & Celery
#### Install RabbitMQ
    apt-get update 
    apt-get install erlang
    apt-get install rabbitmq-server
    sudo rabbitmq-plugins enable rabbitmq_management# web running

then we can connect rabbitmq on
http://IP:15672/  or http://localhost:15672/  
<!--if ERROR: node with name "rabbit" already running on "localhost"
https://www.cnblogs.com/Sisiflying/p/6386988.html -->

#### Install Celery
    apt-get install python3-pip
    export LC_ALL="en_US.UTF-8"
    pip3 install celery

------------------
#### Create Web Account

    cd /user/sbin
    ./rabbitmqctl set_user user password # set user and password
    ./rabbitmqctl set_user_tags user administrator # set user permission
    ./rabbitmqctl set_permissions -p / user ".*" ".*" ".*"     # set connect IP
or

    rabbitmqctl add_user user password # set user and password
    rabbitmqctl set_user_tags user administrator # set user permission
    rabbitmqctl set_permissions -p / user ".*" ".*" ".*"     # set connect IP

#### Create Worker Account

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

#### Example
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
    add.apply_async(0,0)# 
    
------------------
#### On Node
The Worker role, run this command to get tasks.

    celery -A Worker worker --loglevel=info
#### On Server
The Producer and Broker role, run this command to push
    
    python3 Producer.py
-------------------------------
#### Return Result By apply_async
    app = Celery("task",
                 include=["Tasks"],# tasks file name
                 backend='rpc://',
                 broker='pyamqp://worker_user:worker_password@Rabbitmq_IP:5672/')
-------------------------------
Server need install : rabbitmq-server, celery
<!--crontab : git clone url, python3 job-->

Node need install : celery
<!--crontab : git clone url
vim /etc/rc.local # it will run on boot-->
-------------------------------
#### Set Queue Group
* Send tasks : @app.task change to @app.task( queue = **queue_group_name** )
* Login web : worker user, then queues will show tasks group by **queue_group_name**
* Get tasks : celery -A task worker --loglevel=info -Q **queue_group_name** 

## Flower

Flower is a monitor system, it can monitor workers.
#### install
    pip3 install flower
#### Run

    # web running
    flower -A Worker --port=5555
    #Node run this command
    celery -A Worker worker --loglevel=info

## Supervisor
It must be install by root.

      sudo su
      python # Running celery, it it run this python version.
You can install Anaconda(3) to control your version.

      Do you wish the installer to prepend the Anaconda3 install location
      to PATH in your /root/.bashrc ? [yes|no]
      yes

#### install
    sudo apt-get install supervisor
#### Running

      sudo systemctl enable supervisor 
      sudo systemctl disable supervisor
      sudo systemctl status supervisor 

      sudo service supervisor start
      sudo service supervisor stop
      sudo service supervisor restart
#### Set
    
    sudo vim /etc/supervisor/conf.d/celery_*.conf

    [program:celeryd_1]
    directory=your directory path
    command=celery -A tasks worker --loglevel=error --maxtasksperchild=1 --concurrency=8 --hostname=%%h_1 -Q seat_float
    stdout_logfile=/var/log/celery/celeryd_1.log
    stderr_logfile=/var/log/celery/celeryd_1.err
    autostart=true
    autorestart=true
    startsecs=10
    stopwaitsecs=600
    stopasgroup=true
    killasgroup=true
-------------------------------
## Git
#### Git No Need Password
Paste your SSH key from  '~/.ssh/id_rsa.pub'. If you have no id_rsa.pub, you can follow that to generate ssh key.<br>

    cd ~/.ssh/
    ssh-keygen
then, paste to gitlab or github -> option -> ssh key<br>

#### change github pull and push to no need password

    git remote -v #show git is follow https or ssh. push or pull by no password must be ssh.
    #You can change the URL with:
    git remote set-url origin git+ssh://git@github.com/username/reponame.git
#### git command 
      # change loacal branch
      git checkout master 
      # check local branch version 
      git branch 
      # create a new branch
      git branch test 
      # push branch to gitlab or github
      git push origin test 
      # merge 
      git checkout master 
      git merge test
      # delete
      git branch -d <branch>
-------------------------------
## Other
#### Run celery on Python3

    pip3 install virtualenv 
    virtualenv celery_for_python3
    source celery_for_python3/bin/activate
#### Kill Process

    ps aux | grep celery | awk '{print $2}' | xargs # print PID
    ps aux | grep celery | awk '{print $2}' | xargs kill -9 # print PID and kill Process


#### Set Watchdog
If your celery on running, but the code will be changed.
The celery process can't update, because the code has be compiled.
The Watchdog which provides watchmedo, it can re-loading code into Celery after a change.

    pip3 install watchdog
    watchmedo auto-restart -- celery -A task worker --loglevel=info

If temperature too high or memory too less, then reboot.

#### Worker
Linode or Raspberry Pi will install our python packages, we will have packages list.


#### Set Linode System Date
The date from linode is follow US. If you are Taiwan, you can change the date from the command

      sudo dpkg-reconfigure tzdata

<!--

# git
*/1 * * * *   pi  bash /home/pi/bin/autoGitForCrawlerTg.sh

Worker

sudo vim /etc/supervisor/conf.d/worker.conf

[program:celeryd_1]
directory=/worker/gitlab/FinancialMining/Tasks
command=celery -A Worker worker --loglevel=info --maxtasksperchild=1 --concurrency=8 --hostname=%h_1
stdout_logfile=/var/log/celery/worker.log
stderr_logfile=/var/log/celery/worker.err
autostart=true
autorestart=true
startsecs=10
stopwaitsecs=600
stopasgroup=true
killasgroup=true


### Rabbitmq&Flower

sudo vim /etc/supervisor/conf.d/flower.conf

      [program:flowerd]
      command=celery flower --broker=amqp://worker:worker@172.105.212.230:5672/
      stdout_logfile=/var/log/celery/flowerd.log
      stderr_logfile=/var/log/celery/flowerd.err
      autostart=true
      autorestart=false
      startsecs=10
      stopwaitsecs=600

sudo vim /home/worker/gitlab/autogit.sh 

      cd your project path
      git pull




sudo vim /etc/crontab

# git
*/1 * * * *   root  bash /worker/gitlab/autogit.sh


-->


