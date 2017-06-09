import sys
import os
import logging 

import common_setup

def build_apk( list_to_build,  build_version="assembleDebug"):
    save_dir = os.getcwd() #os.path.abspath(os.path.curdir)
    for idx, i in enumerate(list_to_build):
        try:
            os.chdir(os.path.join(os.path.abspath(os.path.curdir), str(i) ) )
            cmd = "gradle {0} " .format (build_version )
            if str(i) == "navigator":
                cmd += " -xnavigator:lintVitalRelease"
            res = os.system( cmd )

            print ( " Current dir {0}".format (os.getcwd() ) )
            
            
            print ( res ) 
            print ( os.getcwd())
            os.chdir(save_dir)
        except Exception as e:
            print ( str  (e) )

    os.chdir(save_dir)

def clean_apk( list_to_build, myfiles ):
    save_dir = os.getcwd() #os.path.abspath(os.path.curdir)
    for idx, i in enumerate(list_to_build):
        try:
            os.chdir(os.path.join(os.path.abspath(os.path.curdir), str(i) ) )
            cmd = "gradle clean"
            res = os.system( cmd )
            print ( res ) 
            # Check that APK was really erased
            fname = myfiles[idx]
            try:
                if os.path.isfile(fname) :
                    cmd = "rm -f %s " % ( fname )
                    os.system ( cmd )
            except Exception as e:
                print ( str(e) )


            print ( os.getcwd())
            os.chdir(save_dir)
        except Exception as e:
            print ( str  (e) )

    os.chdir(save_dir)

def check_output ( list_to_build, myfiles ) :
    res = 0
    save_dir = os.getcwd() #os.path.abspath(os.path.curdir)
    for idx, i in enumerate(list_to_build):
        try:
            os.chdir(os.path.join(os.path.abspath(os.path.curdir), str(i) ) )
            fname = myfiles[idx]
            if os.path.isfile(fname) :
                print ( 'OK. {0} was built'.format ( fname ) ) 
            else:
                print (' ERROR. Could not find {0}'.format ( fname ))
                res +=1

            os.chdir(save_dir)
        except Exception as e:
            print ( str  (e) )

    os.chdir(save_dir)
    return res == 0


def copy_output ( list_to_build, myfiles, outpath ) :
    res = 0
    save_dir = os.getcwd() #os.path.abspath(os.path.curdir)
    for idx, i in enumerate(list_to_build):
        try:
            fname = os.path.join(os.path.abspath(os.path.curdir), str(i), myfiles[idx] )            
            if os.path.isfile(fname) and os.path.isdir(outpath) :                           
                cmd = 'cp {0} {1}/'.format ( fname, outpath)
                os.system( cmd )
            else:               
                res +=1

            os.chdir(save_dir)
        except Exception as e:
            print ( str  (e) )

    os.chdir(save_dir)
    return res == 0


def install_apk(apk_dir, apk_file, package_name, app_type="user"):
    try:
        res = -1
        cmds = []
        sys_type = 0
        '''

        adb push output_apk/NetworkService.apk /data/local/tmp/com.hcn.network_service
        #adb shell pm install -r "/data/local/tmp/com.hcn.network_service"
        adb shell pm uninstall com.hcn.network_service
        adb shell pm install -r "/data/local/tmp/com.hcn.network_service"
        '''
        full_path_name = os.path.join (os.path.abspath(os.path.curdir), apk_dir, apk_file)  
        tmp_local_path = os.path.join ("/data/local/tmp/", package_name)

        #cmd = "sudo adb install -r {}".format (full_path_name)
        #res = os.system ( cmd )


        
        
        if app_type == "user":
            cmds.append ("sudo adb push {0} {1}".format (full_path_name, tmp_local_path) )
            cmds.append ( "sudo adb shell pm uninstall {}".format (package_name) )      
            cmds.append ( "sudo adb shell pm install -r {}".format (tmp_local_path ) )
        else:
            sys_type = 1
            cmds.append ("sudo adb push {0} {1}".format (full_path_name, "/sdcard/") )
            cmds.append ( "sudo adb shell " )
            adb_arg = "su -c " 
            ardb_c0 = "rmnt " 
            adb_c1 = "cp /system/priv-app/{0}/{1} /sdcard/{1}.bak".format (apk_file[:-4], apk_file, apk_file)
            adb_c2 = "cp /sdcard/{0} /system/priv-app/{1}/{2} ".format (apk_file, apk_file[:-4], apk_file)
            cmds.append(" exit")
            cmds.append ( " exit ")
        i=0 # num of errors
        for c in cmds:
            try:
                res = os.system ( c )
                if res == 0:
                    print ( "Successfully executed cmd {} ... ".format ( c) )
                else:
                    print ( "Error executing cmd {} ... ".format ( c) )
                    i +=1
            except Exception as e:
                print ( str  (e) )

        if i == 0:
            res = 0
            print ( "File loaded successfully on the device" )
            if sys_type == 1:
                os.system( "")
        else:
            print ( "Error loading the APK ... ")
    except Exception as e:
        print ( str  (e) )    

    return res

def sign_apk_jar(apk_file):
    try:
        key_location ='/home/builder/android-certs'
        jar_location = '/home/builder/android-certs'
       
        apk_signed = "".join( [apk_file[:-4], "-signed.apk"] )
                      
        cmd = "java -jar {0}/signapk.jar {1}/platform.x509.pem {2}/platform.pk8 {3} {4}".format( \
                        jar_location, key_location, key_location, apk_file, apk_signed)
        res = os.system ( cmd )

        print ( res)

    except Exception as e:
        print ( str (e) )


def build_sub(build_path, output_volume, pkg):
   
    
    projects_to_build = common_setup.android_projects_to_build[idx:idx+1]
    apk_paths = common_setup.android_apk_paths[idx:idx+1]
    apk_files = common_setup.android_apk_files[idx:idx+1]

    print ( ' apk_paths=', apk_paths)
    print ( 'projects_to_build ', projects_to_build)
    
    build_types=["assembleDebug", "assembleRelease" ]

    for bd in build_types:
        clean_apk(projects_to_build, apk_paths)
       
        build_apk(projects_to_build, build_version=bd)
        res = check_output( projects_to_build, apk_paths)
    
        print ("  check_output returned {0}".format ( res ))
        if res is True:
            subdir = "debug" if bd == "assembleDebug" else "release"
            tgt_dir = os.path.join (os.path.abspath(os.path.curdir), common_setup.out_path, subdir) 
            os.system( " mkdir -p {0}" .format (tgt_dir))
            print (" copy to {0}".format ( tgt_dir))
            res = copy_output(projects_to_build,apk_paths, tgt_dir)
            if res is True:
                for i in apk_files: 
                    p =  os.path.join ( tgt_dir, i)
                    if os.path.isfile(p):
                        sign_apk_jar(p)
        if res:                        
            print ('SUCCESS')
        else:
            print('FAILURE')     
           
        if res:  
            if os.path.isdir(output_volume):
                os.system("cp -r {0}/* {1}".format ( common_setup.out_path, output_volume))
 

def build_all(build_path, output_volume ):
    build_types=["assembleDebug", "assembleRelease" ]
    for bd in build_types:
        clean_apk(common_setup.android_projects_to_build, common_setup.android_apk_paths)     
       
        build_apk(common_setup.android_projects_to_build, build_version=bd)
        res = check_output( common_setup.android_projects_to_build, common_setup.android_apk_paths)
    
        print ("  check_output returned {0}".format ( res ))
        if res is True:
            subdir = "debug" if bd == "assembleDebug" else "release"
            tgt_dir = os.path.join (os.path.abspath(os.path.curdir), common_setup.out_path, subdir) 
            os.system( " mkdir -p {0}" .format (tgt_dir))
            print (" copy to {0}".format ( tgt_dir))
            res = copy_output(common_setup.android_projects_to_build, common_setup.android_apk_paths, tgt_dir)
            if res is True:
                for i in common_setup.android_apk_files: 
                    p =  os.path.join ( tgt_dir, i)
                    if os.path.isfile(p):
                        sign_apk_jar(p)
        if res:                        
            print ('SUCCESS')
        else:
            print('FAILURE')     
           

    if res:  
        if os.path.isdir(output_volume):
            os.system("cp -r {0}/* {1}".format ( common_setup.out_path, output_volume))
 
#python build_apk.py build_dir /android_binaries all
if __name__ == "__main__": 

    os.system("ssh -p 49152 -o StrictHostKeyChecking=no -o PasswordAuthentication=no builder-debug@gitlab.hcn-inc.com") 

    pkg = "all"

    if len (sys.argv) > 1:
        build_path = str(sys.argv[1])
    
    if len (sys.argv) > 2:
        output_volume = str(sys.argv[2])
    else:
        output_volume = "/android_binaries"


    if len (sys.argv) > 3:
        pkg = str(sys.argv[3])


    init_dir = os.getcwd() 
    

    os.system( " mkdir -p {0}" .format (build_path))
    os.chdir(os.path.join(os.path.abspath(os.path.curdir), build_path ) )

    out_path = common_setup.out_path
    os.system( " mkdir -p {0}" .format (out_path))  
    os.system( " mkdir -p {0}/debug" .format (out_path))
    os.system( " mkdir -p {0}/release" .format (out_path))

    os.system( " rm -f {0}/release/*" .format (out_path))
    os.system( " rm -f {0}/debug/*" .format (out_path))

    if pkg in [ "all", "ALL"]:
        build_all( build_path ,  output_volume )
    else:
        build_sub( build_path ,  output_volume , pkg)

    os.chdir(init_dir)
