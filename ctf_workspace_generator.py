#!/usr/bin/env python

import os
import argparse
from colorama import Fore, Style
from tqdm import tqdm
import time
import sys

def create_directory_structure(base_path, platform, ctf_names):
    directory_structure = {
        "thm": ["Enumeration", os.path.join("Enumeration", "Autorecon"), "Loot", "Exploit", "Downloaded_Files", "Notes"],
        "htb": ["Enumeration", os.path.join("Enumeration", "Autorecon"), "Exploit", "Report", "Downloaded_Files"],
        "pgp": ["Enumeration", os.path.join("Enumeration", "Autorecon"), "Exploit", "Downloaded_Files"],
        "vh": ["Enumeration", os.path.join("Enumeration", "Autorecon"), "Loot", "Exploit", "Downloaded_Files"]
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
                time.sleep(0.2)  # 2-second delay between directory creations
                pbar.update(1)

        print(f"{Fore.GREEN}Directories created for {ctf_name} under {platform}:{Style.RESET_ALL}")
        for path in created_directories:
            print(f"Created: {path}")

        print(f"{Fore.GREEN}Directory structure created for {ctf_name} under {platform}!{Style.RESET_ALL}")

    return platform_path

def set_targets(targets):
    for key, target in targets.items():
        os.system(f"set-target {key} {target}")

def perform_ping_scan(targets):
    converted = []
    for t in targets:
        try: converted.append(os.getenv(t))
        except: pass
    try:
        print(f"{Fore.CYAN}Connectivity scans will be performed against the following:{Style.RESET_ALL} {Style.BRIGHT + Fore.MAGENTA}{converted}{Style.RESET_ALL} {Fore.RED}CTRL-C now to stop.{Style.RESET_ALL}")
        # countdown
        for i in range(10, 0, -1):
            sys.stdout.write("\r{} ".format(i))  # \r moves the cursor back to the start of the line
            sys.stdout.flush()  # Flush the output to show the countdown immediately
            time.sleep(1)  # Wait for 1 second
            
    except KeyboardInterrupt:
        print(f"{Fore.CYAN}\nNote: `source /home/{os.getlogin()}/.zshrc` to update the session's env.{Style.RESET_ALL}\n{Fore.RED}Exiting, Goodbye!{Style.RESET_ALL}")
        exit(0)
                
    for target in targets:
        print(f"{Style.BRIGHT + Fore.CYAN}\nConnectivity check for: {os.getenv(target)}{Style.RESET_ALL}")
        # connectivity check
        type_text(f"$ping -c 4 ${target}")
        os.system(f"timeout 5 ping -c 4 ${target}")
        
        # perform a check against 4 common ports
        type_text(f"nc -zv ${target} <22> <53> <80> <445>")
        os.system(f"timeout 3 nc -zv ${target} 22")
        os.system(f"timeout 3 nc -zv ${target} 53")
        os.system(f"timeout 3 nc -zv ${target} 80")
        os.system(f"timeout 3 nc -zv ${target} 445")

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
    parser.add_argument("--platform", metavar="<Platform>", choices=['thm', 'htb', 'pgp', 'vh'], help="Platform type")
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

    if valid_targets:
        set_targets(valid_targets)

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
        perform_ping_scan(valid_scan_targets)

if __name__ == "__main__":
    main()
