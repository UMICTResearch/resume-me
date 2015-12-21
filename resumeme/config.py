# File upload settings
ENV = 'dev'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'jpg', 'png', 'jpeg'])

###
# Application wide Error Messages
###

# Login Errors
LOGIN_ERROR = "Username or Password not valid"

# Registration Errors
REGISTRATION_EMAIL_EXISTS = "Email Already Exists, Please use another email."
REGISTRATION_INACTIVE = "Your account is currently not active."
REGISTRATION_NOLOGIN = "Unable to log you in. Please try again."
REGISTRATION_UNAME_EXISTS = "Username Already Exists, Please use another username."
REGISTRATION_ERROR = "Registration error. Please try again."
