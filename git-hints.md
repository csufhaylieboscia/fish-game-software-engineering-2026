# Git Cheatsheet

## Committing changes

* save file working on
* pull changes if others are currently working
```bash
git pull
```
* add the file of what the changes were on
```bash
# add specific file with filename
git add filename

# add all files
git add .
```
* Make a comment on what has been changed
```bash
git commit -m "comment of whats changed"
```
* push changes
```bash
git push 
```
## git clone
 1. In Github click the code button and copy either the https or SSH link
2. Go to terminal, in file location where project will reside
3. On command line enter `git clone copiedLink`
4. enter `git status` to ensure that repository is up to date
5. if not up to date use `git pull` to receive new changes

## Set Up Git config

Basic User information:
```bash 
git config --global user.name "Your Name"
git config --global user.email "Your email"
```

Verify Config 
```bash
git config --list
```

## Creating an SSH key for password-less 

* travel down to your computers home directory and generate a new key with you github email
```bash
ssh-kegen -t ed25519 -c "yourgithubemail@git.com"
```
* It will prompt you, just hit enter
* Travel into the .shh directory to find your newly created keys and also view them
```bash
cd .shh
ls -la
```
* you should have see `id_ed25519` and `id_ed25519.pub`
* DO NOT share `id_ed25519` this is your personal key
* Print out `id_ed25519.pub` your public key to copy and place in github, Copy the whole line that is printed out
```bash
cat id_ed25519.pub
```
* Travel to your git hub settings > SSH and GPG keys > New SSH key > and paste your key and give it a name > add SSH key
