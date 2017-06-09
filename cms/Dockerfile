FROM ubuntu:16.04

LABEL Maintainer Samira Ouaaz "souaaz@hcn-inc.com"

RUN apt-get update 
RUN apt-get install -y apt-utils sudo python git vim curl runit
RUN apt-get install -y  software-properties-common python-software-properties 

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get --assume-yes install postgresql postgresql-contrib python-pip
RUN apt-get --assume-yes install python2.7-dev

RUN apt-get --no-install-recommends -y install && \
    build-essential pkg-config erlang && \
    libicu-dev libmozjs185-dev libcurl4-openssl-dev

RUN pip install --upgrade pip && \
	pip install psycopg2 bcrypt Pillow Flask Flask-SQLAlchemy Flask-Mail Flask-WTF couchdb

RUN /etc/init.d/postgresql  start && sudo -u postgres psql < cms.sql


#EDIT app/initialize.py !!!
#cd cms2
#python
#>>> from app.initialize import init_db
#>>> init_db()
#>>> 


RUN useradd -ms /bin/bash builder && \
    usermod -aG sudo builder && \
    echo 'builder:builder' | sudo chpasswd

RUN useradd -ms /bin/bash couchdb && \
    usermod -aG sudo couchdb && \
    echo 'couchdb:couchdb' | sudo chpasswd

RUN mkdir -p /tmp && cd /tmp && \
	wget --quiet http://apache.forsale.plus/couchdb/source/2.0.0/apache-couchdb-2.0.0.tar.gz && \
	tar -zxvf apache-couchdb-2.0.0.tar.gz && \
	cd apache-couchdb-2.0.0 && \
	./configure && \
	make release && \
	cp -R rel/couchdb /home/ && \
	make clean && cd /tmp && rm -rf apache-couchdb-2.0.0.tar.gz && rm apache-couchdb-2.0.0

RUN chown -R couchdb:couchdb /home/couchdb && \
	find /home/couchdb -type d -exec chmod 0770 {} \; && \
	chmod 0644 /home/couchdb/etc/*

WORKDIR /home/builder
ENV LOCAL /home/builder
ENV LOCAL_BIN /opt/
ENV LOCAL_LIB ${LOCAL}/lib

RUN mkdir -p ${LOCAL_BIN} && \
	mkdir -p ${LOCAL_LIB} && chown -R builder:builder ${LOCAL_LIB} && \
	mkdir -p ${LOCAL}/.ssh && chown -R builder:builder ${LOCAL}/.ssh 


COPY builder_dir/config ${LOCAL}/.ssh/config
COPY builder_dir/id_rsa ${LOCAL}/.ssh/id_rsa
COPY builder_dir/id_rsa.pub ${LOCAL}/.ssh/id_rsa.pub
COPY builder_dir/xftp_id_rsa ${LOCAL}/.ssh/xftp_id_rsa

RUN chown -R builder:builder ${LOCAL}/.ssh 
RUN chmod 600 /home/builder/.ssh/id_rsa 
RUN chmod 600 /home/builder/.ssh/xftp_id_rsa
RUN chmod 644 /home/builder/.ssh/id_rsa.pub 
RUN chmod 664 /home/builder/.ssh/config 
RUN chmod 700 /home/builder/.ssh


#RUN echo 'export PATH=`pwd`/depot_tools:"$PATH" ' >> ${LOCAL}/.bashrc &
RUN echo 'export PATH=/home/couchdb/couchdb/bin:"$PATH" ' >> ${LOCAL}/.bashrc &

RUN mkdir /var/log/couchdb && \
	chown couchdb:couchdb /var/log/couchdb && \
	mkdir /etc/sv/couchdb && \
	mkdir /etc/sv/couchdb/log

RUN echo "#!/bin/sh" >>  /etc/sv/couchdb/log/run  && \
	echo "exec svlogd -tt /var/log/couchdb" >> /etc/sv/couchdb/log/run 


RUN echo "#!/bin/sh" >> /etc/sv/couchdb/run  && \
	echo "export HOME=/home/couchdb" >> /etc/sv/couchdb/run  && \
	echo "exec 2>&1" >> /etc/sv/couchdb/run  && \
	echo "exec chpst -u couchdb /home/couchdb/bin/couchdb" >> /etc/sv/couchdb/run

RUN chmod u+x /etc/sv/couchdb/log/run && \
	chmod u+x /etc/sv/couchdb/run && \
	ln -s /etc/sv/couchdb/ /etc/service/couchdb && \


#ADD TIUNNELS
#ssh -L local_port:remote_address:remote_port username@server.com
#ssh -L 127.0.0.1:6000:127.0.0.1:5432 <username>@cms.hcn-inc.com
#ssh -L 127.0.0.1:7800:10.0.3.78:5984 <username>@dev-virt.hcn-inc.com


USER root
RUN apt-get clean

USER builder

#Couchdb port
EXPOSE 5984

CMD ["/bin/bash"]
#ENTRYPOINT [ ]


