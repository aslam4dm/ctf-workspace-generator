#!/usr/bin/env python

import os
import argparse
from colorama import Fore, Style
from tqdm import tqdm
import time
import sys
import subprocess
from set_target import set_target

def create_directory_structure(base_path, platform, ctf_names):
    directory_structure = {
        "thm": ["Enumeration", os.path.join("Enumeration", "Autorecon"), "Loot", "Exploit", "Report", "Downloaded_Files", "Notes"],
        "htb": ["Enumeration", os.path.join("Enumeration", "Autorecon"), "Loot", "Exploit", "Report", "Downloaded_Files", "Notes"],
        "pgp": ["Enumeration", os.path.join("Enumeration", "Autorecon"), "Loot", "Exploit", "Report", "Downloaded_Files", "Notes"],
        "vh": ["Enumeration", os.path.join("Enumeration", "Autorecon"), "Loot", "Exploit", "Report", "Downloaded_Files", "Notes"],
        "other": ["Enumeration", os.path.join("Enumeration", "Autorecon"), "Loot", "Exploit", "Report", "Downloaded_Files", "Notes"],
        "oscp": ["Enumeration", os.path.join("Enumeration", "Autorecon"), "Loot", "Exploit", "Report", "Downloaded_Files", "Notes"],
        "bscp": ["Enumeration", os.path.join("Enumeration", "Autorecon"), "Loot", "Exploit", "Report", "Downloaded_Files", "Notes"]
    }

    for ctf_name in ctf_names:
        platform_path = os.path.join(base_path, platform, ctf_name)

        # Check if the directory already exists
        if os.path.exists(platform_path):
            print(f"{Fore.RED}Directory '{platform_path}' already exists.{Style.RESET_ALL}")
            overwrite = input("Do you want to overwrite it? (yes/no): ").lower()
            if overwrite != 'yes':
                print(f"{Fore.RED}Operation cancelled for {ctf_name}. Skipping...{Style.RESET_ALL}")
                continue

        created_directories = []
        with tqdm(total=len(directory_structure[platform]), desc=f"Creating Directories for {ctf_name}", ncols=100) as pbar:
            for directory in directory_structure[platform]:
                directory_path = os.path.join(platform_path, directory)
                os.makedirs(directory_path, exist_ok=True)
                created_directories.append(directory_path)
                time.sleep(0.3)  # 2-second delay between directory creations
                pbar.update(1)

        print(f"{Fore.GREEN}Directories created for {ctf_name} under {platform}:{Style.RESET_ALL}")
        for path in created_directories:
            print(f"Created: {path}")

        print(f"{Fore.GREEN}Directory structure created for {ctf_name} under {platform}!{Style.RESET_ALL}")

    return platform_path

def set_targets(targets, rc):
    trgts = {}
    for key, target in targets.items():
        trgts[key] = target
        set_target({key}, {target}, {rc})
        # os.system(f"set-target {key} {target}")
    return trgts

def perform_ping_scan(targets):
    # When --trgtX is specified in the argument as well as --scan-trgtX
    if isinstance(targets, str):
        target = targets
        print(f"{Fore.CYAN}Connectivity scans will be performed against the following:{Style.RESET_ALL} {Style.BRIGHT + Fore.MAGENTA}{target}{Style.RESET_ALL} {Fore.RED}CTRL-C now to stop.{Style.RESET_ALL}")
        countdown_func(3)
        print(f"{Style.BRIGHT + Fore.CYAN}\nConnectivity check for: {target}{Style.RESET_ALL}")
        # connectivity check
        con_scan(target)
        
    elif isinstance(targets, list):
        converted = []
        for t in targets:
            try: converted.append(os.getenv(t))
            except: pass
        
        print(f"{Fore.CYAN}Connectivity scans will be performed against the following:{Style.RESET_ALL} {Style.BRIGHT + Fore.MAGENTA}{converted}{Style.RESET_ALL} {Fore.RED}CTRL-C now to stop.{Style.RESET_ALL}")
        countdown_func(3)
        for target in targets:
            print(f"{Style.BRIGHT + Fore.CYAN}\nConnectivity check for: {os.getenv(target)}{Style.RESET_ALL}")
            # connectivity check
            con_scan(target, True)

# Scan function - runs connectivity scans on target
def con_scan(t, env=False):
    if env == False:
        # perform ping scan
        #type_text(f"$timeout 4 ping -c 4 {t}")
        #os.system(f"timeout 4 ping -c 4 {t}")
        #subprocess.run(['timeout', '4', 'ping', '-c', '4', t])    

        # self reverse lookup
        type_text(f"timeout 5 dig -p 53 -x {t} @{t}")
        os.system(f"timeout 5 dig -p 53 -x {t} @{t}")
        
        # perform a check against 4 common ports
        type_text(f"$nc -zv ${t} <22> <53> <80> <445>")
        os.system(f"timeout 3 nc -zv {t} 22")
        os.system(f"timeout 3 nc -zv {t} 53")
        os.system(f"timeout 3 nc -zv {t} 80")
        os.system(f"timeout 3 nc -zv {t} 445")
        
        # dns reverse lookups
        type_text(f"timeout 4 dig -x {t} +short")
        rev = subprocess.run(f"timeout 4 dig -x {t} +short", shell=True, capture_output=True, text=True).stdout.strip()
        time.sleep(1)
        print(rev)
        # self reverse lookup
        type_text(f"timeout 4 dig -x {t} @{t} +short")
        self_rev = subprocess.run(f"timeout 4 dig -x {t} @{t} +short",shell=True, capture_output=True, text=True).stdout.strip()
        time.sleep(1)
        print(self_rev)
        #self_rev = rev.stdout.strip()
        
        # Add records to /etc/hosts file???
        if rev and self_rev:
            #print("note: A reverse DNS lookup using dig -x will attempt to find the PTR record associated with that IP, which might not always provide a meaningful or recognizable domain name. It might return something like lhr35s02-in-f3.1e100.net. This is a reverse DNS entry associated with that IP address")
            None 
        elif rev and not self_rev:
            None
        elif self_rev and not rev:
            None
            
            
    elif env == True:
        type_text(f"$timeout 4 ping -c 4 ${t}")
        os.system(f"timeout 4 ping -c 4 ${t}")
        
        # perform a check against 4 common ports
        type_text(f"$timeout 3 nc -zv ${t} <22> <53> <80> <445>")
        os.system(f"timeout 3 nc -zv ${t} 22")
        os.system(f"timeout 3 nc -zv ${t} 53")
        os.system(f"timeout 3 nc -zv ${t} 80")
        os.system(f"timeout 3 nc -zv ${t} 445")
        
        # dns reverse lookups
        type_text(f"timeout 4 dig -x ${t} +short")
        rev = subprocess.run(f"timeout 4 dig -x ${t} +short", shell=True, capture_output=True, text=True).stdout.strip()
        time.sleep(1)
        print(rev)
        # self reverse lookup
        type_text(f"timeout 4 dig -x {t} @${t} +short")
        self_rev = subprocess.run(f"timeout 4 dig -x ${t} @${t} +short",shell=True, capture_output=True, text=True).stdout.strip()
        time.sleep(1)
        print(self_rev)
        #self_rev = rev.stdout.strip()
        
        # Add records to /etc/hosts file???
        if rev and self_rev:
            #print("note: A reverse DNS lookup using dig -x will attempt to find the PTR record associated with that IP, which might not always provide a meaningful or recognizable domain name. It might return something like lhr35s02-in-f3.1e100.net. This is a reverse DNS entry associated with that IP address")
            None 
        elif rev and not self_rev:
            None
        elif self_rev and not rev:
            None

def connect_to_vpn(vpn_path):
    # Continue code from here
    os.system(f"sudo openvpn {vpn_path}")
    return 0

# Countdown function
def countdown_func(t):
    try:
        for i in range(t, -1, -1):
            sys.stdout.write("\r{} ".format(i))  # \r moves the cursor back to the start of the line
            sys.stdout.flush()  # Flush the output to show the countdown immediately
            time.sleep(1)  # Wait for 1 second
        sys.stdout.write("\r{} ".format(''))
        sys.stdout.flush()             
    except KeyboardInterrupt:
        print(f"{Fore.CYAN}\nNote: `source /home/{os.getlogin()}/.zshrc` to update the session's env.{Style.RESET_ALL}\n{Fore.RED}Exiting, Goodbye!{Style.RESET_ALL}")
        exit(0)

# cool function that makes it look like text is being typed
def type_text(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()  # Flush the output to display the character immediately
        time.sleep(0.06)  # Adjust the sleep duration to change typing speed
    print()  # Move to the next line after typing is complete

def main():
    parser = argparse.ArgumentParser(description="Create directory structure based on arguments.")
    parser.add_argument("--ctfname", metavar="<CTFName>", help="CTF names separated by comma")
    parser.add_argument("--platform", metavar="<Platform type (thm/htb/pgp/vh/oscp/other/bscp)>", choices=['thm', 'htb', 'pgp', 'vh', 'oscp', 'other', 'bscp'], help="Platform type")
    parser.add_argument("--trgt1", metavar="<Target1>", help="Target 1")
    parser.add_argument("--trgt2", metavar="<Target2>", help="Target 2")
    parser.add_argument("--trgt3", metavar="<Target3>", help="Target 3")
    parser.add_argument("--trgt4", metavar="<Target4>", help="Target 4")
    parser.add_argument("--trgt5", metavar="<Target5>", help="Target 5")
    parser.add_argument("--trgtdc", metavar="<TargetDC>", help="Target Data Center")
    parser.add_argument("--scan-trgt1", action="store_true", help="Perform ping scan for Target 1")
    parser.add_argument("--scan-trgt2", action="store_true", help="Perform ping scan for Target 2")
    parser.add_argument("--scan-trgt3", action="store_true", help="Perform ping scan for Target 3")
    parser.add_argument("--scan-trgt4", action="store_true", help="Perform ping scan for Target 4")
    parser.add_argument("--scan-trgt5", action="store_true", help="Perform ping scan for Target 5")
    parser.add_argument("--scan-trgtdc", action="store_true", help="Perform ping scan for Target Data Center")
    parser.add_argument("--set-vpn", metavar="Path to vpn file", help="Path to vpn file")
    parser.add_argument("--rc", metavar="shell profile", help="shell profile <bash>/<zsh>")
    args = parser.parse_args()

    ctf_names = [name.strip() for name in (args.ctfname.split(',') if args.ctfname else [])]
    base_path = f"/home/{os.getlogin()}/Documents/"
    platform = args.platform if args.platform else None

    if ctf_names and not platform:
        parser.error("--platform is required when using --ctfname")

    if ctf_names and platform:
        platform_path = create_directory_structure(base_path, platform, ctf_names)

    targets = {
        "trgt1": args.trgt1,
        "trgt2": args.trgt2,
        "trgt3": args.trgt3,
        "trgt4": args.trgt4,
        "trgt5": args.trgt5,
        "trgtdc": args.trgtdc
    }

    valid_targets = {key: value for key, value in targets.items() if value is not None}
    trgts = None
    if valid_targets:
        if rc in ['zsh', 'ZSH', 'zSh', 'bash', 'Bash', 'BASH']:
            trgts = set_targets(valid_targets, rc.lower())
        else:
            # defaults to '.bashrc'
            trgts = set_targets(valid_targets, "bash")
            
    scan_targets = {
        "trgt1": args.scan_trgt1,
        "trgt2": args.scan_trgt2,
        "trgt3": args.scan_trgt3,
        "trgt4": args.scan_trgt4,
        "trgt5": args.scan_trgt5,
        "trgtdc": args.scan_trgtdc
    }

    valid_scan_targets = [target for target, should_scan in scan_targets.items() if should_scan]
    
    if valid_scan_targets:
        #if len(valid_scan_targets) > 1:
        # when --trgtX and --scan-trgtX are specified
        if len(valid_scan_targets)>=1 and trgts != None:
            # Loop through keys returned from set_targets() function and see if they match keys specified in valid_scan_targets
            for k,t in trgts.items():
                for vst in valid_scan_targets:
                    # if there is a match, perform a scan based on the newly set trgt e.g. --trgtX 10.10.10.10 --scan-trgtX means - perform scan on 10.10.10.10
                    if k == vst:
                    # invoke function with single target 'string'
                        perform_ping_scan(t)
                        # remove the specific trgtX from the valid_scan_targets list
                        valid_scan_targets.remove(f"{k}")
            # once completed set trgts to default None. So that a fair check occurs for the next sequence of code
            trgts = None
        
        # Perform scan by invoking $trgtX environment variable
        if len(valid_scan_targets)>=1 and trgts == None:
            # invoke function passing in the list
            perform_ping_scan(valid_scan_targets)

    if args.set_vpn:
        connect_to_vpn(args.set_vpn)
        
if __name__ == "__main__":
    main()
