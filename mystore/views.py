from django.shortcuts import render
from mystore.models import Product
from django.http import HttpResponse
from cart import forms

# Create your views here.
def index(request):
    pro_list = Product.objects.order_by('name')
    pro_dict = {"products":pro_list}
    return render(request, "mystore/index.html", context=pro_dict)

def product_detail(request, id=None):
    product = Product.objects.get(pk=id)
    cart_product_form = forms.CardAddProductForm()

    return render(request,'mystore/product_detail.html', context={'product': product, 'cart_product_form': cart_product_form})