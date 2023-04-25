from django.shortcuts import render
from django.http import JsonResponse
from cartapp.models import *
# Create your views here.
def show_products(request):
    response = render(request,"products.html",context={"products": Product.objects.all()})
    if request.method == "POST":
        if "product_pk" not in request.COOKIES: # якщо product_pk немає в кукі
            new_product = request.POST.get('product_pk') # отримуємо product_pk
            response.set_cookie('product_pk',new_product) # створюємо кукі
            return response # повертаємо результат
        else: # 
            new_product = request.COOKIES['product_pk'] + " " + request.POST.get('product_pk') # "1" + " " + "2"  = "1 2"
            response.set_cookie('product_pk',new_product) # створюємо кукі
            return response # повертаємо результат

    return response

def show_cart(request):
    if "product_pk" in request.COOKIES:

        products_pk = request.COOKIES['product_pk']
        
        products_pk = products_pk.split(' ')

        list_products = list()
        for product_pk in products_pk:
            list_products.append(Product.objects.get(pk=product_pk))
        response = render(request,"cart.html",context={"products": list_products})

    else:
        response = render(request,"cart.html",context={"products":list()})

    if request.method == "POST":
        if len(request.COOKIES["product_pk"]) == 1:
            response.delete_cookie("product_pk")
        delete_product = request.COOKIES['product_pk']
        product_pk = request.POST.get("product_pk") + " "
        delete_product = delete_product.replace(product_pk, "", 1)
        response.set_cookie("product_pk", delete_product)

    return response
