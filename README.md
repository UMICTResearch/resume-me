# resume-me

#### Beta [![Deployment status from DeployBot](https://sig.deploybot.com/badge/88313865989649/37135.svg)](http://deploybot.com)

#### Test [![Deployment status from DeployBot](https://sig.deploybot.com/badge/02267417997177/37757.svg)](http://deploybot.com)

## Table of Contents
1. [Coding Standards](#coding-standards)
2. [Installation Instructions](#installation-instructions)
3. [Run the application on your local system](#run the application on your local system)
4. [Code Push](#code-push)

##Coding Standards
- Strictly follow PEP8 coding standards
  - You can install pep8 checkers (https://pypi.python.org/pypi/pep8):
    - Linux (Ubuntu) - sudo apt-get install pep8 python-autopep8
    - OR simply using pip - pip install pep8
- Use the editorconfig file with preferred IDE for consistency

##Installation Instructions

####Mongodb
Ubuntu official repository can be used for installing mongodb but it is advised to install the latest version using the following method.

1. Adding key to validate new mongodb sources
````$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10````
2. Adding links to repository for installing latest mongodb
````echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list````
3. Update software sources
````sudo apt-get update````
4. Install Mongodb
````sudo apt-get install -y mongodb-org````
5. Check status
````service mongod status````

For installation on Macs, you can use the following method.

1. If you don’t already have a package installer, install one. Homebrew is one example
````$ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" ````
2. If you already have Homebrew, update it
````$brew update````
3. Now install mongodb (the last line of the install output shows you the install location, which you should add to your ~/.bashrc)
````install mongodb````
4. MongoDB stores its data in the /data/db directory by default but it does not generate that folder structure for you. So, you have to create that directory.
````$ sudo mkdir -p /data/db````
5. Check status
````mongod status````

####Python
- Note: The following instructions only need to be done once. After installation, refer to "Run the application on your local system" for instructions on how to launch the app
- Install the following packages: python, python-dev, pip and virtual-environment.
  - Mac: In the terminal, type "sudo easy_install python" (press enter), "sudo easy_install python-dev" (enter), "sudo easy_install pip" (enter) and "sudo install virtual-environment"
  - Linux (Ubuntu): "sudo apt-get install python python-dev python-pip python-virtualenv virtualenvwrapper" (enter)
- Clone the repository
- Now, type virtualenv venv
- After the python virtual environment is installed, it has to be activated
- To activate python virtual environment, "source venv/bin/activate"
- To install all remaining python packages in the virtual environment: pip install -r requirements.txt

##Run the application on your local system
- Once in the virtual environment (e.g., source venv/bin/activate), type "python run.py"
- You may have to create a secret key, the instructions will be provided in the terminal
- After you have run the commands for the secret key re-type "python run.py"
- The server starts and the website is accessible at: http://127.0.0.1:4500/
- To quit the application, use - "CTRL + C"
- To exit the virtual environment, type "deactivate"

##Code Push

####For smaller bug fixes

1. Clone repository (if you have not already cloned the repository)
Execute: "$ git clone 'reponame'"
2. Create a new branch which is based off origin/master. This is the hotfix branch.
Execute: "$ git checkout -b hotfix origin/master"
3. Make changes and commit. The commit message should be in present tense.
4. Before pushing to remote, fetch changes
Execute: "$ git fetch"
5. If updates to the local repo are required
Execute: "$ git pull --ff origin"
6. If no updates are required
Execute: "$ git push origin hotfix"
7. Go to github.com/reponame
8. Open a pull request against the master branch
9. Assign the pull request to another team member
10. Inform the team member to review code and merge into master

####For Readme

All steps are the same except, replace name of branch "hotfix" with "readme"


####For new features

All steps are the same except, replace name of branch "hotfix" with a different name like "feature-1"

####Stay tuned for more instructions
