from django.conf import settings
from mystore.models import Product

class Cart(object):
    def __init__(self,request):
        """
        initialze the session
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        #cart: dai dien cho gio hang
        if not cart:  # check gio hang
            cart = self.session[settings.CART_SESSION_ID] = {}
        #self.cart chua gio hang
        self.cart = cart

    def add(self,product,quantity=1,update_quantity = False):
        """
        add the product to the cart or update its quantity
        """
        product_id = str(product.pk)
        #nếu id của product ko nằm trong giỏ hàng ===> tạo ra một product trong giỏ hàng
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity':0, 'fee':str(product.fee)}
        #nếu trạng thái bằng true
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        #thêm tiếp tục vào product đã có trong giở hàng
        else:
            self.cart[product_id]['quantity'] += quantity
        #bất cứ khi nào giở hàng thay dổi ===> save
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self,product):
        product_id = str(product.pk)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        interate over the items in card and get the product from the database
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in = product_ids)
        for product in products:
            self.cart[str(product.pk)]['product'] = product
        for item in self.cart.values():
            item['fee'] = item['fee']
            item['total_fee'] = int(item['fee'])*item['quantity']
            yield item

    def __len__(self):
        """
        count all items in the card
        """
        return sum(int(item['quantity']) for item in self.cart.values())

    def get_total_fee(self):
        """
        get total fee of product
        """
        return sum((int(item['fee']))*int(item['quantity']) for item in self.cart.values())