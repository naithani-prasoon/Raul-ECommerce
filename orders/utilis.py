import string
import random
import os
import csv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import string
import random
import os
from django.shortcuts import render, HttpResponseRedirect
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
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
import pdfkit
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


def pdf(idnum,context):
    outfilename = "Order_Number_" + idnum + ".pdf"
    outfiledir = settings.MEDIA_ROOT
    outfilepath = os.path.join( outfiledir, outfilename )
    rendered = render_to_string('orders/Confirmed Order.html', context)
    pdfkit.from_string(rendered,outfilepath)


def add_item():
    from Raul.models import product, Variation
    with open('orders/static/orders/catalog-2020-07-20-2213.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        Count = 0
        line_count = 0
        for row in csv_reader:
            Count = product.objects.filter(title=str(row[1])).count()
            Product = product()
            variation = Variation()
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                if str(row[5]) == "Regular":
                    if(str(row[6]) != "variable"):
                        print(f'\t Product Name:{row[1]} Product Description:{row[2]} Product Category: {row[3]} Product Price: {row[6]}.')
                        Product.title = str(row[1])
                        Product.description = str(row[2])
                        Product.category = str(row[3])
                        Product.price = str(row[6])
                        lowercase_title = str(row[1]).lower()
                        Product.slug = lowercase_title.replace(" ","_")
                        Product.save()
                        line_count += 1
                else:
                    if Count == 0:
                        Product.title = str(row[1])
                        Product.description = str(row[2])
                        Product.category = str(row[3])
                        if (str(row[6]) != "variable"):
                            Product.price = str(row[6])
                            lowercase_title = str(row[1]).lower()
                            Product.slug = lowercase_title.replace(" ","_")
                            Product.save()
                        Count = product.objects.filter(title=str(row[1])).count()
                        print(Count)
                    if Count > 0:
                        product_instance = product.objects.get(title=str(row[1]))
                        print(product_instance.price)
                        variation.product = product_instance
                        variation.category = "size"
                        variation.title = str(row[5])
                        if (str(row[6]) != "variable"):
                            variation.price = str(row[6])
                            variation.save()
                        Count = 0



            print(f'Processed {line_count} lines.')




