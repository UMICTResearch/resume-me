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
- Clone the repository
- Install the following packages: python, python-dev, pip and virtual-environment. There is no need to install a package that is already installed. To do this, if on a mac, in the terminal, type "sudo easy_install python" (press enter), "sudo easy_install python-dev" (enter), "sudo easy_install pip" (enter) and "sudo_instsall virtual-environment"
- now, type virtualenv venv
- pip install -r requirements.txt (this script should install all remaining packages needed)

##Run the application on your local system
- <TODO: NISHAN - what is the command to run this on the local system?>
- <TRD: I tried the following: virtualenv ven and then source venv/bin/activate, then pip install -r requirements.txt, then I received the errror File "run.py", line 5, in <module>
    from app import app
  File "/Users/tdillahu/Development/Projects/resume-me/app/__init__.py", line 6, in <module>
    import pytz
ImportError: No module named pytz
I then ran pip install pytz
(venv)si-tdillahu-mbp:resume-me tdillahu$ pip install pytz
You are using pip version 6.0.8, however version 7.0.3 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
Collecting pytz

After that error, I received the following error: ImportError: No module named dateutil
I then had to run "pip install python-dateutil"
and received another error
ImportError: No module named requests
I then ran "pip install requests"
(venv)si-tdillahu-mbp:resume-me tdillahu$  pip install requests

And then python run.py

and got the following:
logger initiated for pcbc-mturk-app.resupload.helpers
logfile initiated at : ./Logs/check_status_task.log
logger initiated for pcbc-mturk-app
Error: No secret key. Create it with:
mkdir -p /Users/tdillahu/Development/Projects/resume-me/instance
head -c 24 /dev/urandom > /Users/tdillahu/Development/Projects/resume-me/instance/secret_key
(venv)si-tdillahu-mbp:resume-me tdillahu$ mkdir -p /Users/tdillahu/Development/Projects/resume-me/instance
(venv)si-tdillahu-mbp:resume-me tdillahu$ head -c 24 /dev/urandom > /Users/tdillahu/Development/Projects/resume-me/instance/secret_key
(venv)si-tdillahu-mbp:resume-me tdillahu$ python run.py
logger initiated for pcbc-mturk-app.resupload.helpers
logfile initiated at : ./Logs/check_status_task.log
logger initiated for pcbc-mturk-app
logfile initiated at : ./Logs/resume-feedback-dev.log
 * Running on http://0.0.0.0:4500/ (Press CTRL+C to quit)
 * Restarting with stat
logger initiated for pcbc-mturk-app.resupload.helpers
logfile initiated at : ./Logs/check_status_task.log
logger initiated for pcbc-mturk-app
logfile initiated at : ./Logs/resume-feedback-dev.log
127.0.0.1 - - [15/Jun/2015 16:16:29] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [15/Jun/2015 16:16:29] "GET /favicon.ico HTTP/1.1" 404 -
127.0.0.1 - - [15/Jun/2015 16:18:09] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [15/Jun/2015 16:19:14] "GET / HTTP/1.1" 200 -

I got the following after right clicking on http://0.0.0.0:4500/
"Test Server for research. Contact gparuthi [at] umich.edu if you have any questions."

##Code Push Mechanism
- Create a branch for the feature in the sprint
- Make changes and push to the branch
- Raise a merge request with test branch
- Assign merge request to another developer(s)

####Stay tuned for more instructions
