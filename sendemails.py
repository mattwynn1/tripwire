from mechanize import Browser
from bs4 import *
from time import *
import re
import sys
from django.core.management import setup_environ
sys.path.append('/home/omaha/webapps/dj/myproject')
import settings
setup_environ(settings)
from myproject.tripwire.models import *
from django.core.mail import send_mass_mail
from django.db.models import Q
from django.template.loader import *
from django.core.mail import EmailMultiAlternatives

lastnames = Name.objects.values("last")

firstnames = Name.objects.values("first")

firstlist = []

for obj in firstnames:
    firstlist.append(obj['first'])

jailmatches = Inmate.objects.filter(last__in=lastnames).filter(reduce(lambda x, y: x |y, [Q(rest__icontains=first) for first in firstlist]))
recipients = ['matt.wynn@owh.com', 'cody.winchester@owh.com']

if jailmatches.count > 0:
    plaintext = get_template('jail/email.txt')
    htmly = get_template('jail/email.html')
    d = Context({ 'jailmatches': jailmatches, })
    subject, from_email, to = 'Jail bookings of interest', 'jailalerts@no-reply.com', recipients
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


