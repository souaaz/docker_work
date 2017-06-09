import sys
import os
import logging 

import common_setup

'''
#1
    clone repo
    cd to repo
    git checkout -t origin/ANDNAV-512
#2
    git clone -b ANDNAV-512 gitlab:android-app-development/navigator.git
'''

#python checkout_repos.py build_dir all ANDNAV-512
def clone_repos(list_repos, branch=None):
    try:
        for i in list_repos:
            repo_to_clone = common_setup.git_tmplte.format ( common_setup.githost, str(i) )
            print (repo_to_clone)
            res = os.system( repo_to_clone )
            if branch != None:
                try:
                    #' git ls-remote --heads gitlab:android-app-development/navigator.git'
                    import commands
                    chk_branch_cmd = 'git ls-remote --heads {0}:android-app-development/{1}.git {2} | wc -l '.format ( common_setup.githost, str(i), branch )                   
                    chk_branch = commands.getstatusoutput( chk_branch_cmd )                            
                    #returns a tuple with the (return_value, output)                                                        
                    if chk_branch[0] == 0 and int(chk_branch[1]) > 0:     
                        os.chdir( str(i) )
                        res = os.system ('git checkout -t origin/{0}'.format( branch) )
                        print ( 'RETURN ---> ', res )
                        os.chdir( '..')
                except Exception as e:
                    print ( str (e) )                    

    except Exception as e:
        print ( str (e) )

def update_libs():
    try:
        cmd = "rsync {0}/{1} {2}/{3}".format (common_setup.local_dir_binaries, common_setup.xwalk_src, common_setup.proj_lib_dir, common_setup.xwalk_target )
        os.system ( cmd )

    except Exception as e:
        print ( str  (e) )


#checkout_repos <dir> <repo> <branch> 
#EXAMPLES
#python checkout_repos.py build_dir
#python checkout_repos.py build_dir all 
#python checkout_repos.py build_dir all ANDNAV-512
#python checkout_repos.py build_dir navigator ANDNAV-512

if __name__ == "__main__": 

    os.system("ssh -p 49152 -o StrictHostKeyChecking=no -o PasswordAuthentication=no builder-debug@gitlab.hcn-inc.com") 

    pkg = "all"
    branch = None
    build_path = "build_dir"

    if len (sys.argv) > 1:
        build_path = str(sys.argv[1])
    
    if len (sys.argv) > 2:
        pkg = str(sys.argv[2])

    if len (sys.argv) > 3:
        branch = str(sys.argv[3])

    init_dir = os.getcwd() 
    os.system( " mkdir -p {0}" .format (build_path))
    os.chdir(os.path.join(os.path.abspath(os.path.curdir), build_path ) )

    if pkg in [ "all", "ALL"]:
        clone_repos( common_setup.android_repos, branch=branch ) 
        update_libs()      
    else:
        if type(pkg) in [ unicode, str]:
            if pkg in common_setup.android_projects_to_build:
                idx = common_setup.android_projects_to_build.index(pkg)
        if pkg == "navigator":
            clone_repos( common_setup.android_repos[idx:], branch=branch)
            update_libs()
        else:
            clone_repos( common_setup.android_repos[idx:idx+1], branch=branch)
       
    os.chdir(init_dir)
