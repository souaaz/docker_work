FROM alpine:latest

LABEL Maintainer Samira Ouaaz "souaaz@hcn-inc.com"


RUN apk update 
RUN apk add --update openjdk7  
#RUN apk add --update libstdc++6 libz1 sudo python git nano wget unzip 
RUN apk add --update sudo python git nano wget unzip bash openssh

RUN addgroup sudo && addgroup builder 
RUN adduser -s /bin/bash -D builder -G sudo && \
    echo 'builder:builder' | sudo chpasswd

WORKDIR /home/builder
ENV LOCAL /home/builder
ENV LOCAL_BIN /opt/
ENV LOCAL_LIB /opt/lib
ENV ANDROID_CERTS_DIR ${LOCAL}/android-certs

RUN mkdir -p ${LOCAL_BIN} &&  mkdir -p /usr/lib/jvm && mkdir -p ${LOCAL_LIB}
RUN mkdir -p ${LOCAL}/.ssh && chown -R builder:builder ${LOCAL}/.ssh 
RUN mkdir -p ${ANDROID_CERTS_DIR}

COPY builder_dir/config ${LOCAL}/.ssh/config
COPY builder_dir/id_rsa ${LOCAL}/.ssh/id_rsa
COPY builder_dir/id_rsa.pub ${LOCAL}/.ssh/id_rsa.pub

RUN chown -R builder:builder ${LOCAL} 
RUN chown -R builder:builder ${LOCAL}/.ssh 
RUN chmod 600 /home/builder/.ssh/id_rsa 
RUN chmod 644 /home/builder/.ssh/id_rsa.pub 
RUN chmod 664 /home/builder/.ssh/config 
RUN chmod 700 /home/builder/.ssh

ENV TARGET_JAVA_DIR /usr/lib/jvm
ENV JAVA_ROOT_DIR jdk1.7.0_79
ENV JAVA_BINARY jdk-7u79-linux-x64.tar.gz
ENV JAVA_HOME ${TARGET_JAVA_DIR}/${JAVA_ROOT_DIR}
 

ENV GRADLE ${LOCAL_BIN}/gradle-2.14.1
ENV GRADLE_BINARY gradle-2.14.1-bin.zip

COPY builder_dir/${GRADLE_BINARY} ${LOCAL_BIN}/${GRADLE_BINARY}
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


COPY builder_dir/build.sh ${LOCAL}/build.sh
COPY builder_dir/build_apk.py ${LOCAL}/build_apk.py


COPY builder_dir/xwalk_shared_library-64bit.aar ${LOCAL_LIB}/xwalk_shared_library-18.48.477.13-64bit.aar
#rsync release@10.0.254.107://storage/third-party/crosswalk/xwalk_shared_library-64bit/18.48.477.13/xwalk_shared_library-64bit.aar


#Signature keys for Android
#rsync release@xftp://storage/android-certs/* builder_dir/android-certs/
#rsync /storage/deployment/os-build-tools/0.1.0.3/Archos/Resign-FW/signapk.jar builder_dir/

COPY builder_dir/signapk.jar ${ANDROID_CERTS_DIR}/
COPY builder_dir/android-certs/platform.x509.pem ${ANDROID_CERTS_DIR}/
COPY builder_dir/android-certs/platform.pk8 ${ANDROID_CERTS_DIR}/


USER root

USER builder

CMD ["/bin/bash"]
#ENTRYPOINT ["/bin/bash", "build.sh"]
#ENTRYPOINT [ "/usr/bin/python",  "build_apk.py", "build_dir" , "/android_binaries"]


