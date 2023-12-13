# ctf-workspace-generator
Create file structure for ctfs/exams/pentests etc.

# Examples
`./ctf_workspace_generator` --ctfname 'mr robot' --platform thm
`./ctf_workspace_generator --ctfname Lame,Trick,Stocker --platform htb`
`./ctf_workspace_generator --ctfname ms01,192.1.1.1,192.1.1.2` --platform oscp` 


# Additionally, you can use --trgt to run set-trgt trgt1 <arg>
```
./ctf_workspace_generator --ctfname Lame,Trick,Stocker --platform htb --trgt 10.10.17.12
source ~/.zshrc
```
