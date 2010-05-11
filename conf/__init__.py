import os

HOME = "/Users/seanfioritto/lookout"
EMAIL = os.path.join(HOME, "emails")


def home(path="/"):
    return os.path.join(HOME, path)

def email(path="/"):
    return os.path.join(EMAIL, path)
