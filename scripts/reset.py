#!/Users/seanfioritto/lookout/env/LOOKOUT/bin/python

from conf import home
import os

def main():

    # create the dropall script
    os.chdir(home("webapp"))
    os.system('python manage.py sqlreset blurb testing account feed alerts clients | grep "DROP TABLE" > /tmp/dropall.sql')
    
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
