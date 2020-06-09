from django.shortcuts import render,redirect
from mainpage.models import Lists,MyLists,Lists_Dates
from checklist.models import ListItems
from django.contrib import messages
import time
import datetime
import random
from django.utils import timezone
# Create your views here.
def newlist(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request,'newlist.html')
    else:
        return redirect('../../account/signin')

def listsave(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method=='POST':
            title = request.POST['title']
            items,items1 = [],[]
            i=1
            while 'item'+str(i) in request.POST and request.POST['item'+str(i)]!='' :
                items.append(request.POST['item'+str(i)])
                items1.append([request.POST['item'+str(i)],'notchecked'])
                i+=1
            no1 = str(datetime.datetime.now().timestamp()+(random.randint(1,9999)*1000)).split('.')
            listno = str(int(no1[0])+int(no1[1]))
            date = datetime.datetime.now() + datetime.timedelta(hours=5,minutes=30)
            saveddate = date
            Lists(list_no=listno,date=date,title=title,items=items).save()
            MyLists(email=user.email,list_no=listno,ishost=True).save()
            ListItems(list_no=listno,lastsavedon=saveddate,lastsavedby=user.email,items=items1).save()
            Lists_Dates(list_no=listno,updatedon=date,updatedby=user.email).save()
            messages.info(request,'List created.')
            return redirect('../')
    else:
        return redirect('../../account/signin')

