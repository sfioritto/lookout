from fabric.api import *

env.hosts = ['lookoutthere.com']
env.approot = "/var/lookout/www"
env.prodhome = "/var/lookout"
env.emailroot = "/var/lookout/www/emails"


def test():
    local("nosetests tests/")


def pack(hash):

    """
    Creates a clean copy of the code
    """
    archivename = "%s.tar.gz" % hash
    local("git archive --format=tar %s | gzip > /tmp/%s;" % (hash, archivename))
    return archivename


def prepare(hash):

    """
    Test and archive postosaurus.
    """

    test()
    pack(hash)


def upload(archive):
    put('/tmp/%s' % archive, '/tmp/')


def untar(archive, hash):
    with settings(warn_only=True):
        with cd(env.prodhome):
            sudo("rm -rf snapshots/%s" % hash)
            sudo("mkdir snapshots/%s" % hash)
            sudo("cd snapshots/%s; tar -xvf '/tmp/%s'" % (hash,archive))


def upload_untar(archive, hash):
    upload(archive)
    untar(archive, hash)


def switch(hash):
    with cd(env.prodhome):
        sudo("ln -s %s/snapshots/%s /tmp/live_tmp && sudo mv -Tf /tmp/live_tmp /var/lookout/www" % (env.prodhome, hash))

    with cd(env.approot):
        sudo("cp prod/webapp/settings.py webapp/settings.py")
        sudo("cp prod/emails/settings.py emails/settings.py")


def reboot():
    with settings(warn_only=True):
        with cd(env.emailroot):
            sudo("apache2ctl graceful")
            sudo("lamson stop -ALL run/")
            sudo("rm run/*")
            sudo("lamson start -gid 65534 -uid 103")
            sudo("lamson start -gid 65534 -uid 103 -boot config.queue -pid run/queue.pid")
            sudo("chown -R sean:sean ../www")

    
def deploy(hash):
    
    test()
    archive = pack(hash)
    upload(archive)
    untar(archive, hash)
    switch(hash)
#    reboot()

    
    

