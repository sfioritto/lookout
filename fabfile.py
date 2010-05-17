from fabric.api import *
from datetime import datetime

env.hosts = ['postosaurus.com']
env.approot = "/var/local/postosaurus"


def test():
    local("nosetests")


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
            run("rm -rf snapshots/%s" % hash)
            run("mkdir snapshots/%s" % hash)
            run("cd snapshots/%s; tar -xvf '/tmp/%s'" % (hash,archive))


def upload_untar(archive, hash):
    upload(archive)
    untar(archive, hash)


def switch(hash):
    with cd(env.prodhome):
        sudo("ln -s %s/snapshots/%s/app /tmp/live_tmp && sudo mv -Tf /tmp/live_tmp /var/local/postosaurus/app" % (env.prodhome, hash))
        sudo("ln -s %s/snapshots/%s/webapp /tmp/live_tmp && sudo mv -Tf /tmp/live_tmp /var/local/postosaurus/webapp" % (env.prodhome, hash))
        sudo("ln -s %s/snapshots/%s/media /tmp/live_tmp && sudo mv -Tf /tmp/live_tmp /var/local/postosaurus/media" % (env.prodhome, hash))
        sudo("ln -s %s/snapshots/%s/config /tmp/live_tmp && sudo mv -Tf /tmp/live_tmp /var/local/postosaurus/config" % (env.prodhome, hash))
    with cd(env.approot):
        run("cp webappsettings.py webapp/settings.py")
        run("cp config/prod-settings.py config/settings.py")


def reboot():
    with settings(warn_only=True):
        with cd(env.approot):
            sudo("apache2ctl graceful")
            sudo("lamson stop -ALL run/")
            sudo("rm run/*")
            sudo("lamson start -gid 1000 -uid 1000")
            sudo("lamson start -gid 1000 -uid 1000 -boot config.queue -pid run/queue.pid")
            sudo("chown -R %s:%s ../postosaurus" % (env.user, env.user))
    

def image(instance):
    date = datetime.today().strftime("%Y%m%d%H%M")
    bucket = 'postosaurus' + date

    put('~/.ec2/%s' % env.aws_private_key, '/tmp/%s' % env.aws_private_key)
    put('~/.ec2/%s' % env.aws_certificate, '/tmp/%s' % env.aws_certificate)
    sudo('mv /tmp/%s /mnt/%s' % (env.aws_private_key, env.aws_private_key))
    sudo('mv /tmp/%s /mnt/%s' % (env.aws_certificate, env.aws_certificate))
    
    #bundle
    sudo('ec2-bundle-vol --no-inherit -d /mnt -k /mnt/%s -c /mnt/%s -u %s -r i386' % (env.aws_private_key, env.aws_certificate, env.aws_user))

    #updload
    sudo('ec2-upload-bundle -b %s -m /mnt/image.manifest.xml -a %s -s %s %s' % (bucket, env.aws_access_key, env.aws_secret_key, instance))

    #register
    local("ec2-register -K ~/.ec2/%s -C ~/.ec2/%s %s/image.manifest.xml" % (env.aws_private_key, env.aws_certificate, bucket))

    cleanup()

def cleanup():
    sudo("rm /mnt/image*; rm -rf /mnt/img-mnt/; rm /mnt/%s; rm /mnt/%s" % (env.aws_private_key, env.aws_certificate))    

def deploy(hash):
    with cd(env.devpath):
        test()
        archive = pack(hash)
    upload_untar(archive, hash)
    switch(hash)
    reboot()

    
    

