# ctf-workspace-generator
Create file structure for ctfs/exams/pentests etc.

# Examples
```
chmod +x ctf_workspace_generator.py
./ctf_workspace_generator.py --ctfname 'mr robot' --platform thm
./ctf_workspace_generator.py --ctfname Lame,Trick,Stocker --platform htb
./ctf_workspace_generator.py --ctfname ms01,192.1.1.1,192.1.1.2 --platform oscp
``` 
![image](https://github.com/aslamadmani1337/ctf-workspace-generator/assets/35896884/d7859bdb-7c3a-4012-9a43-07bdeab4cb1c)



# Additionally, you can use --trgt to run set-trgt trgt1 <arg>
```
./ctf_workspace_generator --ctfname Lame,Trick,Stocker --platform htb --trgt 10.10.17.12
source ~/.zshrc
```
