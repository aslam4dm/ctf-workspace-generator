#!/usr/bin/python3

import os
import argparse
from colorama import Fore, Style
from tqdm import tqdm
import time

def create_directory_structure(base_path, platform, ctf_names):
    directory_structure = {
        "thm": ["Enumeration", os.path.join("Enumeration", "Autorecon"), "Loot", "Exploit", "Report", "Downloaded_Files", "Notes"],
        "htb": ["Enumeration", os.path.join("Enumeration", "Autorecon"), "Loot", "Exploit", "Report", "Downloaded_Files", "Notes"],
        "pgp": ["Enumeration", os.path.join("Enumeration", "Autorecon"), "Loot", "Exploit", "Report", "Downloaded_Files", "Notes"],
        "vh": ["Enumeration", os.path.join("Enumeration", "Autorecon"), "Loot", "Exploit", "Report", "Downloaded_Files", "Notes"],
        "oscp": ["Enumeration", os.path.join("Enumeration", "Autorecon"), "Loot", "Exploit", "Report", "Downloaded_Files", "Notes"],
        "other": ["Enumeration", os.path.join("Enumeration", "Autorecon"), "Loot", "Exploit", "Report", "Downloaded_Files", "Notes"]
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

def set_target(target):
    print(f"{Fore.CYAN}Setting target. Make sure to run `source /home/{os.getlogin()}/.zshrc` once completed.{Style.RESET_ALL}")
    time.sleep(1.5)
    os.system(f"set-target trgt1 {target}")
    #os.system("/bin/zsh -c 'source /home/{os.getlogin()}/.zshrc'")

def main():
    parser = argparse.ArgumentParser(description="Create directory structure based on arguments.")
    parser.add_argument("--ctfname", metavar="<CTFName>", help="CTF names separated by comma", required=True)
    parser.add_argument("--platform", metavar="<Platform>", choices=['thm', 'htb', 'pgp', 'vh', 'oscp', 'other'], help="Platform type", required=True)
    parser.add_argument("--trgt", metavar="<Target>", help="Target IP address")
    args = parser.parse_args()

    ctf_names = [name.strip() for name in args.ctfname.split(',')]
    base_path = f"/home/{os.getlogin()}/Documents/"
    platform_path = create_directory_structure(base_path, args.platform, ctf_names)

    if args.trgt:
        set_target(args.trgt)
        #print(f"{Fore.GREEN}Target set to: {args.trgt}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
