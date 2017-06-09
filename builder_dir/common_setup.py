
githost = "gitlab"
out_path = "output_apk"

git_tmplte = "git clone {0}:android-app-development/{1}.git"
git_checkout_tmplte = "git clone -b {0} {1}:android-app-development/{2}.git"
local_dir_binaries="/home/builder/lib"

xwalk_src = "xwalk_shared_library-18.48.477.13-64bit.aar"
proj_lib_dir = "navigator/navigator/libs"
xwalk_target = "xwalk_shared_library-18.48.477.13-64bit.aar"


android_repos = [
    "adminservice", 
    "customkeyboard",  
    "hcnlauncher",  
    "ntp-service",
    "networkservice", 
    "navigator",
    "networkcontroller",
    "couchsync",
    "generalutils"
]

android_projects_to_build = [
    "adminservice", 
    "customkeyboard",  
    "hcnlauncher",  
    "ntp-service",
    "networkservice", 
    "navigator" 
    ]

android_apk_paths = [
    "app/build/outputs/apk/AdminService.apk",
    "app/build/outputs/apk/CustomKeyboard.apk",
    "launcher/build/outputs/apk/HCNLauncher.apk",
    "ntpservice/build/outputs/apk/NTPService.apk",
    "app/build/outputs/apk/NetworkService.apk",
    "navigator/build/outputs/apk/Navigator.apk",
]

android_apk_files = [
    "AdminService.apk",
    "CustomKeyboard.apk",
    "HCNLauncher.apk",
    "NTPService.apk",
    "NetworkService.apk",
    "Navigator.apk",
    ]

android_app_packages = [
    "com.hcn.adminservice", 
    "com.hcn.keyboard", 
    "com.hcn.launcher",
    "com.hcn.ntpservice", 
    "com.hcn.network_service"
    "com.hcn.navigator", 
    ]

android_app_type = [
    "system",
    "user",
    "system",
    "user",
    "user",
    "user"
]   
    