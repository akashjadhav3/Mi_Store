from django.shortcuts import render, redirect
from .models import Product, Contact,Login, Orders, OrderUpdate,Signin, Payments
from math import ceil
import json
from .forms import UserRegisterForm
from django.contrib import messages
#from django.views.decorators.csrf import csrf_exempt
#from PayTm import Checksum
# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#MERCHANT_KEY = 'Your-Merchant-Key-Here'


def IsAdminCheck(user):
    is_admin_group = user.groups.filter(name__in=['admin']).exists()    
    return is_admin_group

def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    isAdmin = IsAdminCheck(request.user)
    context = {'allProds':allProds,'isAdmin':isAdmin}
    return render(request, 'shop/index.html', context)

# def home(request):
#     isAdmin = IsAdminCheck(request.user)
#     allProds = []
#     catprods = Product.objects.values('category', 'id')
#     cats = {item['category'] for item in catprods}
#     for cat in cats:
#         prod = Product.objects.filter(category=cat)
#         n = len(prod)
#         nSlides = n // 4 + ceil((n / 4) - (n // 4))
#         allProds.append([prod, range(1, nSlides), nSlides])
#     params = {'allProds':allProds, 'isAdmin':isAdmin}
#     return render(request, 'shop/home.html', params)


def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    thank = False
    isAdmin = IsAdminCheck(request.user)
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html', {'thank': thank,'isAdmin': isAdmin})

# def login(request):
#     thank = False
#     if request.method=="POST":
#         uname = request.POST.get('uname', '')
#         psw = request.POST.get('psw', '')
#         login = Login(uname=uname, psw=psw)
#         login.save()
#         thank = True
#     return render(request, 'shop/login.html', {'thank': thank})

# def signin(request):
#     thank = False
#     if request.method=="POST":
#         uname = request.POST.get('uname', '')
#         email = request.POST.get('email', '')
#         phone = request.POST.get('phone', '')
#         psw = request.POST.get('psw', '')
#         signin = Signin(uname=uname, phone=phone, email=email, psw=psw)
#         signin.save()
#         thank = True
#     return render(request, 'shop/register.html', {'thank': thank})

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')


def productView(request, myid):

    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/prodView.html', {'product':product[0]})

import uuid
import razorpay
from mac.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET
client = razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRET))

@login_required
def checkout(request):
    isAdmin = IsAdminCheck(request.user)
    if request.method=="POST":
        user = request.user
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        
        #Razorpay
        order_ammount = int(amount)*100
        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'
        notes = {'shipping_address':address}
        payment_order = client.order.create(dict(amount=order_ammount,currency=order_currency,receipt='TR110462011',payment_capture=1,notes=notes))
        # payment_order = client.order.create({'amount':order_ammount,'currency':order_currency,'receipt' : order_receipt,'payment_capture':'1'})
        # payment_order = client.order.create('amount':order_ammount, 'currency':order_currency, 'receipt':order_receipt, 'notes':notes)
        payment_order_id = payment_order['id']
        
        order.order_id2 = str(payment_order_id)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id

        
        context = {'thank':thank, 'model_id': id,'amount':amount,'api_key':RAZORPAY_API_KEY,'order_id':payment_order_id,'name':name,'phone':phone,'address':address}
        context['isAdmin']=isAdmin
        return render(request, 'payment/payment.html', context)
    return render(request, 'shop/checkout.html')


#@csrf_exempt
#def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
 #   response_dict = {}
  #  for i in form.keys():
   #     response_dict[i] = form[i]
    #    if i == 'CHECKSUMHASH':
     #       checksum = form[i]

    #verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    #if verify:
     #   if response_dict['RESPCODE'] == '01':

      #      print('order successful')
       # else:
        #    print('order was not successful because' + response_dict['RESPMSG'])
   # return render(request, 'shop/paymentstatus.html', {'response': response_dict})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) or None
        if form.is_valid():
            username = request.POST.get('username')
            #########################mail####################################
            # htmly = get_template('user/Email.html')
            # d = { 'username': username }
            # subject, from_email, to = 'hello', 'from@example.com', 'to@emaple.com'
            # html_content = htmly.render(d)
            # msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # try:
            #     msg.send()
            # except:
            #     print("error in sending mail")
            ##################################################################
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('Login')
    else:
        form = UserRegisterForm()
    return render(request, 'shop/register.html', {'form': form,'title':'reqister here'})



from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
def Login(request):
    if request.method == 'POST':
  
        # AuthenticationForm_can_also_be_used__
  
        username = request.POST['username']
        
        password = request.POST['password']
        print(username)
        print(password)
        user = authenticate(request, username = username, password = password)
        print(user)
        if user is not None:
            form = login(request, user)
            return redirect('ShopHome')
        else:
            messages.info(request, f'account done not exit plz sign in')
    form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form':form, 'title':'log in'})

from django.contrib.auth import logout


def user_logout(request):
    logout(request) 
    return redirect('Login')


@login_required
def payment_success(request):
    payment_id = request.GET.get('payment_id')
    order_id = request.GET.get('order_id')
    signature = request.GET.get('signature')
    obj = Orders.objects.filter(order_id2=order_id)
    if obj:
        obj.update(payment_status=True)
        p1=Payments.objects.create(
            user = request.user,
            payment_id = payment_id,
            order_id = order_id,
            signature = signature,
            order_related = obj[0]
        )
        a=p1.save()
        return JsonResponse({'html':"Thanks for ordering with us"})
    return redirect('ShopHome')


@login_required
def transaction_details(request):
    obj = Payments.objects.filter(user=request.user.id)
    print(obj)
    if obj:
        return render(request,'shop/transaction.html',{'obj':obj,'isAdmin': IsAdminCheck(request.user)})
    return render(request,'shop/transaction.html',{'obj':obj})
    # return redirect('ShopHome')


def receipt(request,id):
    print(id)
    obj = Orders.objects.get(pk=id)
    if obj:
        return render(request,'shop/receipt.html',{'obj':obj})
    return redirect('ShopHome')