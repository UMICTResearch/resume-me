# resume-me
================

## Table of Contents
1. [Coding Standards](#coding-standards)
2. [Installation Instructions](#installation-instructions)
3. [Run the application on your local system](#run the application on your local system)
4. [Code Push Mechanism](#code-push-mechanism)

##Coding Standards
- Strictly follow PEP8 coding standards
- Use the editorconfig file with preferred IDE for consistency

##Installation Instructions
- Note: The following instructions only need to be done once. After installation, refer to "Run the application on your local system" for instructions on how to launch the app
- Clone the repository
- Install the following packages: python, python-dev, pip and virtual-environment.
  - Mac: In the terminal, type "sudo easy_install python" (press enter), "sudo easy_install python-dev" (enter), "sudo easy_install pip" (enter) and "sudo install virtual-environment"
  - Linux (Ubuntu): "sudo apt-get install python python-dev python-pip python-virtualenv virtualenvwrapper" (enter)
- Now, type virtualenv venv
- After the python virtual environment is installed, it has to be activated
- To activate python virtual environment, "source venv/bin/activate"
- To install all remaining packages: pip install -r requirements.txt (Note: enter the complete path to requirements.txt)
##Run the application on your local system
- Once in the virtual environment (e.g., source venv/bin/activate), type "python run.py"
- You may have to create a secret key, the instructions will be provided in the terminal
- After you have run the commands for the secret key re-type "python run.py"
- The server starts and the website is accessible at: http://127.0.0.1:4500/
- To quit the application, use - "CTRL + C"
- To exit the virtual environment, type "deactivate"

##Code Push Mechanism
- Create a branch for the feature in the sprint

- Make changes and push to the branch
- Raise a merge request with test branch
- Assign merge request to another developer(s)

####Stay tuned for more instructions
