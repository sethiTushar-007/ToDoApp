from django.shortcuts import render,redirect
from .models import Sharing,Share
from django.contrib import messages
from mainpage.models import Lists,MyLists
import datetime
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.auth.models import User
# Create your views here.
def share(request,id):
    user = request.user
    if request.user.is_authenticated:
        
        if request.method=='GET':
            title = ''
            lastsharedon = ''
            list = Lists.objects.get(list_no=id)
            title = list.title
            persons = []
            i=1
            if list.isshared:
                isnew=False
                list_of_shares = []
                shares = Sharing.objects.filter(list_no=id,host=user.email)
                for share in shares:
                    list_of_shares.append(share.sharedto)
            else:
                isnew=True
        
            if not isnew:
                for person in list_of_shares:
                    if i==1:
                        persons.append(Share(id=str(i),person=person,isFirst=True))
                    else:
                        persons.append(Share(id=str(i),person=person))
                    i+=1
            
            return render(request,'share.html',{'list_no':id,'title':title,'persons':persons,'new_id':i,'isnew':isnew})
        else:
            persons = []
            i=1
            while 'item'+str(i) in request.POST and request.POST['item'+str(i)]!='' :
                if request.POST['item'+str(i)]!=user.email:
                    persons.append(request.POST['item'+str(i)])
                i+=1
            if len(persons)==0:
                Lists.objects.filter(list_no=id).update(isshared=False)
            else:
                Lists.objects.filter(list_no=id).update(isshared=True)
            lastsharedon = datetime.datetime.now() + datetime.timedelta(hours=5,minutes=30)
            shares = Sharing.objects.filter(host=user.email,list_no=id)
            lastpersons = []
            mail_to_send_to = []
            for share in shares:
                lastpersons.append(share.sharedto)

            for lastperson in lastpersons:
                if not lastperson in persons:
                    Sharing.objects.filter(host=user.email,list_no=id,sharedto=lastperson).delete()
                    MyLists.objects.filter(email=lastperson,list_no=id).delete()
            
            message_content = []
            for person in persons:
                if User.objects.filter(email=person).exists():
                    message_content.append(person+' ('+User.objects.get(email=person).first_name+')')
                else:
                    message_content.append(person)
                if not Sharing.objects.filter(host=user.email,list_no=id,sharedto=person):
                    Sharing(list_no=id,host=user.email,sharedto=person,sharedon=lastsharedon).save()
                    mail_to_send_to.append(person)
                    MyLists(email=person,list_no=id,ishost=False).save()
            current_site = get_current_site(request)
            mail_subject = 'Checklist Shared'
            title = Lists.objects.get(list_no=id).title
            message1 = 'shared a list with you'
            message = render_to_string('alist_sharing.html',{'host_username':user.first_name,'host_email':user.email,'title':title,'domain':current_site.domain,'message':message1})
            from_email = settings.EMAIL_HOST_USER
            to_email = mail_to_send_to
            send_mail(mail_subject,message,from_email,to_email,fail_silently=True)
            messages.info(request,'List shared.')
            message3 = 'Sharing of the list (Title : '+title+') with the following people is successful.'
            message2 = render_to_string('alist_share_confirmation.html',{'name':user.first_name,'domain':current_site.domain,'message':message3,'content':message_content})
            send_mail('List sharing status',message2,from_email,[user.email],fail_silently=True)
            return redirect('../')
    else:
        return redirect('../../account/signin')