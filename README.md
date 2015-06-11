# resume-me
================

## Table of Contents
1. [Coding Standards](#coding-standards)
2. [Installation Instructions](#installation-instructions)
3. [Code Push Mechanism](#code-push-mechanism)

##Coding Standards
- Strictly follow PEP8 coding standards
- Use the editorconfig file with preferred IDE for consistency

##Installation Instructions
- Clone the repository
- Install the following packages: python, python-dev, pip and virtual-environment. There is no need to install a package that is already installed. To do this, if on a mac, in the terminal, type "sudo easy_install python" (press enter), "sudo easy_install python-dev" (enter), "sudo easy_install pip" (enter) and "sudo_instsall virtual-environment"
- now, type virtualenv venv
- pip install -r requirements.txt (this script should install all remaining packages needed)

##Run the application on your local system
-<TODO: NISHAN - what is the command to run this on the local system?>
-<TRD: I tried the following: virtualenv ven and then source venv/bin/activate and finally python run.py (but I received the following errors: Traceback (most recent call last):
  File "run.py", line 5, in <module>
    from app import app
  File "/Users/tdillahu/Development/Projects/resume-me/app/__init__.py", line 6, in <module>
    import pytz
ImportError: No module named pytz


##Code Push Mechanism
- Create a branch for the feature in the sprint
- Make changes and push to the branch
- Raise a merge request with test branch
- Assign merge request to another developer(s)

####Stay tuned for more instructions
