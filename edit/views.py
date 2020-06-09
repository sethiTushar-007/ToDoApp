from django.shortcuts import render,redirect
from mainpage.models import Lists,MyLists,Lists_Dates
from .models import myList,myItem
from checklist.models import ListItems
from django.contrib import messages
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
# Create your views here.
def edit(request,id):
    
    if request.user.is_authenticated:
        user = request.user
        if request.method=='GET':
            list = Lists.objects.get(list_no=id)
            items = list.items
            mylists = MyLists.objects.get(email=user.email,list_no=id)
            listdates = Lists_Dates.objects.filter(list_no=id)
            if listdates:
                updatedon = listdates[0].updatedon
            else:
                updatedon = list.date
            if list.isshared:
                createdby = MyLists.objects.get(list_no=id,ishost=True).email
                if User.objects.filter(email=createdby).exists():
                    if createdby==user.email:
                        createdby='You'
                    else:
                        createdby=User.objects.get(email = createdby).first_name
                updatedby = listdates[0].updatedby
                if User.objects.filter(email=updatedby).exists():
                    if updatedby==user.email:
                        updatedby='You'
                    else:
                        updatedby = User.objects.get(email=updatedby).first_name

                if mylists.ishost:
                    my_list_info = myList(isshared=True,ishost=mylists.ishost,list_no=id,title=list.title,createdon=list.date.strftime('%d %b, %Y at %I:%M %p'),createdby=createdby,updatedon = updatedon.strftime('%d %b, %Y at %I:%M %p'),updatedby=updatedby)
                else:
                    my_list_info = myList(isshared=True,ishost=mylists.ishost,list_no=id,title=list.title,createdon=list.date.strftime('%d %b, %Y at %I:%M %p'),createdby=createdby,updatedon = updatedon.strftime('%d %b, %Y at %I:%M %p'),updatedby=updatedby)
            else:
                my_list_info = myList(isshared=False,ishost=True,list_no=id,title=list.title,createdon=list.date.strftime('%d %b, %Y at %I:%M %p'),updatedon=updatedon.strftime('%d %b, %Y at %I:%M %p'))

            my_items=[]
            i=1
            for item in items:
                if items.index(item)==0:
                    my_items.append(myItem(id=i,item=item,isFirst=True))
                else:
                    my_items.append(myItem(id=i,item=item))
                i+=1
            return render(request,'edit.html',{'info':my_list_info,'items':my_items,'new_id':i})
        else:
            lists_info = Lists.objects.get(list_no=id)
            lists_items = ListItems.objects.get(list_no=id)
            checked = []
            items_main = []
            for j in lists_items.items:
                items_main.append(j[0])
                checked.append(j[1])
            title = request.POST['title']
            items,items1 = [],[]
            i=1
            while 'item'+str(i) in request.POST:
                if request.POST['item'+str(i)]!='':
                    if request.POST['item'+str(i)] in items_main:
                        items1.append([request.POST['item'+str(i)],checked[items_main.index(request.POST['item'+str(i)])]])
                    else:
                        items1.append([request.POST['item'+str(i)],'notchecked'])
                    items.append(request.POST['item'+str(i)])
            
                i+=1

            saveddate = datetime.datetime.now() + datetime.timedelta(hours=5,minutes=30)
            savedby = user.email
            ishost = MyLists.objects.get(list_no=id,email=user.email).ishost
            Lists.objects.filter(list_no=id).update(title=title,items=items)
            ListItems.objects.filter(list_no=id).update(items=items1)
            Lists_Dates.objects.filter(list_no=id).update(updatedon=saveddate,updatedby=savedby)
            MyLists.objects.filter(list_no=id,email=savedby).delete()
            MyLists(list_no=id,email=savedby,ishost=ishost).save()
        
            messages.info(request,'List updated.')
            return redirect('/')
    else:
        return redirect('../../account/signin')

    





