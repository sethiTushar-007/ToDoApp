from django.shortcuts import render,redirect
from mainpage.models import Lists,MyLists,DeletedList,Lists_Dates
import datetime
from .models import myList,Item,ListItems
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
# Create your views here.
def checklist(request,id):
    user = request.user
    if request.user.is_authenticated:
        lists = Lists.objects.get(list_no=id)
        mylists = MyLists.objects.get(list_no=id,email=user.email)
        listitems = ListItems.objects.get(list_no=id)
        listdates = Lists_Dates.objects.filter(list_no=id)
        item = listitems.items
        if request.method=='GET':
            
            saveddate = listitems.lastsavedon.strftime('%d %b, %Y at %I:%M %p')
            if listdates:
                updatedon = listdates[0].updatedon
            else:
                updatedon = lists.date
            if lists.isshared:
                savedby = listitems.lastsavedby
                if User.objects.filter(email=savedby).exists():
                    if savedby==user.email:
                        savedby='You'
                    else:
                        savedby = User.objects.get(email=savedby).first_name
                list_info = myList(isshared=True,ishost=mylists.ishost,list_no=id,title=lists.title,date=updatedon.strftime('%d %b, %Y at %I:%M %p'),saveddate=saveddate,savedby=savedby)
            else:
                list_info = myList(isshared=False,ishost=True,list_no=id,title=lists.title,date=lists.date.strftime('%d %b, %Y at %I:%M %p'),saveddate=saveddate)
        
            items_list = []
            i = 1
            for it in item:
                if it[1]=='ischecked':
                    items_list.append(Item(id=i,item=it[0],ischecked=True))
                elif it[1]=='notchecked':
                    items_list.append(Item(id=i,item=it[0],ischecked=False))
                i+=1
            
            return render(request,'checklist.html',{'info':list_info,'items':items_list})

        else:
            i=1
            new_list = []
            date = datetime.datetime.now() + datetime.timedelta(hours=5,minutes=30)
            is_checked = request.POST
            for it in item:
                if 'item-'+str(i)+' ' in is_checked or 'item-'+str(i) in is_checked:
                    new_list.append([it[0],'ischecked'])
                else:
                    new_list.append([it[0],'notchecked'])
                i+=1
            ListItems.objects.filter(list_no=id).update(lastsavedon=date,lastsavedby=user.email,items=new_list)
            messages.info(request,'Checklist saved.')
            return redirect('../checklist/'+id)
    else:
        return redirect('../../account/signin')

            
    