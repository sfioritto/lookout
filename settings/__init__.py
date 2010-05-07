import os

LOOKOUT_HOME = "/Users/seanfioritto/lookout"
LOOKOUT_EMAIL = os.path.join(LOOKOUT_HOME, "email")
LOOKOUT_WEBAPP = os.path.join(LOOKOUT_HOME, "webapp")
LOOKOUT_ERROR = os.path.join(LOOKOUT_HOME, "error")
RUN_QUEUE = os.path.join(LOOKOUT_HOME, LOOKOUT_EMAIL, "run")
ERROR_QUEUE = os.path.join(LOOKOUT_HOME, LOOKOUT_EMAIL, "email/error")
