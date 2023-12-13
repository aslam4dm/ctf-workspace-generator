# Install
```
git clone https://github.com/aslam4dm/ctf-workspace-generator.git
pip install -r requirements.txt
chmod +x ctf_workspace_generator.py
sudo cp ctf_workspace_generator.py /bin/ctf_workspace_generator 
```
# ctf-workspace-generator
Create file structure for ctfs/exams/pentests etc.
Note, this tool will create the file structure under the /home/<user>/Documents directory.
```
ctf_workspace_generator --ctfname <name(s)> --platform <name>
```
# Examples
```
ctf_workspace_generator --ctfname 'mr robot' --platform thm
ctf_workspace_generator --ctfname Lame,Trick,Stocker --platform htb
ctf_workspace_generator --ctfname ms01,192.1.1.1,192.1.1.2 --platform oscp
``` 
![image](https://github.com/aslamadmani1337/ctf-workspace-generator/assets/35896884/d7859bdb-7c3a-4012-9a43-07bdeab4cb1c)



# Additionally, you can use --trgt to run set-trgt trgt1 <arg>
Note: to use this, you will need to have the set-target tool configured. See https://github.com/aslamadmani1337/set-target
```
./ctf_workspace_generator --ctfname Lame,Trick,Stocker --platform htb --trgt1 10.10.17.12
source ~/.zshrc
```

# Perform Connectivity Scans on your $trgt Env Targets
```
./ctf_workspace_generator --trgt1 10.88.100.101 --trgt2 10.88.100.43
source /home/<user>/.zshrc
./ctf_workspace_generator --ctfname ms01,ms02 --platform oscp --scan-trgt1 --scan-trgt2
```
