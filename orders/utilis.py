import string
import random
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import string
import random
import os
from .models import Order
from carts.models import Cart
from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import SimpleDocTemplate,Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from django.contrib.auth import get_user_model, get_user


from .models import Order

def id_generator(size=10, chars= string.ascii_uppercase + string.digits):
    the_id = "".join(random.choice(chars) for x in range(size))
    try:
        order = Order.objects.get(order_id= the_id)
        id_generator()
    except Order.DoesNotExist:
        return the_id

API_KEY = "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"
def email_test():
    message = Mail(
        from_email='afares2009@icloud.com',
        to_emails='aifares@buffalo.edu',
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient(API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

def make_invoice(data,idnum):
    outfilename = "Order_Number_" + idnum + ".pdf"
    outfiledir = settings.MEDIA_ROOT
    outfilepath = os.path.join( outfiledir, outfilename )

    pdf = SimpleDocTemplate(
        outfilepath,
        pagesize = letter
    )
    table = Table(data)
    elems =[]
    elems.append(table)
    pdf.build(elems)

