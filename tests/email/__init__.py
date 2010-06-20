from webapp.clients.models import Client
from webapp.account.models import Account
from webapp.alerts.models import Alert

def create_alert(term="tim"):
    """
    Creates a basic alert that can be used for tests. Assumes
    an account and client object exist.
    """
    alert = Alert(user=Account.objects.all()[0],
                  client=Client.objects.all()[0],
                  term=term,
                  type="l",
                  frequency="50",
                  length=50)
    alert.save()
    return alert
