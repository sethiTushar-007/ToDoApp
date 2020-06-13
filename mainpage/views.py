from django.shortcuts import render,redirect
from .models import Lists,myList,DeletedList,MyLists,Lists_Dates
from share.models import Sharing
from checklist.models import ListItems
import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
# Create your views here.

def main_screen(request):
    
    if request.user.is_authenticated:
        user = request.user
        if user.last_name!='':
            user.first_name = user.first_name + ' ' + user.last_name
            user.last_name = ''
            user.save()
        user.username = user.email
        user.save()
        mylists = MyLists.objects.filter(email=user.email)
        list_nos = []
        for mylist in mylists:
            lists = Lists.objects.get(list_no=mylist.list_no)
            if lists.isshared:
                if mylist.ishost:
                    share = Sharing.objects.filter(host=user.email,list_no=mylist.list_no)
                    list_nos.append(myList(isshared=True,ishost=True,list_no=mylist.list_no,title=lists.title,date=lists.date.strftime('%d %b, %Y at %I:%M %p'),sharedwith=len(share)))
                else:
                    share = Sharing.objects.filter(sharedto=user.email,list_no=mylist.list_no)
                    sharedby = share[0].host
                    if User.objects.filter(email=share[0].host).exists():
                        sharedby = User.objects.get(email=sharedby).first_name
                    list_nos.append(myList(isshared=True,ishost=False,list_no=mylist.list_no,title=lists.title,last_shared_date=share[0].sharedon.strftime('%d %b, %Y at %I:%M %p'),shared_by=sharedby))
            else:
                list_nos.append(myList(isshared=False,ishost=True,list_no=mylist.list_no,title=lists.title,date=lists.date.strftime('%d %b, %Y at %I:%M %p')))
        list_nos.reverse()
        return render(request,'mainpage.html',{'lists':list_nos})
    else:
        return redirect('../../account/signin')
def delete(request,id):
    lists = Lists.objects.get(list_no=id)
    title = lists.title.lower()
    entered_title = ''
    if request.user.is_authenticated:
        user = request.user
        if request.method=='GET':
            return render(request,'onlytitle.html',{'id':id,'list_title':title,'entered_title':entered_title})
        else:
            entered_title = request.POST['entered_title']
            if entered_title==title:
                myl = MyLists.objects.filter(email=user.email,list_no=id)
                for my in myl:
                    if my.ishost:
                        MyLists.objects.filter(list_no=id).delete()
                        DeletedList(list_no=id,delete_date = datetime.datetime.now()+datetime.timedelta(hours=5,minutes=30)).save()
                        Sharing.objects.filter(list_no=id,host=user.email).delete()
                        Lists_Dates.objects.filter(list_no=id).delete()
                    else:
                        MyLists.objects.filter(email=user.email,list_no=id).delete()
                        Sharing.objects.filter(sharedto=user.email,list_no=id).delete()
                
                messages.info(request,"List deleted.")
                return redirect('/')
            else:
                messages.info(request,'Enter the given text correctly.')
                return render(request,'onlytitle.html',{'id':id,'list_title':title,'entered_title':entered_title})
    else:
        return redirect('../../account/signin')
