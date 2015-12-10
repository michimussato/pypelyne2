#!/usr/bin/sh

#yum install -y net-tools nano wget unzip
yum install -y nano wget unzip httpd ImageMagick gcc zlib-devel libxslt-devel libxml2-devel python-devel

systemctl disable firewalld
systemctl stop firewalld

#yum install -y postgresql postgresql-server postgresql-contrib postgresql-devel

#yum install -y httpd

touch /var/www/html/index.html
#nano /var/www/html/index.html
#<html>
#    <head>
#        <title>Apache Base Install</title>
#    </head>
#    <body>
#        <p>Apache Install Successful</p>
#    </body>
#</html>

chmod 755 /var/www/html/index.html

systemctl start httpd.service
systemctl enable httpd.service
#chkconfig httpd on

firewall-cmd --permanent --zone=public --add-service=http
#firewall-cmd --permanent --zone=public --add-port=80/tcp

firewall-cmd --reload

reboot

#remove default postgres installation

#nano /etc/yum.repos.d/CentOS-Base.repo

#add to [base] and [updates]
#exclude=postgresql*

#rpm -Uvh http://yum.postgresql.org/9.2/redhat/rhel-6-x86_64/pgdg-centos92-9.2-6.noarch.rpm

yum install -y postgresql postgresql-server postgresql-contrib postgresql-devel
/usr/bin/postgresql-setup initdb

systemctl start postgresql.service
systemctl enable postgresql.service

reboot

#centos 6:
#su - postgres -c /usr/pgsql-9.2/bin/initdb


#centos 7:

#service postgresql-9.2 start
#chkconfig postgresql-9.2 on
#systemctl start postgresql-9.2.service
#systemctl enable postgresql-9.2.service
#sudo su postgres -
#/usr/bin/postgresql-setup initdb
#if fail:
#rm -rf /var/lib/pgsql/data
#https://rajivpandit.wordpress.com/2013/08/15/install-and-configure-tactic-4-0-on-centos6-4-rhel/

#su - postgres -c /usr/bin/postgresql-setup initdb
#su - postgres -c /usr/bin/postgres initdb

#yum install -y gcc zlib-devel libxslt-devel libxml2-devel
#yum install -y python-devel

#lxml
wget --directory-prefix=/tmp http://lxml.de/files/lxml-2.3.5.tgz
tar -xvf /tmp/lxml-2.3.5.tgz -C /tmp
cd /tmp/lxml-2.3.5
/usr/bin/python2.7 setup.py install

#PIL
wget --directory-prefix=/tmp http://effbot.org/downloads/Imaging-1.1.7.tar.gz
tar -xvf /tmp/Imaging-1.1.7.tar.gz -C /tmp
cd /tmp/Imaging-1.1.7
/usr/bin/python2.7 setup.py install

#Crypto
wget --directory-prefix=/tmp http://pypi.python.org/packages/source/p/pycrypto/pycrypto-2.3.tar.gz
tar -xvf /tmp/pycrypto-2.3.tar.gz -C /tmp
cd /tmp/pycrypto-2.3
/usr/bin/python2.7 setup.py install

#psycopg2
wget --directory-prefix=/tmp http://initd.org/psycopg/tarballs/PSYCOPG-2-4/psycopg2-2.4.6.tar.gz
tar -xvf /tmp/psycopg2-2.4.6.tar.gz -C /tmp
#pg_config=/usr/pgsql-9.2/bin/pg_config
nano /tmp/psycopg2-2.4.6/setup.cfg
cd /tmp/psycopg2-2.4.6
/usr/bin/python2.7 setup.py install


#yum install -y ImageMagick


#wget --directory-prefix=/tmp http://community.southpawtech.com/sites/default/files/download/TACTIC%20-%20Enterprise/TACTIC-4.4.0.v02.zip
wget --directory-prefix=/tmp http://community.southpawtech.com/sites/default/files/download/TACTIC%20-%20Enterprise/TACTIC-4.3.0.v02.zip
unzip /tmp/TACTIC-4.3.0.v02.zip -d /tmp
#unzip /tmp/TACTIC-4.3.0.v02.zip -d /tmp

systemctl stop postgresql-9.2.service

mv /var/lib/pgsql/data/pg_hba.conf /var/lib/pgsql/data/pg_hba.conf.INSTALL
#mv /var/lib/pgsql/9.2/data/pg_hba.conf /var/lib/pgsql/9.2/data/pg_hba.conf.INSTALL
cp /tmp/TACTIC-4.3.0.v02/src/install/postgresql/pg_hba.conf /var/lib/pgsql/data/pg_hba.conf
#cp /tmp/TACTIC-4.4.0.v02/src/install/postgresql/pg_hba.conf /var/lib/pgsql/9.2/data/pg_hba.conf

chown postgres:postgres /var/lib/pgsql/data/pg_hba.conf

systemctl start postgresql.service

reboot

#test:
psql -U postgres template1
#(\q to quit postgres)

#####everything fine till here...
#maybe try a different version
#tried suggested postgresql and standard centos 7 verison.
#fall over at the same point

export LC_ALL=en_US.utf-8

/usr/bin/python2.7 /tmp/TACTIC-4.3.0.v02/src/install/install.py
#(/home/apache) -> /opt/tactic
#(apache) ->
#if fail: rm -rf /opt/tactic/tactic_src_4.3.0.v02

#IMPORTANT NOTICE:
#
#
#        You are upgrading from an earlier version to 4.0.  TACTIC version 4.0 has made some important changes, particularly in the way that some tables are related to each other.  Previously, TACTIC would relate such items as snapshots, tasks and notes by the column "search_id".  In 4.0, this has been changed to "search_code".  The "search_id" will still exists, but wil not be used to relate tables.
#
#        In order to upgrade, TACTIC needs to fill in the "search_code" column of various tables.  This is a heavy process if you have a lot of data.  It is a non-destructive script and will only add data.  It will not change any current existing data.  You may wish to run this separately if you have large projects with lots of data.
#
#        You can run this script now or you can run it manually by:
#
#        python <TACTIC_INSTALL_DIR>/src/bin/fixes/fix_search_code.py

#Running ...
#
#cmd:  /usr/bin/python2.7 "/opt/tactic/tactic/src/bin/fixes/fix_search_code.py"
#
#
#Error:  duplicate key value violates unique constraint "search_object_code_idx"
#DETAIL:  Key (code)=(sthpw/custom_script) already exists.
#
#Please refer to the upgrade_output.txt file for any upgrade messages.
#
#Default project template files have been updated.
#
#
#*** Installation of TACTIC completed at [/opt/tactic] ***
#
#
#Next, please install the Apache Web Server and then copy the Apache config extension [/opt/tactic/tactic_data/config/tactic.conf] to the Apache web server config area. e.g. /etc/httpd/conf.d/
#
#Depending on the OS, you may need to add the following line to the main config file [httpd.conf] shipped with Apache as well:
#
#Include conf.d/*.conf

cp /opt/tactic/tactic_data/config/tactic.conf /etc/httpd/conf.d

#in /etc/httpd/conf/httpd.conf
#remove IncludeOptional conf.d/*.conf
#and add Include conf.d/*.conf
#if necessary

#nano /var/www/html/index.html
#remove contents and add line:
#printf "<META http-equiv=\"refresh\" content=\"0;URL=/tactic\">" > /var/www/html/index.html

systemctl restart httpd.service

#list modules:
/usr/sbin/httpd -t -D DUMP_MODULES

#check if these modules are in list:
#rewrite_module (shared)
#proxy_module (shared)
#proxy_http_module (shared)
#proxy_balancer_module (shared)
#deflate_module (shared)

chmod a+x /opt/tactic/tactic/src/install/service/tactic
/opt/tactic/tactic/src/install/service/tactic


#first start
su apache -s /bin/bash -c "/usr/bin/python2.7 /opt/tactic/tactic/src/bin/ startup_dev.py"
#su apache -s /bin/bash -c "/opt/python2.7/bin/python2.7 /opt/tactic/tactic/src/bin/startup_dev.py"

nano /opt/tactic/tactic/src/install/service/tactic
#change su - $TACTIC_USER -m -c "$LAUNCH" >> $LOG 2>&1 &
#to
su $TACTIC_USER -s /bin/bin/bash -m -c "$LAUNCH" >> $LOG 2>&1 &

#change LOG to
LOG=/pypelynes/log/tactic.log
