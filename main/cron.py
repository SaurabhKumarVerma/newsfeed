from blacklist.models import Blacklist


def my_job():
    b = Blacklist(ip='12344')
    b.save()
