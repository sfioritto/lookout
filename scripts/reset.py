#!/Users/seanfioritto/lookout/env/LOOKOUT/bin/python

from conf import home
import os

def main():
    os.chdir(home(""))
    os.system("psql -U postgres -d lookout -f scripts/dropall.sql")
    os.chdir(home('webapp'))
    os.system("python manage.py syncdb")


if __name__ == "__main__":
    main()
