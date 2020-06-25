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
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from django.contrib.auth import get_user_model, get_user


def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    the_id = "".join(random.choice(chars) for x in range(size))
    try:
        order = Order.objects.get(order_id=the_id)
        id_generator()
    except Order.DoesNotExist:
        return the_id

def make_invoice(data,idnum):
    outfilename = "Order_Number_" + idnum + ".pdf"
    outfiledir = 'media'
    outfilepath = os.path.join( outfiledir, outfilename )

    pdf = SimpleDocTemplate(
        outfilepath,
        pagesize = letter
    )

    table = Table(data)
    elems =[]
    elems.append(table)
    pdf.build(elems)

def sendEmail(request):
    User = get_user(request)
    subject = 'Subject'
    to_email= User.email
    cart = Cart.objects.get(user=User,active=True)
    html_content = render_to_string('orders/recipt.html', {'cart': cart})
    text_content = strip_tags(html_content)
    from_email = settings.EMAIL_HOST_USER
    msg = EmailMultiAlternatives(subject=subject,body=text_content,from_email=from_email,to=[to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    print("Hi")









