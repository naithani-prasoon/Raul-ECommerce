import csv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import string
import random
import os
from django.conf import settings
from django.template.loader import render_to_string
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
import pdfkit
from .models import Order

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags







def id_generator(size=10, chars= string.ascii_uppercase + string.digits):
    the_id = "".join(random.choice(chars) for x in range(size))
    try:
        order = Order.objects.get(order_id= the_id)
        id_generator()
    except Order.DoesNotExist:
        return the_id

API_KEY = "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"

def email_test(context):
    subject = 'Your Raul Retail Order'
    html_message = render_to_string('orders/Confirmed Order.html', context)
    plain_message = strip_tags(html_message)
    from_email = 'From <raulwebsite069@gmail.com>'
    to = 'dberhan@buffalo.edu'

    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

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
                        Product.section = SectionFinder(str(row[3]))
                        Product.price = str(row[6])
                        lowercase_title = str(row[1]).lower()
                        Product.slug = lowercase_title.replace(" ","_")
                        try:
                            Product.image = str(row[1]).replace(" ","_") + ".jpg"
                        except:
                            pass
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
                            try:
                                Product.image = str(row[1]).replace(" ","_") + str(row[5])+ ".jpg"
                            except:
                                pass
                            if str(row[3]) != "Delivery":
                                if str(row[3]) != "Shipping":
                                    if str(row[3]) != "Event":
                                        Product.section = SectionFinder(str(row[3]))
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
def SectionFinder(str):
    if str == "Baskets":
        return "Decorative Accessories"
    if str == "Candlesticks":
        return "Decorative Accessories"
    if str == "Benches":
        return "Furniture"
    if str == "Bowls":
        return "Sale"
    if str == "Bowls, Footed":
        return "Tabletop"
    if str == "Boxes":
        return "Decorative Accessories"
    if str == "Bud Vase, Hanging":
        return "Decorative Accessories"
    if str == "Bud Vases":
        return "Decorative Accessories"
    if str == "Cake Stands":
        return "Tabletop"
    if str == "Candelabras":
        return "Tabletop"
    if str == "Candle Holders":
        return "Decorative Accessories"
    if str == "Candle Holders, Hanging":
        return "Decorative Accessories"
    if str == "Candlelight":
        return "Decorative Accessories"
    if str == "Candlesticks":
        return "Decorative Accessories"
    if str == "Cashpots":
        return "Decorative Accessories"
    if str == "Chairs":
        return "Furniture"
    if str == "Clocks":
        return "Decorative Accessories"
    if str == "Decorative Objects":
        return "Decorative Accessories"
    if str == "Decorative Objects":
        return "Decorative Accessories"
    if str == "Dinnerware":
        return "Tabletop"
    if str == "Floral":
        return "Floral"
    if str == "Footed Vases":
        return "Decorative Accessories"
    if str == "Furniture":
        return "Furniture"
    if str == "Frames":
        return "Decorative Accessories"
    if str == "Glassware":
        return "Decorative Accessories"
    if str == "Hurricanes":
        return "Decorative Accessories"
    if str == "Lamps":
        return "Decorative Accessories"
    if str == "Lanterns":
        return "Decorative Accessories"
    if str == "Mirrors":
        return "Wall Art"
    if str == "Pitchers":
        return "Tabletop"
    if str == "Plant":
        return "Floral"
    if str == "Rugs":
        return "Furniture"
    if str == "Sale":
        return "Sale"
    if str == "Notebooks":
        return "Decorative Accessories"
    if str == "Saucers":
        return "Decorative Accessories"
    if str == "Sofas":
        return "Furniture"
    if str == "Statues":
        return "Decorative Accessories"
    if str == "Wall Art":
        return "Wall Art"
    if str == "Votives":
        return "Decorative Accessories"
    if str == "Vases, Footed":
        return "Decorative Accessories"
    if str == "Vases":
        return "Decorative Accessories"
    if str == "Urns":
        return "Decorative Accessories"
    if str == "Trays":
        return "Decorative Accessories"
    if str == "Terrariums":
        return "Decorative Accessories"
    if str == "Stationary":
        return "Decorative Accessories"
    if str == "Shelves":
        return "Furniture"
    if str == "Tables":
        return "Furniture"
    if str == "Boxes":
        return "Furniture"
    if str == "Glassware":
        return "Tabletop"
    if str == "":
        return "Hello"
    if str == "Miscellaneous":
        return "Hello"
    if str == "Stools":
        return "Furniture"
    if str == "Chandeliers":
        return "Decorative Accessories"
    if str == "Statues":
        return "Furniture"
    if str == "Baskets":
        return "Decorative Accessories"
    if str == "Bowls, Footed":
        return "Tabletop"
    if str == "Tabletop":
        return "Tabletop"
    if str == "Pillars":
        return "Sale"






































