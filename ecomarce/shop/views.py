from django.shortcuts import render
from django.http import HttpResponse
from . models import Product,Contact,Orders
from . models import orderUpdate
import json
from math import ceil
# Create your views here.
def product(request):
    allprods=[]
    catprods=Product.objects.values("category")
    cats={item["category"] for item in catprods}
    for cat in cats:
        prods=Product.objects.filter(category=cat)
        n=len(prods)
        nSlides=n//4 + ceil(n/4)- (n//4)
        allprods.append([prods,range(1,nSlides),nSlides])

    params={'allProds':allprods}    
    return render(request,'shop/products.html',params)

def shop(request):
    return render(request, 'shop/index.html')
        
def contact(request):
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        msg = request.POST.get('msg', '')
        contact = Contact(name=name, email=email,msg=msg)
        contact.save()
        
        

    return render(request, 'shop/contact.html')
        
def productview(request,myid):
    product=Product.objects.filter(id=myid)
    print(product)
    
    return render(request, 'shop/productview.html', {'product':product[0]})
        
def search(request):
    return render(request, 'shop/search.html')
def about(request):
    return render(request, 'shop/about.html')
        
def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone)
        order.save()
        
        update=orderUpdate(order_id= order.order_id,update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html',{'thank':thank,'id':id})

        
    return render(request, 'shop/checkout.html')
        
def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = orderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps(updates, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')


        

    
   

