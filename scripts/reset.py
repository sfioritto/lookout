#!/Users/seanfioritto/lookout/env/LOOKOUT/bin/python

from conf import home
from webapp import settings
import os

def main():

    # create the dropall script
    os.chdir(home("webapp"))

    # grabs all the app names from installed_apps, skip the auth app so you don't have to
    # create the superuser account over and over.
    apps = ' '.join([a.split('.')[-1] for a in settings.INSTALLED_APPS]).strip('auth ')

#     os.system('python manage.py sqlreset auth blurb testing account feed alerts clients | grep "DROP TABLE" > /tmp/dropall.sql')
    os.system('python manage.py sqlreset %s | grep "DROP TABLE" > /tmp/dropall.sql' % apps)
    
    #add cascade to each line
    dropall = open("/tmp/dropall.sql").read()
    open("/tmp/dropall.sql", "w").write("\n".join([x[:-1] + "CASCADE;" for x in dropall.strip("\n").split("\n")]))
             
    # execute the newly created script
    os.system("psql -U postgres -d lookout -f /tmp/dropall.sql")

    # regenerate the tables
    os.system("python manage.py syncdb")
    os.system("python manage.py loaddata fixtures/initial_data.json")


if __name__ == "__main__":
    main()
