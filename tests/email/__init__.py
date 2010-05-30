from webapp.clients.models import Client
from webapp.account.models import Account
from webapp.alerts.models import Alert

def create_alert(term="tim"):
    alert = Alert(user=Account.objects.all()[0],
                  client=Client.objects.all()[0],
                  term=term,
                  type="l",
                  frequency="50",
                  length=50)
    alert.save()
    return alert
