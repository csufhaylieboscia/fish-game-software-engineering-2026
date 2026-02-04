# Git Cheatsheet

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