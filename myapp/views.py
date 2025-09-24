from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User,Group


# Create your views here.
from Myapp.models import category_table, Complaint_table, User_table, Book_table, review_table, request_table, \
    payment_table, chat_table, rent_table, rent_payment_table, notification_table


def login_get(request):
    return render(request,'index.html')

def login_post(request):
    username=request.POST['username']
    password=request.POST['password']
    user=authenticate(username=username,password=password)
    if user is not None:
        if user.groups.filter(name='admin').exists():
            login(request,user)
            return redirect('/Myapp/AdminHome/')
        elif user.groups.filter(name='user').exists():
            login(request, user)
            return redirect('/Myapp/UserHome/')
        else:
            messages.warning(request,'Invalid username or password')
            return redirect('/Myapp/login_get')
    messages.warning(request,'Invalid Username or password exists')
    return redirect('/Myapp/login_get')

def AdminHome(request):
    ob=review_table.objects.all()
    u=User_table.objects.count()
    b=Book_table.objects.count()
    c=review_table.objects.count()
    d=payment_table.objects.count()+rent_payment_table.objects.count()
    return render(request,'Admin/admin_home.html',{'rating':ob,'users':u,'books':b,'review':c,'payment':d})


@login_required(login_url='/Myapp/login_get')
def change_password(request):
    return render(request,'Admin/change_password.html')

@login_required(login_url='/Myapp/login_get')
def change_passwordpost(request):
    current_password = request.POST['current_password']
    new_password = request.POST['new_password']
    confirm_password = request.POST['confirm_password']

    f = check_password(current_password, request.user.password)
    if f:
        if new_password == confirm_password:
            user = request.user
            user.set_password(confirm_password)
            user.save()
            messages.success(request, "Password changed successfully. Please log in again.")
            return redirect('/Myapp/login_get')
        else:
            messages.error(request, "New password and confirm password do not match.")
            return redirect('/Myapp/change_password#course')
    else:
        messages.error(request, "Current password is incorrect.")
        return redirect('/Myapp/change_password#course')

@login_required(login_url='/Myapp/login_get')
def admin_homepage(request):
    return render(request,'Admin/adminhome.html')

@login_required(login_url='/Myapp/login_get')
def viewcategory(request):
    ob=category_table.objects.all()
    return render(request,'Admin/View category.html',{'data':ob})

@login_required(login_url='/Myapp/login_get')
def Addcategory(request):
    return render(request,'Admin/Add category.html')

@login_required(login_url='/Myapp/login_get')
def AddcategoryPost(request):
    category=request.POST["textfield"]
    ob=category_table()
    ob.category=category
    ob.save()
    return redirect('/Myapp/viewcategory/#course')

@login_required(login_url='/Myapp/login_get')
def editcategory(request,id):
    request.session["did"]=id
    ob=category_table.objects.get(id=id)
    return render(request,'admin/Edit category.html',{'data':ob})

@login_required(login_url='/Myapp/login_get')
def editcategoryPost(request):
    name = request.POST["textfield"]
    ob = category_table.objects.get(id= request.session["did"])
    ob.categoryname=name
    ob.save()
    return redirect('/myapp/viewcategory')

@login_required(login_url='/Myapp/login_get')
def deletecategory(request,id):
    ob = category_table.objects.get(id=id)
    ob.delete()
    return redirect('/Myapp/viewcategory/#course')

@login_required(login_url='/Myapp/login_get')
def viewusers(request):
    ob=User_table.objects.all()
    return render(request,'Admin/View users.html',{'data':ob})

@login_required(login_url='/Myapp/login_get')
def viewbooks(request):
    ob=Book_table.objects.all()
    return render(request,'Admin/view books.html',{'data':ob})

@login_required(login_url='/Myapp/login_get')
def viewtransactions(request):
    ob=payment_table.objects.all()
    rent=rent_payment_table.objects.all()
    return render(request,'Admin/View transactions.html',{'data':ob,'rent':rent})

@login_required(login_url='/Myapp/login_get')
def viewuserrating(request):
    ob=review_table.objects.all()
    return render(request,'Admin/viewuserrating.html',{'data':ob})

@login_required(login_url='/Myapp/login_get')
def viewcomplaint(request):
    ob=Complaint_table.objects.all()
    return render(request,'Admin/View Complaints.html',{'data':ob})

@login_required(login_url='/Myapp/login_get')
def sendreply(request,id):
    request.session['rid']=id
    return render(request,'Admin/Send reply.html')

@login_required(login_url='/Myapp/login_get')
def sendreplypost(request):
    reply=request.POST["reply"]
    ob=Complaint_table.objects.get(id=request.session['rid'])
    ob.reply=reply
    ob.save()
    return redirect('/Myapp/viewcomplaint#course')

###User###





@login_required(login_url='/Myapp/login_get')
def UserHome(request):
    user=User_table.objects.get(LOGIN__id=request.user.id)
    ob=Book_table.objects.filter(USER=user.id)
    books=Book_table.objects.exclude(USER=user.id)
    complaints=Complaint_table.objects.filter(USER=user.id)
    categories = category_table.objects.all()
    return render(request,'User/user_home.html',{'data':ob,'book':books,'complaints':complaints,'categories':categories})




def registration_user(request):
    return render(request,'User/Registration.html')

def RegistrationPost(request):
    name=request.POST['name']
    email=request.POST['email']
    phone=request.POST['phone']
    district=request.POST['district']
    pincode=request.POST['pincode']
    place=request.POST['place']
    longtitude=request.POST['longitude']
    latitude=request.POST['latitude']
    photo=request.FILES['photo']
    username=request.POST['username']
    password=request.POST['password']
    fs=FileSystemStorage()
    ps=fs.save(photo.name,photo)
    ob=User_table()
    ob.name=name
    ob.phone=phone
    ob.email=email
    ob.district=district
    ob.longitude=longtitude
    ob.latitude=latitude
    ob.photo=ps
    ob.pincode=pincode
    ob.place=place
    user=User.objects.create(username=username,password=make_password(password))
    user.save()
    user.groups.add(Group.objects.get(name='user'))
    ob.LOGIN=user
    ob.save()
    return redirect('/Myapp/login_get')

@login_required(login_url='/Myapp/login_get')
def View_profile(request):
    ob=User_table.objects.get(LOGIN=request.user.id)
    return render(request,'User/View_profile.html',{'user':ob})

@login_required(login_url='/Myapp/login_get')
def Update_profile(request):
    ob=User_table.objects.get(LOGIN=request.user.id)
    return render(request,'User/Update_profile.html',{'user':ob})

@login_required(login_url='/Myapp/login_get')
def UpdateProfilePost(request):
    name=request.POST['name']
    email=request.POST['email']
    phone=request.POST['phone']
    district=request.POST['district']
    pincode=request.POST['pincode']
    place=request.POST['place']
    longtitude=request.POST['longitude']
    latitude=request.POST['latitude']
    ob=User_table.objects.get(LOGIN=request.user.id)
    if 'photo' in request.FILES:
        photo=request.FILES['photo']
        fs=FileSystemStorage()
        ps=fs.save(photo.name,photo)
        ob.photo = ps
        ob.save()
    ob.name=name
    ob.phone=phone
    ob.email=email
    ob.district=district
    ob.longitude=longtitude
    ob.latitude=latitude
    ob.pincode=pincode
    ob.place=place
    ob.save()
    return redirect('/Myapp/View_profile')




@login_required(login_url='/Myapp/login_get')
def Add_book(request):
    ob=category_table.objects.all()
    return render(request,'User/Add_book.html',{'data':ob})

@login_required(login_url='/Myapp/login_get')
def BookPost(request):
    name = request.POST['name']
    author = request.POST['author']
    details = request.POST['details']
    price = request.POST['price']
    category = request.POST['category']
    rent_price = request.POST['rent_price']
    photo = request.FILES['photo']
    fs = FileSystemStorage()
    ps = fs.save(photo.name, photo)
    ob = Book_table()
    ob.USER=User_table.objects.get(LOGIN=request.user.id)
    ob.name = name
    ob.author = author
    ob.details = details
    ob.price = price
    ob.rent_price=rent_price
    ob.photo = ps
    ob.CATEGORY_id = category
    ob.save()
    return redirect('/Myapp/UserHome/#featured-books')


@login_required(login_url='/Myapp/login_get')
def EditBook(request,id):
    cb=Book_table.objects.get(id=id)
    request.session['eid']=id
    ob=category_table.objects.all()
    return render(request,'User/Edit_book.html',{'data':cb,'category':ob})

@login_required(login_url='/Myapp/login_get')
def BookEditPost(request):
    name = request.POST['name']
    author = request.POST['author']
    details = request.POST['details']
    price = request.POST['price']
    rent_price = request.POST['rent_price']
    category = request.POST['category']
    ob = Book_table.objects.get(id=request.session['eid'])
    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        ps = fs.save(photo.name, photo)
        ob.photo = ps
        ob.save()
    ob.USER=User_table.objects.get(LOGIN=request.user.id)
    ob.name = name
    ob.author = author
    ob.details = details
    ob.price = price
    ob.rent_price = rent_price
    ob.CATEGORY_id = category
    ob.save()
    return redirect('/Myapp/UserHome/#featured-books')

@login_required(login_url='/Myapp/login_get')
def deleteBook(request,id):
    ob=Book_table.objects.get(id=id)
    ob.delete()
    return redirect('/Myapp/UserHome/#featured-books')


@login_required(login_url='/Myapp/login_get')
def view_request(request):
    ob=request_table.objects.filter(BOOK__USER__LOGIN__id=request.user.id)
    cb=rent_table.objects.filter(BOOK__USER__LOGIN__id=request.user.id)
    print(ob)
    return render(request,'User/view_request.html',{'data':ob,'rent':cb})

@login_required(login_url='/Myapp/login_get')
def view_status(request):
    return render(request,'User/view_request.html')


@login_required(login_url='/Myapp/login_get')
def searchBook(request):
    input=request.POST['search']
    ob=Book_table.objects.filter(Q(name__icontains=input))
    return render(request,'User/user_home.html',{'data':ob})

@login_required(login_url='/Myapp/login_get')
def AddComplaintPost(request):
    complaint=request.POST['complaint']
    ob=Complaint_table()
    ob.complaint=complaint
    ob.date=datetime.today()
    ob.reply='pending'
    ob.USER=User_table.objects.get(LOGIN=request.user.id)
    ob.save()
    return redirect('/Myapp/UserHome/#complaint')

@login_required(login_url='/Myapp/login_get')
def DeleteComplaint(request,id):
    ob=Complaint_table.objects.get(id=id)
    ob.delete()
    return redirect('/Myapp/UserHome/#complaint')

@login_required(login_url='/Myapp/login_get')
def BookDetails(request,id):
    ob=Book_table.objects.get(id=id)
    rv=review_table.objects.filter(BOOK=id)
    requested = request_table.objects.filter(USER=User_table.objects.get(LOGIN__id=request.user.id), BOOK=ob).first()
    rent_requested = rent_table.objects.filter(USER=User_table.objects.get(LOGIN__id=request.user.id), BOOK=ob).first()
    return render(request,'User/viewbookdetails.html',{'book':ob,'reviews':rv,'requested':requested,'rent_requested':rent_requested})

@login_required(login_url='/Myapp/login_get')
def ReviewPost(request,id):
    review=request.POST['review']
    rating=request.POST['rating']
    ob=review_table()
    ob.review=review
    ob.rating=rating
    ob.date=datetime.today()
    ob.USER=User_table.objects.get(LOGIN__id=request.user.id)
    ob.BOOK_id=id
    ob.save()
    return redirect('/Myapp/UserHome/')

@login_required(login_url='/Myapp/login_get')
def RequestBook(request,id):
    ob=request_table()
    ob.USER=User_table.objects.get(LOGIN__id=request.user.id)
    ob.BOOK_id=id
    ob.status='pending'
    ob.date=datetime.today()
    ob.save()
    return redirect('/Myapp/UserHome/')

@login_required(login_url='/Myapp/login_get')
def RequestRentBook(request,id):
    ob=rent_table()
    ob.USER=User_table.objects.get(LOGIN__id=request.user.id)
    ob.BOOK_id=id
    ob.status='pending'
    ob.date=datetime.today()
    ob.save()
    return redirect('/Myapp/UserHome/')


@login_required(login_url='/Myapp/login_get')
def AcceptRequest(request,id):
    ob=request_table.objects.get(id=id)
    ob.status='Accepted'
    ob.save()
    return redirect('/Myapp/view_request/')

@login_required(login_url='/Myapp/login_get')
def RejectRequest(request,id):
    ob=request_table.objects.get(id=id)
    ob.status='Rejected'
    ob.save()
    ob.delete()
    return redirect('/Myapp/view_request/')

@login_required(login_url='/Myapp/login_get')
def AcceptRentRequest(request,id):
    ob=rent_table.objects.get(id=id)
    ob.status='Accepted'
    ob.save()
    return redirect('/Myapp/view_request/')

@login_required(login_url='/Myapp/login_get')
def RejectRentRequest(request,id):
    ob=rent_table.objects.get(id=id)
    ob.status='Rejected'
    ob.save()
    ob.delete()
    return redirect('/Myapp/view_request/')


@login_required(login_url='/Myapp/login_get')
def change_passwordpostUser(request):
    current_password = request.POST['current_password']
    new_password = request.POST['new_password']
    confirm_password = request.POST['confirm_password']

    f = check_password(current_password, request.user.password)
    if f:
        if new_password == confirm_password:
            user = request.user
            user.set_password(confirm_password)
            user.save()
            messages.success(request, "Password changed successfully. Please log in again.")
            return redirect('/Myapp/login_get')
        else:
            messages.error(request, "New password and confirm password do not match.")
            return redirect('/Myapp/UserHome')
    else:
        messages.error(request, "Current password is incorrect.")
        return redirect('/Myapp/UserHome')



@login_required(login_url='/Myapp/login_get')
def raz_pay(request,amount,id):
    import razorpay
    razorpay_api_key = "rzp_test_MJOAVy77oMVaYv"
    razorpay_secret_key = "MvUZ03MPzLq3lkvMneYECQsk"

    razorpay_client = razorpay.Client(auth=(razorpay_api_key, razorpay_secret_key))

    # amount = 200
    amount= float(amount)*100

    # Create a Razorpay order (you need to implement this based on your logic)
    order_data = {
        'amount': amount,
        'currency': 'INR',
        'receipt': 'order_rcptid_11',
        'payment_capture': '1',  # Auto-capture payment
    }

    # Create an order
    order = razorpay_client.order.create(data=order_data)

    context = {
        'razorpay_api_key': razorpay_api_key,
        'amount': order_data['amount'],
        'currency': order_data['currency'],
        'order_id': order['id'],
    }

    obj = payment_table()
    obj.REQUEST_id = id
    obj.date = datetime.today()
    obj.amount = float(amount/100)
    obj.status = 'paid'
    obj.save()

    request_table.objects.filter(id=id).update(status='paid')

    return render(request, 'User/razorpay.html',{ 'razorpay_api_key': razorpay_api_key,
        'amount': order_data['amount'],
        'currency': order_data['currency'],
        'order_id': order['id'],"id":id})


@login_required(login_url='/Myapp/login_get')
def raz_pay_rent(request,amount,id):
    import razorpay
    razorpay_api_key = "rzp_test_MJOAVy77oMVaYv"
    razorpay_secret_key = "MvUZ03MPzLq3lkvMneYECQsk"

    razorpay_client = razorpay.Client(auth=(razorpay_api_key, razorpay_secret_key))

    # amount = 200
    amount= float(amount)*100

    # Create a Razorpay order (you need to implement this based on your logic)
    order_data = {
        'amount': amount,
        'currency': 'INR',
        'receipt': 'order_rcptid_11',
        'payment_capture': '1',  # Auto-capture payment
    }

    # Create an order
    order = razorpay_client.order.create(data=order_data)

    context = {
        'razorpay_api_key': razorpay_api_key,
        'amount': order_data['amount'],
        'currency': order_data['currency'],
        'order_id': order['id'],
    }

    obj = rent_payment_table()
    obj.RENT_id = id
    obj.date = datetime.today()
    obj.amount = float(amount/100)
    obj.status = 'paid'
    obj.save()

    rent_table.objects.filter(id=id).update(status='paid')

    return render(request, 'User/razorpay.html',{ 'razorpay_api_key': razorpay_api_key,
        'amount': order_data['amount'],
        'currency': order_data['currency'],
        'order_id': order['id'],"id":id})



@login_required(login_url='/Myapp/login_get')
def chat(request,id):
    request.session["userid"] = id
    cid = str(request.session["userid"])
    request.session["new"] = cid
    qry = User_table.objects.get(LOGIN=cid)
    return render(request, "User/Chat.html", {'photo':qry.photo.url, 'name': qry.name, 'toid': cid})

@login_required(login_url='/Myapp/login_get')
def chat_view(request):
    fromid = request.user.id
    toid = request.session["userid"]
    qry = User_table.objects.get(LOGIN=request.session["userid"])
    from django.db.models import Q

    res = chat_table.objects.filter(Q(FROMID_id=fromid, TOID_id=toid) | Q(FROMID_id=toid, TOID_id=fromid)).order_by('id')
    l = []

    for i in res:
        l.append({"id": i.id, "message": i.message, "to": i.TOID_id, "date": i.date, "from": i.FROMID_id})

    return JsonResponse({'photo': qry.photo.url, "data": l, 'name': qry.name, 'toid': request.session["userid"]})


@login_required(login_url='/Myapp/login_get')
def chat_send(request, msg):
    lid = request.user.id
    toid = request.session["userid"]
    message = msg

    import datetime
    d = datetime.datetime.now().date()
    chatobt = chat_table()
    chatobt.message = message
    chatobt.TOID_id = toid
    chatobt.FROMID_id = lid
    chatobt.date = d
    chatobt.save()

    return JsonResponse({"status": "ok"})


@login_required(login_url='/Myapp/login_get')
def User_sendchat(request):
    FROM_id=request.POST['from_id']
    TOID_id=request.POST['to_id']
    msg=request.POST['message']

    from  datetime import datetime
    c=chat_table()
    c.FROMID_id=FROM_id
    c.TOID_id=TOID_id
    c.message=msg
    c.date=datetime.now()
    c.save()
    return JsonResponse({'status':"ok"})


@login_required(login_url='/Myapp/login_get')
def User_viewchat(request):
    fromid = request.POST["from_id"]
    toid = request.POST["to_id"]
    # lmid = request.POST["lastmsgid"]
    from django.db.models import Q

    res = chat_table.objects.filter(Q(FROMID_id=fromid, TOID_id=toid) | Q(FROMID_id=toid, TOID_id=fromid)).order_by('id')
    l = []

    for i in res:
        l.append({"id": i.id, "msg": i.message, "from": i.FROMID_id, "date": i.date, "to": i.TOID_id})

    return JsonResponse({"status":"ok",'data':l})



@login_required(login_url='/Myapp/login_get')
def ViewNotification(request):
    ob=notification_table.objects.filter(RENT__USER=User_table.objects.get(LOGIN__id=request.user.id))
    return render(request,'User/view notifications.html',{'data':ob})

@login_required(login_url='/Myapp/login_get')
def SendNotificationPost(request,id):
    notification=request.POST['notification']
    ob=notification_table()
    ob.notification=notification
    ob.date=datetime.today()
    ob.RENT_id=id
    ob.USER=User_table.objects.get(LOGIN__id=request.user.id)
    ob.save()
    return redirect('/Myapp/view_request/')


def ViewPayment(request):
    current_user = User_table.objects.get(LOGIN__id=request.user.id)

    # Payments made by the user (My Payments)
    sell = payment_table.objects.filter(REQUEST__USER=current_user)
    rent = rent_payment_table.objects.filter(RENT__USER=current_user)

    # Payments received by the user (owner of the book)
    sell_received = payment_table.objects.filter(REQUEST__BOOK__USER=current_user)
    rent_received = rent_payment_table.objects.filter(RENT__BOOK__USER=current_user)

    return render(request, 'User/View_payment.html', {
        'my_payments': sell,
        'my_rent_payments': rent,
        'received_payments': sell_received,
        'received_rent_payments': rent_received
    })



def LogOut(request):
    logout(request)
    return redirect('/Myapp/login_get')




