from django.shortcuts import render
from mystore.models import Product
from django.http import HttpResponse
from cart import forms
import json
import urllib
import feedparser
import datetime
import os
import xlsxwriter
from .form import FormContact

# Create your views here.
def index(request): 
    pro_list = Product.objects.order_by('name')    
    cart_list = {}
    for product in pro_list:
        cart_list[product.id] = forms.CardAddProductForm()    
    pro_dict = {"products":pro_list, "carts":cart_list}
    
    return render(request, "mystore/index.html", context=pro_dict)

def product_detail(request, id=None):
    product = Product.objects.get(pk=id)
    cart_product_form = forms.CardAddProductForm()

    return render(request,'mystore/product_detail.html', context={'product': product, 'cart_product_form': cart_product_form})

def draw_chart(request):
    pro_list = Product.objects.order_by('name')
    name = []
    price = []
    for entry in pro_list:
        name.append(entry.name)
        price.append(entry.fee)
    gia_1 = {
        'name': 'Price',
        'data': price,
        'color': 'red'
    }
    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Price of Products'},
        'xAxis': {'categories': name},

        'series': [gia_1]
    }
    dump = json.dumps(chart)

    #export_excel
    chuoi_tap_tin = ""
    time_now = datetime.datetime.now()
    list_product = []
    list_tieu_de = ["id", "name", "fee", "description"]
    list_product.append(list_tieu_de)
    for item in pro_list:
        product = [item.id, item.name, item.fee, item.description]
        list_product.append(product)
    if request.method == 'POST':
        ten_tap_tin = "danh_sach_product_" + time_now.strftime("%d-%m-%Y-%H-%M-%S" + ".xlsx")
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']),'Desktop')
        duong_dan = desktop + "\\" + ten_tap_tin
        ghi_tap_tin(duong_dan, list_product)
        chuoi_tap_tin = "Đã lưu tập tin tại: " + duong_dan

    return render(request, "mystore/chart.html", {'chart': dump, 'result': chuoi_tap_tin})

def read_rss(request):
    feeds = feedparser.parse('https://newbalance.newsmarket.com/rss/latest-news/all')
    #print(feeds)
    return render(request, "mystore/readrss.html", context={"feeds": feeds})

def ghi_tap_tin(duong_dan, list_ghi):
    workbook = xlsxwriter.Workbook(duong_dan)
    worksheet = workbook.add_worksheet()

    row = 0
    for item in list_ghi:
        i=0
        while i <len(item):
            worksheet.write(row, i, item[i])
            i+=1
        row+=1
    workbook.close()
    return

def about_us(request):
    return render(request, "mystore/about_us.html")

def contact(request):
    registered = False
    if request.method == "POST":
        form_contact = FormContact(data = request.POST)
        if form_contact.is_valid():
            register = form_contact.save()
            register.save()
            registered = True
        else:
            print(form_contact.errors)
    else:
        form_contact = FormContact()

    return render(request,"mystore/contact.html",{'contact_form':form_contact,'registered':registered})
