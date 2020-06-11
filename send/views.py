from django.shortcuts import render,redirect
from django.contrib import messages
from mainpage.models import Lists,MyLists,Lists_Dates
from checklist.models import ListItems
import datetime
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
import random
from django.contrib.auth.models import User
from django.utils import timezone
# Create your views here.
def share(request,id):
    user = request.user
    if request.user.is_authenticated:
        
        if request.method=='GET':
            title = ''
            list = Lists.objects.get(list_no=id)
            title = list.title
            return render(request,'send.html',{'title':title})
        else:
            persons = []
            i=1
            while 'item'+str(i) in request.POST and request.POST['item'+str(i)]!='' :
                if request.POST['item'+str(i)]!=user.email:
                    persons.append(request.POST['item'+str(i)])
                i+=1
            title = Lists.objects.get(list_no=id).title
            message_content = []
            for person in persons:
                if User.objects.filter(email=person).exists():
                    message_content.append(person+' ('+User.objects.get(email=person).first_name+')')
                else:
                    message_content.append(person)
                no1 = str(datetime.datetime.now().timestamp()+(random.randint(1,9999)*random.randint(1,8888))).split('.')
                listno = str(int(no1[0])+int(no1[1]))
                date = datetime.datetime.now() + datetime.timedelta(hours=5,minutes=30)
                saveddate = date

                Lists(list_no=listno,date=date,title=title,items=Lists.objects.get(list_no=id).items).save()
                MyLists(email=person,list_no=listno,ishost=True).save()
                ListItems(list_no=listno,lastsavedon=saveddate,lastsavedby=person,items=ListItems.objects.get(list_no=id).items).save()
                Lists_Dates(list_no=listno,updatedon=date,updatedby=person).save()
            current_site = get_current_site(request)
            mail_subject = 'Checklist : '+title
            message1 = 'sent a list to you'
            message = render_to_string('alist_sharing.html',{'host_username':user.first_name,'host_email':user.email,'title':title,'domain':current_site.domain,'message':message1})
            from_email = settings.EMAIL_HOST_USER
            to_email = persons
            send_mail(mail_subject,message,from_email,to_email,fail_silently=True)
            messages.info(request,'List sent.')
            message3 = 'Sending of the list (Title : '+title+') to the following people is successful.'
            message2 = render_to_string('alist_share_confirmation.html',{'name':user.first_name,'title':title,'domain':current_site.domain,'message':message3,'content':message_content})
            send_mail('List sending status',message2,from_email,[user.email],fail_silently=True)
            return redirect('../')
    else:
        return redirect('../../account/signin')