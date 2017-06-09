FROM ubuntu:16.04

LABEL Maintainer Samira Ouaaz "souaaz@hcn-inc.com"

RUN apt-get update 
#RUN apt-get install -y --fix-missing software-properties-common python-software-properties#


RUN apt-get install -y apt-utils lib32stdc++6 lib32z1 sudo python git nano wget unzip 
RUN apt-get install -y  software-properties-common
RUN add-apt-repository -y ppa:openjdk-r/ppa 
RUN apt-get update 
RUN apt-get install -y openjdk-7-jdk  

RUN useradd -ms /bin/bash builder && \
    usermod -aG sudo builder && \
    echo 'builder:builder' | sudo chpasswd

WORKDIR /home/builder
ENV LOCAL /home/builder
ENV LOCAL_BIN /opt/
ENV LOCAL_LIB ${LOCAL}/lib
ENV ANDROID_CERTS_DIR ${LOCAL}/android-certs

RUN mkdir -p ${LOCAL_BIN} &&  mkdir -p /usr/lib/jvm && \
	mkdir -p ${LOCAL_LIB} && chown -R builder:builder ${LOCAL_LIB} && \
	mkdir -p ${LOCAL}/.ssh && chown -R builder:builder ${LOCAL}/.ssh && \
	mkdir -p ${ANDROID_CERTS_DIR} && chown -R builder:builder ${ANDROID_CERTS_DIR}

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

ENV GRADLE ${LOCAL_BIN}/gradle-2.14.1
ENV GRADLE_BINARY gradle-2.14.1-bin.zip

#Replace with : https://services.gradle.org/distributions/${GRADLE_BINARY}
#COPY builder_dir/${GRADLE_BINARY} ${LOCAL_BIN}/${GRADLE_BINARY}
RUN cd ${LOCAL_BIN} && \
	wget --output-document=${GRADLE_BINARY} --quiet https://services.gradle.org/distributions/${GRADLE_BINARY}
ENV GRADLE_HOME ${GRADLE}
ENV PATH ${PATH}:${GRADLE_HOME}/bin
RUN unzip ${LOCAL_BIN}/${GRADLE_BINARY} -d ${LOCAL_BIN} && rm -f ${LOCAL_BIN}/${GRADLE_BINARY}

ENV ANDROID_HOME /opt/android-sdk-linux

RUN cd /opt && wget --output-document=android-sdk.tgz --quiet https://dl.google.com/android/android-sdk_r24.4.1-linux.tgz && \
  tar xzf android-sdk.tgz && \
  chown -R root.root android-sdk-linux  && \
  rm -f android-sdk.tgz && \
 ( /bin/sleep 3 && while [ 1 ]; do /bin/sleep 1; echo y; done ) | ${ANDROID_HOME}/tools/android update sdk --all --no-ui --filter platform-tools,tools  && \
(/bin/sleep 3 && while [ 1 ]; do /bin/sleep 1; echo y; done ) | ${ANDROID_HOME}/tools/android update sdk --all --no-ui --filter platform-tools,tools,android-17,android-21,android-22,android-23,build-tools-21.1.2,build-tools-23.0.0,build-tools-23.0.1,build-tools-23.0.2,build-tools-23.0.3,addon-google_apis_x86-google-21,extra-android-support,extra-android-m2repository,extra-google-m2repository,extra-google-google_play_services

ENV PATH ${PATH}:${ANDROID_HOME}/tools:${ANDROID_HOME}/platform-tools


USER builder

COPY builder_dir/build_apk.py ${LOCAL}/build_apk.py
COPY builder_dir/common_setup.py ${LOCAL}/common_setup.py
COPY builder_dir/checkout_repos.py ${LOCAL}/checkout_repos.py

COPY builder_dir/copy_files.sh ${LOCAL}/copy_files.sh

#COPY builder_dir/xwalk_shared_library-64bit.aar ${LOCAL_LIB}/xwalk_shared_library-18.48.477.13-64bit.aar
#RUN rsync release@10.0.254.107://storage/third-party/crosswalk/xwalk_shared_library-64bit/18.48.477.13/xwalk_shared_library-64bit.aar ${LOCAL_LIB}/xwalk_shared_library-18.48.477.13-64bit.aar

#RUN scp -i ${LOCAL}/.ssh/xftp_id_rsa release@10.0.254.107://storage/third-party/crosswalk/xwalk_shared_library-64bit/18.48.477.13/xwalk_shared_library-64bit.aar ${LOCAL_LIB}/xwalk_shared_library-18.48.477.13-64bit.aar

USER root
RUN apt-get clean

USER builder

CMD ["/bin/bash"]
#ENTRYPOINT [ "/usr/bin/python",  "build_apk.py", "build_dir" , "/android_binaries"]


