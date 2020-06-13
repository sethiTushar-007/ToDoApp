from django.urls import path
from .import views

urlpatterns = [
    path('signin',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('signup',views.register,name='register'),
    path('details',views.details,name='details'),
    path('verify/<slug:id>',views.verify,name='verify'),
    path('change-password',views.changepassword,name='changepassword'),
    path('change-password/<slug:id>',views.changepasswordverify,name='changepasswordverify'),
    path('email',views.emailsend,name='emailsend'),
    path('delete-my-account',views.deleteaccount,name='deleteaccount')
]