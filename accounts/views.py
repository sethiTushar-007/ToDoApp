from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import PendingEmailsVerify,PasswordEmailVerify
from mainpage.models import MyLists,Lists_Dates
from share.models import Sharing
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime
import random
from allauth.socialaccount.models import SocialAccount
# Password is hashed such that a character in their specific ascii range (lower case, upper case, numeric) is converted to the ascii(index-2),ascii(index+1),ascii(index+3) and #,@,! are added to create confusion.

def convertToHashpassword(name):
    name2 = list(name)
    name1 = []
    l,r = '',''
    for item in name2:
        no = ord(item)
        if item.isalpha():
            if item.isupper():
                l,r = 65,90
            else:
                l,r = 97,122
        else:
            l,r = 48,57
        first = no - 2
        second = no + 1
        third = no + 3
        if first<l:
            first = first - l + r + 1
        if second > r:
            second = second - r + l - 1
        if third>r:
            third = third - r + l - 1
        name1.extend([chr(first),chr(second),chr(third)])
    rand = random.randint(0,len(name1)-1)
    name1.insert(rand,'#')
    rand = random.randint(0,len(name1)-1)
    name1.insert(rand,'@')
    rand = random.randint(0,len(name1)-1)
    name1.insert(rand,'!')
    return ''.join(name1)

def convertToOriginalpassword(name):
    name = name.replace('#','')
    name = name.replace('@','')
    name = name.replace('!','')
    name1 = list(name)
    name2 = []
    i=0
    while i<len(name1):
        if name1[i].isalpha():
            if name[i].isupper():
                l,r = 65,90
            else:
                l,r=97,122
        else:
            l,r=48,57
        no = ord(name[i]) + 2
        if no>r:
            no = no - r + l - 1
        name2.append(chr(no))
        i+=3
    return ''.join(name2)

# Email-Id is hashed such that a character is converted to the ascii(index+2) if the index of the character in the email is even and ascii(index-1) if index of the character in the email is odd and #,@ are added to create confusion.

def convertToHashemail(name):
    name1 = list(name)
    name2 = []
    i = 0
    while i<len(name1):
        if i%2==0:
            name2.append(chr(ord(name1[i])+2))
        else:
            name2.append(chr(ord(name1[i])-1))
        i+=1
    rand = random.randint(0,len(name2)-1)
    name2.insert(rand,'#')
    rand = random.randint(0,len(name2)-1)
    name2.insert(rand,'@')
    return ''.join(name2)

def convertToOriginalemail(name):
    name = name.replace('#','')
    name = name.replace('@','')
    name1 = list(name)
    name2 = []
    i = 0
    while i<len(name1):
        if i%2==0:
            name2.append(chr(ord(name1[i])-2))
        else:
            name2.append(chr(ord(name1[i])+1))
        i+=1
    return ''.join(name2)

# Create your views here.
def login(request):
    email,password = '',''
    if request.method=='GET':
        if request.user.is_authenticated:
            return redirect('/')
        else:
            if request.COOKIES.get('ssetoken'):
                email = convertToOriginalemail(request.COOKIES['ssetoken'])
                password = convertToOriginalpassword(request.COOKIES['ssptoken'])
                if User.objects.filter(username=email).exists():
                    return render(request,'login.html',{'email':email,'password':password})
                else:
                    email = ''
                    password = ''
            return render(request,'login.html',{'email':email,'password':password})
            
            
    else:
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email,password=password)
        if user is not None:
            response = redirect('../')
            if 'remember' in request.POST:
                response.set_cookie('ssetoken',convertToHashemail(email),15552000)
                response.set_cookie('ssptoken',convertToHashpassword(password),15552000)
            else:
                if request.COOKIES.get('ssetoken'):
                    if convertToOriginalemail(request.COOKIES['ssetoken'])==email:
                        response.delete_cookie('ssetoken')
                        response.delete_cookie('ssptoken')
            if 'signedin' not in request.POST:
                request.session.set_expiry(0)

            auth.login(request,user)
            return response

        else:
            if PendingEmailsVerify.objects.filter(email=email):
                messages.info(request,'Email ID not verified. Register again.')
            else:
                messages.info(request,'Invalid Email ID or password.')
            return render(request,'login.html',{'email':email,'password':password})
 
def logout(request):
    auth.logout(request)
    return redirect('../account/signin')

def register(request):
    fname,email,password1,password2 = '','','',''
    if request.method=='GET':
        return render(request,'signup.html')
    else:
        fname = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['pass1']
        password2 = request.POST['pass2']
        if password1==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email ID already registered.')
                return redirect('../account/signin')
            else:
                no1 = str(datetime.now().timestamp()+(random.randint(1,9999)*1000)).split('.')
                no = str(int(no1[0])+int(no1[1]))
                current_site = get_current_site(request)
                mail_subject = 'Email Verification'
                message = render_to_string('activate_email.html',{'username':fname,'domain':current_site.domain,'id':no})
                from_email = settings.EMAIL_HOST_USER
                to_email = [email]
                send_mail(mail_subject,message,from_email,to_email,fail_silently=True)
                PendingEmailsVerify(no=no,email=email,fname=fname,password=password1).save()
                messages.info(request,'Email verification link has been sent to you email id.')
                return redirect('../account/signin')
        else:
            messages.info(request,'Passwords not matching...')
            return render(request,'signup.html',{'email':email,'password1':password1,'password2':password2,'username':fname})

def verify(request,id):
    pes = PendingEmailsVerify.objects.all()
    for pe in pes:
        if pe.no==id:
            if User.objects.filter(email=pe.email).exists():
                PendingEmailsVerify.objects.filter(email=pe.email).delete()
                return HttpResponse('Link is closed. Email ID already verified.')
            else:
                User.objects.create_user(first_name=pe.fname,username=pe.email,email=pe.email,password=pe.password).save()
                PendingEmailsVerify.objects.filter(email=pe.email).delete()
                messages.info(request,'Email verification completed. Registration successful.')
                return redirect('../../account/signin')
    else:
        return HttpResponse('Link is closed. Email ID already verified.')
                
def details(request):
    
    if request.user.is_authenticated :
        user = request.user
        if request.method=='GET':
            return render(request,'details.html')
           
        else:
            username = request.POST['username']
            user.first_name = username
            user.save()
            return redirect('/')
    else:
        return redirect('../../account/signin')

def changepassword(request):
    user = request.user
    no1 = str(datetime.now().timestamp()+(random.randint(1,9999)*1000)).split('.')
    no = str(int(no1[0])+int(no1[1]))
    PasswordEmailVerify(no=no,email=user.email).save()
    current_site = get_current_site(request)
    mail_subject = 'Reset Password'
    message = render_to_string('change_password.html',{'username':user.first_name,'domain':current_site.domain,'id':no})
    from_email = settings.EMAIL_HOST_USER
    to_email = [user.email]
    send_mail(mail_subject,message,from_email,to_email,fail_silently=True)
    messages.info(request,'Link to change your password has been sent to your registered mail id.')
    return redirect('../account/details')

def changepasswordverify(request,id):
    user = request.user
    if request.method=='GET':
        pes = PasswordEmailVerify.objects.all()
        for pe in pes:
            if pe.no==id:
                return render(request,'passwordchange.html')
        else:
            return HttpResponse('Link is closed.')
    else:
        newpassword1 = request.POST['newpassword1']
        newpassword2 = request.POST['newpassword2']
        pes = PasswordEmailVerify.objects.all()
        for pe in pes:
            if pe.no==id:
                if newpassword1==newpassword2:
                    user = User.objects.get(email=pe.email)
                    user.set_password(newpassword1)
                    user.save()
                    PasswordEmailVerify.objects.filter(email=pe.email).delete()
                    messages.info(request,'Success! Password updated.')
                    return redirect('../../account/signin')
                else:
                    messages.info(request,'Passwords not matching...')
                    return render(request,'passwordchange.html',{'newpassword1':newpassword1,'newpassword2':newpassword2})
                    
                
def emailsend(request):
    if request.method=='GET':
        return render(request,'onlyemail.html')
    else:
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            no1 = str(datetime.now().timestamp()+(random.randint(1,9999)*1000)).split('.')
            no = str(int(no1[0])+int(no1[1]))
            PasswordEmailVerify(no=no,email=email).save()
            current_site = get_current_site(request)
            mail_subject = 'Reset Password'
            user = User.objects.get(email=email)
            message = render_to_string('change_password.html',{'username':user.first_name,'domain':current_site.domain,'id':no})
            from_email = settings.EMAIL_HOST_USER
            to_email = [email]
            send_mail(mail_subject,message,from_email,to_email,fail_silently=True)
            messages.info(request,'Link to change your password has been sent to your registered mail id.')
            return redirect('../account/signin')
        else:
            messages.info(request,'Email ID not registered.')
            return redirect('../account/signup')

def deleteaccount(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method=='GET':
            return render(request,'onlyemail.html',{'fordelete':True})
        else:
            email = request.POST['email']
            if user.email==email:
                myl = MyLists.objects.filter(email=user.email)
                for my in myl:
                    id = my.list_no
                    if my.ishost:
                        MyLists.objects.filter(list_no=id).delete()
                        Sharing.objects.filter(list_no=id,host=user.email).delete()
                        Lists_Dates.objects.filter(list_no=id).delete()
                    else:
                        MyLists.objects.filter(email=user.email,list_no=id).delete()
                        Sharing.objects.filter(sharedto=user.email,list_no=id).delete()
                auth.logout(request)
                user.delete()
                response = redirect('../account/signin')
                if request.COOKIES.get('ssetoken'):
                    if convertToOriginalemail(request.COOKIES['ssetoken'])==email:
                        response.delete_cookie('ssetoken')
                        response.delete_cookie('ssptoken')
                messages.info(request,'Account deletion successful!')
                return response
            else:
                messages.info(request,'This is not your registered email ID.')
                return render(request,'onlyemail.html',{'fordelete':True,'email':email})
    else:
        return redirect('../../account/signin')
        
        


