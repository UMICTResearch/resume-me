# resume-me
================

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
- Note: The following instructions only need to be done once. After installation, refer to "Run the application on your local system" for instructions on how to launch the app
- Install the following packages: python, python-dev, pip and virtual-environment.
  - Mac: In the terminal, type "sudo easy_install python" (press enter), "sudo easy_install python-dev" (enter), "sudo easy_install pip" (enter) and "sudo install virtual-environment"
  - Linux (Ubuntu): "sudo apt-get install python python-dev python-pip python-virtualenv virtualenvwrapper" (enter)
- Clone the repository
- Now, type virtualenv venv
- After the python virtual environment is installed, it has to be activated
- To activate python virtual environment, "source venv/bin/activate"
- To install all remaining packages: pip install -r requirements.txt

##Run the application on your local system
- Once in the virtual environment (e.g., source venv/bin/activate), type "python run.py"
- You may have to create a secret key, the instructions will be provided in the terminal
- After you have run the commands for the secret key re-type "python run.py"
- The server starts and the website is accessible at: http://127.0.0.1:4500/
- To quit the application, use - "CTRL + C"
- To exit the virtual environment, type "deactivate"

##Code Push

####For smaller bug fixes

1. Clone repository
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

####For new features

All steps are the same except, replace name of branch "hotfix" with a different name like "feature-1"

####Stay tuned for more instructions
