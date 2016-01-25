#installation
#servername = pypelyne.local


yum -y update
yum upgrade
yum clean all
#yum install -y libpng12 net-tools samba zip wget csh man telnet-server nano mc unzip
yum install -y libpng12 net-tools samba zip wget man nano mc unzip #csh (needed for rr?)
#curl http://beyondgrep.com/ack-2.14-single-file > /usr/bin/ack && chmod 0755 /usr/bin/ack

mkdir -p /pypelyne/royalrender_src
mkdir -p /pypelyne/royalrender_repository
mkdir -p /pypelyne/tactic_src
mkdir -p /pypelyne/tactic
mkdir -p /pypelyne/pypelyne_repo
mkdir -p /pypelyne/logs
chmod -R 0755 /pypelyne
chown -R nobody:nobody /pypelyne

wget --directory-prefix=/pypelyne/royalrender_src http://www.royalrender.de/download/7.0.29__installer.zip
wget --directory-prefix=/pypelyne/tactic_src http://community.southpawtech.com/sites/default/files/download/TACTIC%20-%20Enterprise/TACTIC-4.4.0.v02.zip

chcon -R -t samba_share_t /pypelyne
#restorecon -v /pypelyne

#http://www.tecmint.com/firewalld-rules-for-centos-7/
#samba
firewall-cmd --permanent --zone=public --add-service=samba
#rrServer
firewall-cmd --permanent --zone=public --add-port=7773/tcp
#telnet
#firewall-cmd --permanent --zone=public --add-port=23/tcp
#python
#firewall-cmd --permanent --zone=public --add-port=50000/tcp
#python
#firewall-cmd --permanent --zone=public --add-port=50001/tcp
firewall-cmd --reload


mv /etc/samba/smb.conf /etc/samba/smb.conf.bak
nano /etc/samba/smb.conf

# samba
# https://www.howtoforge.com/samba-server-installation-and-configuration-on-centos-7

[global]
workgroup = WORKGROUP
server string = Samba Server %v
netbios name = centos
security = user
map to guest = bad user
dns proxy = no

#============================ Share Definitions ============================== 
[pypelyne]
path = /pypelyne
browsable =yes
writeable = yes
guest ok = yes
read only = no
follow symlinks = no


systemctl enable smb.service && systemctl enable nmb.service

systemctl restart smb.service && systemctl restart nmb.service


# scp michaelmussato@192.168.0.15:/Users/michaelmussato/Desktop/rrPypelyneRepo.tar.gz /root

# tar vxf /root/rrPypelyneRepo.tar.gz -C /pypelyne/royalrender_repository

unzip /pypelyne/royalrender_src/7.0.29__installer.zip -d /pypelyne/royalrender_src/
unzip /pypelyne/tactic_src/TACTIC-4.4.0.v02.zip -d /pypelyne/tactic_src

chmod -R 0755 /pypelyne
chown -R nobody:nobody /pypelyne

yum clean all


# ln -s /pypelyne/royalrender_repository/lx__rrServerconsole.sh /etc/init.d/lx__rrServerconsole
# ln -s /etc/init.d/lx__rrServerconsole /etc/rc3.d/S99lx__rrServerconsole

# chmod a+x /pypelyne/PyPELyNE/server_scripts/centos7/rr_server/rr_server.sh
# ln -s /pypelyne/PyPELyNE/server_scripts/centos7/rr_server/rr_server.sh /etc/init.d/rr_server
chmod a+x /pypelyne/royalrender_src/rr_server.sh
ln -sf /pypelyne/royalrender_src/rr_server.sh /etc/init.d/rr_server  ####
# ln -s /etc/init.d/rr_server /etc/rc3.d/S90rr_server
chkconfig rr_server on

# chmod a+x /pypelyne/PyPELyNE/server_scripts/centos7/pypelyne_server/pypelyne_server.sh
# ln -s /pypelyne/PyPELyNE/server_scripts/centos7/pypelyne_server/pypelyne_server.sh /etc/init.d/pypelyne_server
# # ln -s /etc/init.d/pypelyne_-server /etc/rc3.d/S90pypelyne_server
# chkconfig pypelyne_server on



# csh /pypelyne/royalrender_repository/lx__rrServerconsole.sh &

# path mapping:
# win: mac: /Volumes/pypelyne linux: /pypelyne
# install workstation installer


cp /etc/issue /etc/issue.default
# edit issue.default:
nano /etc/issue.default
############################

Welcome to PyPELyNE Server
==========================

http://www.tinyurl.com/mussato
michimussato@gmail.com

host name:          \n

This is a \s (\S) system
Running Kernel \r on an \m

Default login:      root
Default password:   root


############################

# /sbin/ifup-local
cp -f /etc/issue.default /etc/issue;
# printf "IP:                 " >> /etc/issue;
# /bin/hostname -I              >> /etc/issue;
# # printf $(hostname -I)         >> /etc/issue;
# printf "\n\n\n"               >> /etc/issue;

reboot

# start rr to generate conf files
/pypelyne/royalrender_repository/bin/lx64/rrServerconsole





















previous

installation
servername = pypelyne.local


yum update -y
yum upgrade
yum clean all
yum install -y libpng12 net-tools samba zip wget csh man telnet-server nano mc unzip
#curl http://beyondgrep.com/ack-2.14-single-file > /usr/bin/ack && chmod 0755 /usr/bin/ack

mkdir -p /pypelyne/royalrender_repository
mkdir -p /pypelyne/tactic
chmod -R 0755 /pypelyne
chown -R nobody:nobody /pypelyne

#wget --directory-prefix=/pypelyne/royalrender_repository http://www.royalrender.de/download/7.0.29__installer.zip
#wget --directory-prefix=/pypelyne/tactic http://community.southpawtech.com/sites/default/files/download/TACTIC%20-%20Enterprise/TACTIC-4.4.0.v02.zip

chcon -R -t samba_share_t /pypelyne
#restorecon -v /pypelyne 

#http://www.tecmint.com/firewalld-rules-for-centos-7/
firewall-cmd --permanent --zone=public --add-service=samba		#samba
firewall-cmd --permanent --zone=public --add-port=7773/tcp		#rrServer
firewall-cmd --permanent --zone=public --add-port=23/tcp		#telnet
#firewall-cmd --permanent --zone=public --add-port=50000/tcp		#python
firewall-cmd --permanent --zone=public --add-port=50001/tcp		#python
firewall-cmd --reload


mv /etc/samba/smb.conf /etc/samba/smb.conf.bak
nano /etc/samba/smb.conf

#samba
#https://www.howtoforge.com/samba-server-installation-and-configuration-on-centos-7

[global]
workgroup = WORKGROUP
server string = Samba Server %v
netbios name = centos
security = user
map to guest = bad user
dns proxy = no

#============================ Share Definitions ============================== 
[pypelyne]
path = /pypelyne
browsable = yes
writeable = yes
guest ok = yes
read only = no
follow symlinks = no


systemctl enable smb.service && systemctl enable nmb.service

systemctl restart smb.service && systemctl restart nmb.service


scp michaelmussato@192.168.0.15:/Users/michaelmussato/Desktop/rrPypelyneRepo.tar.gz /root

tar vxf /root/rrPypelyneRepo.tar.gz -C /pypelyne/royalrender_repository

unzip /pypelyne/royalrender_repository/7.0.29__installer.zip -d /pypelyne/royalrender_repository/
unzip /pypelyne/tactic/TACTIC-4.4.0.v02.zip -d /pypelyne/tactic/

chmod -R 0755 /pypelyne
chown -R nobody:nobody /pypelyne

yum clean all
reboot

#ln -s /pypelyne/royalrender_repository/lx__rrServerconsole.sh /etc/init.d/lx__rrServerconsole
#ln -s /etc/init.d/lx__rrServerconsole /etc/rc3.d/S99lx__rrServerconsole

chmod a+x /pypelyne/royalrender_src/rr_server.sh
ln -sf /pypelyne/royalrender_src/rr_server.sh /etc/init.d/rr_server
#ln -s /etc/init.d/rr_server /etc/rc3.d/S90rr_server
chkconfig rr_server on

chmod a+x /pypelyne/PyPELyNE/server_scripts/centos7/pypelyne_server/pypelyne_server.sh
ln -s /pypelyne/PyPELyNE/server_scripts/centos7/pypelyne_server/pypelyne_server.sh /etc/init.d/pypelyne_server
#ln -s /etc/init.d/pypelyne_-server /etc/rc3.d/S90pypelyne_server
chkconfig pypelyne_server on



#csh /pypelyne/royalrender_repository/lx__rrServerconsole.sh &

#path mapping:
#win: mac: /Volumes/pypelyne linux: /pypelyne
#install workstation installer


cp /etc/issue /etc/issue.default
#edit issue.default:
nano /etc/issue.default
############################

Welcome to PyPELyNE Server
==========================

http://www.tinyurl.com/mussato
michimussato@gmail.com

host name:          \n

This is a \s (\S) system
Running Kernel \r on an \m

Default login:      root
Default password:   root


############################

#/sbin/ifup-local
cp -f /etc/issue.default /etc/issue;
#printf "IP:                 " >> /etc/issue;
#/bin/hostname -I              >> /etc/issue;
##printf $(hostname -I)         >> /etc/issue;
#printf "\n\n\n"               >> /etc/issue;