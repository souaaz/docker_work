#! /bin/bash

#Add gitlab host to known_hosts
ssh -p 49152 -o StrictHostKeyChecking=no -o PasswordAuthentication=no builder-debug@gitlab.hcn-inc.com

ssh  -o StrictHostKeyChecking=no -o PasswordAuthentication=no release@10.0.254.107

scp -i ~/.ssh/xftp_id_rsa release@10.0.254.107://storage/third-party/crosswalk/xwalk_shared_library-64bit/18.48.477.13/xwalk_shared_library-64bit.aar /home/builder/lib/xwalk_shared_library-18.48.477.13-64bit.aar 

scp -i ~/.ssh/xftp_id_rsa release@10.0.254.107://storage/android-certs/platform.x509.pem   /home/builder/android-certs
scp -i ~/.ssh/xftp_id_rsa release@10.0.254.107://storage/android-certs/platform.pk8  /home/builder/android-certs
scp -i ~/.ssh/xftp_id_rsa release@10.0.254.107://storage/deployment/os-build-tools/0.1.0.3/Archos/Resign-FW/signapk.jar   /home/builder/android-certs
