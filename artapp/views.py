from datetime import timezone
from pprint import pprint
import random

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.datetime_safe import datetime

from artapp.models import *


def main(request):
    return render(request, 'loginIndex.html')

def userReg(request):

    return render(request, 'UserRegisterIndex.html')

def usrRegistration(request):
    try:
        fname = request.POST['fname']
        lname = request.POST['lname']
        age = request.POST['age']
        phone = request.POST['tel']
        place = request.POST['place']
        post = request.POST['post']
        pin = request.POST['pin']
        gender = request.POST['radio']
        email = request.POST['email']
        username = request.POST['uname']
        password = request.POST['password']
        # to save username and password to login
        lob = login()
        lob.username = username
        lob.password = password
        lob.type = 'user'
        lob.save()
        # save to  database
        uob = user()
        uob.fname = fname
        uob.lname = lname
        uob.age = age
        uob.phone = phone
        uob.place = place
        uob.post = post
        uob.pin = pin
        uob.gender = gender
        uob.email = email
        uob.lid = lob
        uob.save()
        return HttpResponse('''<script>alert("user registered successfully");window.location='/'</script>''')
    except:
        messages.success(request, 'Username already exist')
        return HttpResponse('''<script>alert("Username already exist");window.location='/userReg'</script>''')

def log(request):
    username = request.POST['uname']
    password = request.POST['password']
    try:
        logOb = login.objects.get(username=username, password=password)
        if logOb.type == 'admin':
            request.session['lid'] = logOb.id
            ob1 = auth.authenticate(username='admin', password='admin')  # for login authentication
            auth.login(request, ob1)  # for login authentication
            return HttpResponse('''<script>alert("welcome admin");window.location='/adminHome'</script>''')
        elif logOb.type == 'user':
            request.session['lid'] = logOb.id
            ob1 = auth.authenticate(username='admin', password='admin')  # for login authentication
            auth.login(request, ob1)  # for login authentication
            user_name = logOb.username
            print(user_name)
            alert_message = f"welcome, {user_name}!"
            response_text = f"<script>alert('{alert_message}');window.location='/userHome'</script>"
            # return HttpResponse('''<script>alert('welcome hospital');window.location='/hospitalHome'</script>''')

            return HttpResponse(response_text)
        elif logOb.type == 'artist':
            request.session['lid'] = logOb.id
            ob1 = auth.authenticate(username='admin', password='admin')  # for login authentication
            auth.login(request, ob1)  # for login authentication
            user_name = logOb.username
            alert_message = "welcome, %s!" % user_name
            response_text = "<script>alert('{}');window.location='/artistHome'</script>".format(alert_message)

            return HttpResponse(response_text)
        else:
            return HttpResponse('''<script>alert("invalid username or password ");window.location='/'</script>''')
    except:
        return HttpResponse('''<script>alert("invalid username or password ");window.location='/'</script>''')

###################### admin #################

@login_required(login_url='/') #for login authentication
def adminHome(request):
    return  render(request, 'adminIndex.html')

@login_required(login_url='/') #for login authentication
def manageArtist(request):
    ob = artist.objects.all()
    return render(request, 'admin/manageArtists.html',{'val':ob})

@login_required(login_url='/') #for login authentication
def addArtists(request):

    return render(request,'admin/addArtists.html')

@login_required(login_url='/') #for login authentication
def addArtist(request):
    try:
        artistName = request.POST['name']
        age = request.POST['age']
        joiningDate = request.POST['date']
        workExperience = request.POST['number2']
        gender = request.POST['radio']
        address = request.POST['textarea']
        phone = request.POST['tel']
        username = request.POST['uname']
        password = request.POST['password']
        lob = login()
        lob.username = username
        lob.password = password
        lob.type = 'artist'
        lob.save()
        ob = artist()
        ob.name = artistName
        ob.age = age
        ob.joining_date = joiningDate
        ob.work_experience = workExperience
        ob.gender = gender
        ob.address = address
        ob.phone = phone
        ob.lid = lob
        ob.save()
        return HttpResponse('''<script>alert("artist Added ");window.location='/manageArtist'</script>''')
    except:
        messages.success(request, 'Username already exist')
        return HttpResponse('''<script>alert("artist username already exist");window.location='/manageArtist'</script>''')


def editArtist(request,id):
    ob = artist.objects.get(id=id)
    request.session['arid'] = id
    return render(request, 'admin/editArtists.html',{'val':ob})

@login_required(login_url='/') #for login authentication
def updateArtist(request):
    Artistname = request.POST['name']
    age = request.POST['age']
    joiningDate = request.POST['date']
    workExperience = request.POST['number2']
    gender = request.POST['radio']
    address = request.POST['textarea']
    phone = request.POST['tel']
    ob = artist.objects.get(id=request.session['arid'])
    ob.name = Artistname
    ob.age = age
    ob.gender = gender
    ob.phone = phone
    ob.address = address
    ob.joining_date = joiningDate
    ob.work_experience = workExperience
    ob.save()
    return HttpResponse('''<script>alert("artist updated");window.location='/manageArtist'</script>''')

@login_required(login_url='/') #for login authentication
def delArtist(request,id):
    ob = artist.objects.get(lid__id=id)
    ob.delete()
    lob = login.objects.get(id=id)
    lob.delete()
    return HttpResponse('''<script>alert("artist deleted");window.location='/manageArtist'</script>''')


@login_required(login_url='/') #for login authentication
def updtPriceAvailOfArtWork(request):
    ob = artwork.objects.all()
    return render(request, 'admin/UPDATE_PRICE_AVAIL_OF_ARTWRK.html',{'val':ob})

@login_required(login_url='/') #for login authentication
def updatePriceAvail(request,id):
    ob = artwork.objects.get(id=id)
    request.session['awid'] = id
    return render(request, 'admin/UPDATE_PRICE_AVAIL.html',{'val':ob})

@login_required(login_url='/') #for login authentication
def updPrAv(request):
    price = request.POST['number']
    availability = request.POST['select']
    ob = artwork.objects.get(id=request.session['awid'])
    ob.price = price
    ob.availability = availability
    ob.save()
    return HttpResponse('''<script>alert("artwork update");window.location='/updtPriceAvailOfArtWork'</script>''')

@login_required(login_url='/') #for login authentication
def viewCustomerOrder(request):
    ob = artworkOrder.objects.all()
    return render(request, 'admin/VIEW_CUSTOMER_ORDERS.html',{'val':ob})

@login_required(login_url='/') #for login authentication
def viewArtworkPutSale(request):
    ob = artworkSellReq.objects.all()
    return render(request, 'admin/VIEW_ARTIST_ARTWORK_PUT_SALE.html',{'val':ob})

@login_required(login_url='/') #for login authentication
def putForsale(request,id):
    ob = artworkSellReq.objects.get(id=id)
    ob.status = 'on_sale'
    ob.date = datetime.today()
    ob.save()
    return HttpResponse('''<script>alert("artwork put on sale");window.location='/viewArtworkPutSale'</script>''')


def orderFilter(request):
    ob = artworkOrder.objects.all()
    return render(request,'admin/artworkOrderFilter.html',{'val':ob})

def dateFilter(request):
    try:
        dateFrom = request.POST['date']
        dateTo = request.POST['date2']
        from_date = datetime.strptime(dateFrom, '%Y-%m-%d').date()
        to_date = datetime.strptime(dateTo, '%Y-%m-%d').date()
        orders = artworkOrder.objects.filter(date__range=[from_date, to_date])
        pprint('///////////////////////////')
        pprint(orders)
        pprint('///////////////////////////')

        ob = []
        for i in orders:
            ob.append({
                'uid': i.uid,
                'awid': i.awid,
                'date': i.date,
                'staus': i.staus,
            })
        pprint('/////////////')
        pprint(ob)
        pprint('/////////////')
        return render(request, 'admin/artworkOrderFilter.html', {'val2': ob, 'start_date':dateFrom, 'end_date':dateTo})
    except:
        return render(request, 'admin/artworkOrderFilter.html')



############### ARTISTS ##########################
@login_required(login_url='/') #for login authentication
def artistHome(request):
    return render(request,'artistIndex.html')

@login_required(login_url='/') #for login authentication
def manageArtwork(request):
    ob = artwork.objects.all()
    return render(request, 'ARTISTS/MANGE_ARTWORK.html',{'val':ob})

@login_required(login_url='/') #for login authentication
def addArtwork(request):

    return render(request, 'ARTISTS/ADD_ARTWORK.html')

@login_required(login_url='/') #for login authentication
def add_artwork(request):
    ArtWorkname = request.POST['textfield']
    price = request.POST['number']
    availability = request.POST['select']
    img = request.FILES['fileField']
    Fp = FileSystemStorage()
    Fs = Fp.save(img.name, img)
    desc = request.POST['textarea']
    dateCreated = datetime.today()
    ob = artwork()
    ob.name = ArtWorkname
    ob.price = price
    ob.availability = availability
    ob.image = Fs
    ob.description = desc
    ob.date_created = dateCreated
    ob.aid = artist.objects.get(lid__id=request.session['lid'])
    ob.save()
    return HttpResponse('''<script>alert("artwork added");window.location='/manageArtwork'</script>''')

@login_required(login_url='/') #for login authentication
def editArtwork(request,id):
    ob = artwork.objects.get(id=id)
    request.session['awrid'] = id
    return render(request, 'ARTISTS/EDIT_ARTWORK.html',{'val':ob})

@login_required(login_url='/') #for login authentication
def updateArtWork(request):
    try:
        ArtWorkname = request.POST['textfield']
        price = request.POST['number']
        availability = request.POST['select']
        img = request.FILES['fileField']
        Fp = FileSystemStorage()
        Fs = Fp.save(img.name, img)
        desc = request.POST['textarea']
        dateCreated = datetime.today()
        ob= artwork.objects.get(id=request.session['awrid'])
        ob.name = ArtWorkname
        ob.price = price
        ob.availability = availability
        ob.image = Fs
        ob.description = desc
        ob.date_created = dateCreated
        ob.aid = artist.objects.get(lid__id=request.session['lid'])
        ob.save()
        return HttpResponse('''<script>alert("artwork updated");window.location='/manageArtwork'</script>''')
    except:
        ArtWorkname = request.POST['textfield']
        price = request.POST['number']
        availability = request.POST['select']
        # img = request.FILES['fileField']
        # Fp = FileSystemStorage()
        # Fs = Fp.save(img.name, img)
        desc = request.POST['textarea']
        dateCreated = datetime.today()
        ob = artwork.objects.get(id=request.session['awrid'])
        ob.name = ArtWorkname
        ob.price = price
        ob.availability = availability
        # ob.image = Fs
        ob.description = desc
        ob.date_created = dateCreated
        ob.aid = artist.objects.get(lid__id=request.session['lid'])
        ob.save()
        return HttpResponse('''<script>alert("artwork updated");window.location='/manageArtwork'</script>''')

@login_required(login_url='/') #for login authentication
def viewArtwrkReqandUpdtStats(request):
    ob = customerArtworkReq.objects.all()
    return render(request, 'ARTISTS/VIEW_ARTWORK_REQ_APPROVAL.html',{'val':ob})

@login_required(login_url='/') #for login authentication
def acceptReq(request,id):
    ob = customerArtworkReq.objects.get(id=id)
    ob.staus = 'approved'
    ob.save()
    return HttpResponse('''<script>alert("approved");window.location='/viewArtwrkReqandUpdtStats'</script>''')

@login_required(login_url='/') #for login authentication
def rejectReq(request,id):
    ob = customerArtworkReq.objects.get(id=id)
    ob.staus = 'rejected'
    ob.save()
    return HttpResponse('''<script>alert("rejected");window.location='/viewArtwrkReqandUpdtStats'</script>''')

@login_required(login_url='/') #for login authentication
def srchOrdersApprvl(request):
    ob = artworkOrder.objects.all()
    return render(request, 'ARTISTS/SEARCH_ORDER_APPROVAL.html',{'val':ob})

@login_required(login_url='/') #for login authentication
def srchOrderUser(request):
    Cust = request.POST['select']
    ob = artworkOrder.objects.filter(id=Cust)
    aob = artworkOrder.objects.all()
    return render(request, 'ARTISTS/SEARCH_ORDER_APPROVAL.html', {'val2': ob,'val':aob,'s':Cust})

@login_required(login_url='/') #for login authentication
def apprvOrder(request,id):
    ob = artworkOrder.objects.get(id=id)
    ob.staus = "approved"
    ob.save()
    return HttpResponse('''<script>alert("order approved");window.location='/srchOrdersApprvl'</script>''')

@login_required(login_url='/') #for login authentication
def rejectOrder(request,id):
    ob = artworkOrder.objects.get(id=id)
    ob.staus = "rejected"
    ob.save()
    return HttpResponse('''<script>alert("order rejected");window.location='/srchOrdersApprvl'</script>''')

@login_required(login_url='/') #for login authentication
def artwork_sell_req(request):
    aid = artist.objects.get(lid__id=request.session['lid'])
    ob = artwork.objects.filter(aid=aid)
    # aob = artworkSellReq.objects.all()
    return render(request, 'ARTISTS/ARTWORK_TO_SELL_REQ.html',{'val':ob})

# def sellReq(request,id):
#     aob = artwork.objects.get(id=id)
#     ob = artworkSellReq.objects.filter(awid=aob)
#     ob.aid = artist.objects.get(lid__id=request.session['lid'])
#     ob.date = datetime.today()
#     ob.status = 'requested'
#     ob.save()
#     return HttpResponse('''<script>alert("sell request sent");window.location='/artwork_sell_req'</script>''')

@login_required(login_url='/') #for login authentication
def sellReq(request, id):
    aob = artwork.objects.get(id=id)
    artist_id = request.session['lid']
    artworkSellReq.objects.create(
        awid=aob,
        aid_id=artist.objects.get(lid__id=artist_id).id,
        date=datetime.today(),
        status='requested'
    )
    return HttpResponse('''<script>alert("sell request sent");window.location='/artwork_sell_req'</script>''')

######################### USERS ##########################

@login_required(login_url='/') #for login authentication
def userHome(request):
    return render(request, 'userIndex.html')

@login_required(login_url='/') #for login authentication
def addWorkReq(request):
    uob = user.objects.get(lid__id=request.session['lid'])
    ob = customerArtworkReq.objects.filter(uid=uob)
    return render(request, 'USER/SENT_WORK_REQ.html',{'val':ob})

@login_required(login_url='/') #for login authentication
def sentWorkReq(request):

    return render(request, 'USER/ADDWORK_REQ.html')

@login_required(login_url='/') #for login authentication
def sent_work_req(request):
    artworkName = request.POST['textfield']
    desc = request.POST['textarea']
    ob = customerArtworkReq()
    ob.name = artworkName
    ob.description = desc
    ob.staus = 'pending'
    ob.uid = user.objects.get(lid__id=request.session['lid'])
    ob.save()
    return HttpResponse('''<script>alert("request sent");window.location='/addWorkReq'</script>''')

@login_required(login_url='/') #for login authentication
def viewArtworkAndorder(request):
    ob = artwork.objects.all()
    return render(request, 'USER/VIEW_ARTWORK_ORDER.html',{'val':ob})

@login_required(login_url='/') #for login authentication
def order(request,id):
    awob = artwork.objects.get(id=id)
    ob = artworkOrder.objects.create(
        awid=awob,
        uid=user.objects.get(lid__id=request.session['lid']),
        date=datetime.today(),
        staus='ordered'
    )
    return HttpResponse('''<script>alert("ArtWork ordered");window.location='/viewArtworkAndorder'</script>''')


@login_required(login_url='/') #for login authentication
def viewArtworkAndPurchase(request):
    ob = artwork.objects.all()

    return render(request, 'USER/VIEW_ARTWORK_PUCHASE.html',{'val':ob})

@login_required(login_url='/') #for login authentication
def purchase(request,id):
    awob = artwork.objects.get(id=id)
    ob = artworkSellReq.objects.create(
        awid= awob,
        aid=awob.aid,
        date = datetime.today(),
        status = 'purchased'
    )

    return HttpResponse('''<script>alert("ArtWork purchased");window.location='/viewArtworkAndPurchase'</script>''')

def forgotPass(request):
    return render(request,'forgotPassIndex.html')

def password_reset(request):
    uname = request.POST['uname']
    mail = request.POST['email']
    try:
        g = login.objects.get(username=uname)
        pprint('/////////////')
        pprint(g)
        pprint('/////////////')
        if g is not None:
            a = random.randint(0000, 9999)
            g.password = (str(a))
            g.save()
            send_mail('forgot password ', "YOUR NEW PASSWORD IS  -" + str(a), 'yadhusample1998@gmail.com', [mail],fail_silently=False)
            return HttpResponse('''<script>alert("Password sent to your registered email address !!!");window.location='/'</script>''')
            # return redirect('/')
        else:
            print('error==========')
            return HttpResponse(
                '''<script>alert("Invalid Username or Email Address!!!");window.location='/forgotPass'</script>''')
            # return HttpResponse('''<script>alert("Invalid Username or Email Adress!!!")</script>''')
            # return redirect('forgotPass')
    except:
        return HttpResponse(
            '''<script>alert("Invalid Username or Email Address!!!");window.location='/forgotPass'</script>''')

def logout(request):
    auth.logout(request)
    return redirect('/')
################## ADMIN ##################################
def changePassword(request):
    return render(request,'admin/ADMIN_CHANGE_PASSWORD.html')

def change_password(request):
    username = request.POST['uname']
    old_password = request.POST['password']
    new_password = request.POST['password3']
    confirm_password = request.POST['password2']
    # Check if the username and old password are correct
    try:
        # Check if the username and old password are correct
        user = login.objects.get(username=username, password=old_password)
    except:
        return HttpResponse('Invalid username or old password')

    # if not user:
    #     return HttpResponse('Invalid username or old password')

    # Check if the user is admin
    if user.type != 'admin':
        return HttpResponse('Only admins password can change ')

    # Check if the new password and confirm password match
    if new_password != confirm_password:
        return HttpResponse('New password and confirm password do not match')

    # Update the user's password
    user.password = new_password
    user.save()

    # Redirect to a success page
    return HttpResponse('''<script>alert("PASSWORD_CHANGE_SUCCESSFULLY");window.location='/changePassword'</script>''')

###################### ARTISTS ###########################

def changeArtistPassword(request):
    return render(request,'ARTISTS/ARTIST_CHANGE_PASWWORD.html')

def change_Artist_password(request):
    username = request.POST['uname']
    old_password = request.POST['password']
    new_password = request.POST['password3']
    confirm_password = request.POST['password2']
    # Check if the username and old password are correct
    try:
        # Check if the username and old password are correct
        user = login.objects.get(username=username, password=old_password)
    except:
        return HttpResponse('Invalid username or old password')

    # if not user:
    #     return HttpResponse('Invalid username or old password')

    # Check if the user is admin
    if user.type != 'artist':
        return HttpResponse('Only artist password can change ')

    # Check if the new password and confirm password match
    if new_password != confirm_password:
        return HttpResponse('New password and confirm password do not match')

    # Update the user's password
    user.password = new_password
    user.save()

    # alert to a success page
    return HttpResponse('''<script>alert("PASSWORD_CHANGE_SUCCESSFULL");window.location='/changeArtistPassword'</script>''')

######################## user #####################33

def changeUserPassword(request):
    user_id = request.session.get('lid')
    lob = login.objects.get(id=user_id)
    return render(request,'USER/changeUserPassword.html',{'val':lob})



def change_user_password(request):
    if request.method == 'POST':
        username = request.POST['uname']
        old_password = request.POST['password']
        new_password = request.POST['password3']
        confirm_password = request.POST['password2']

        # Retrieve the currently logged-in user's ID from the session



        try:
            user_id = request.session.get('lid')
        except:
            return HttpResponse('Invalid username')

        # if not user_id:
        #     return redirect('login')  # Redirect to login page if user is not logged in

        # Retrieve the login object for the currently logged-in user
        lob = login.objects.get(id=user_id)

        # Check if the old password provided by the user matches the password stored in the database
        if lob.password != old_password:
            return HttpResponse('Invalid old password')

        # Check if the new password and confirm password match
        if new_password != confirm_password:
            return HttpResponse('New password and confirm password do not match')

        # Update the user's password
        lob.password = new_password
        lob.save()

        # alert to a success page
        return HttpResponse('''<script>alert("PASSWORD_CHANGE_SUCCESSFULL");window.location='/changeUserPassword'</script>''')



# def change_User_password(request):
#     username = request.POST['uname']
#     old_password = request.POST['password']
#     new_password = request.POST['password3']
#     confirm_password = request.POST['password2']
#     # Check if the username and old password are correct
#     try:
#         # Check if the username and old password are correct
#         user = login.objects.get(username=username, password=old_password)
#     except:
#         return HttpResponse('Invalid username or old password')
#
#     # if not user:
#     #     return HttpResponse('Invalid username or old password')
#
#     # Check if the user is admin
#     if user.type != 'user':
#         return HttpResponse('Only user password can change ')
#
#     # Check if the new password and confirm password match
#     if new_password != confirm_password:
#         return HttpResponse('New password and confirm password do not match')
#
#     # Update the user's password
#     user.password = new_password
#     user.save()
#
#     # alert to a success page
#     return HttpResponse('''<script>alert("PASSWORD_CHANGE_SUCCESSFULLY");window.location='/changePassword'</script>''')


# from django.contrib.auth.hashers import make_password
# from django.contrib.auth.models import User
# from django.shortcuts import render, redirect
# from django.http import HttpResponse
#
#
# def change_password(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         old_password = request.POST.get('old_password')
#         new_password = request.POST.get('new_password')
#         confirm_password = request.POST.get('confirm_password')
#
#         # Check if the username and old password are correct
#         user = User.objects.get(username=username)
#         if not user.check_password(old_password):
#             return HttpResponse('Invalid username or old password')
#
#         # Check if the new password and confirm password match
#         if new_password != confirm_password:
#             return HttpResponse('New password and confirm password do not match')
#
#         # Update the user's password
#         user.password = make_password(new_password)
#         user.save()
#
#         # Redirect to a success page
#         return redirect('change_password_success')
#
#     return render(request, 'change_password.html')


# from django.contrib.auth.hashers import make_password
# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from myapp.models import login


# def change_password(request):
#     if request.method == 'POST':
#         username = request.POST.get('uname')
#         old_password = request.POST.get('password')
#         new_password = request.POST.get('password3')
#         confirm_password = request.POST.get('password2')
#
#         # Check if the username and old password are correct
#         user = login.objects.get(username=username, password=old_password)
#         if not user:
#             return HttpResponse('Invalid username or old password')
#
#         # Check if the new password and confirm password match
#         if new_password != confirm_password:
#             return HttpResponse('New password and confirm password do not match')
#
#         # Update the user's password
#         user.password = make_password(new_password)
#         user.save()
#
#         # Redirect to a success page
#         return redirect('change_password_success')
#
#     return render(request, 'change_password.html')


# from django.contrib.auth.hashers import make_password
# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from myapp.models import login
#
#
# def change_password(request):
#     if request.method == 'POST':
#         username = request.POST.get('uname')
#         old_password = request.POST.get('password')
#         new_password = request.POST.get('password3')
#         confirm_password = request.POST.get('password2')
#
#         # Check if the username and old password are correct
#         user = login.objects.get(username=username, password=old_password)
#         if not user:
#             return HttpResponse('Invalid username or old password')
#
#         # Check if the new password and confirm password match
#         if new_password != confirm_password:
#             return HttpResponse('New password and confirm password do not match')
#
#         # Check if the user is admin
#         if user.type != 'admin':
#             return HttpResponse('Only admin can change password')
#
#         # Update the user's password
#         user.password = make_password(new_password)
#         user.save()
#
#         # Redirect to a success page
#         return redirect('change_password_success')
#
#     return render(request, 'change_password.html')




