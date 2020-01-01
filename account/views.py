from django.shortcuts import render, redirect
from .form import RegisterForm
from .models import UserProfile
from .form import ProfileUpdateForm
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializer import UserSerializer, ItemSerializer
from pages.models import Item 

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'account/register.html', {'form':form})
    else:
        return render(request, 'account/register.html', {'form':form})
def profile(request):
    if request.method == 'POST':
        updateform = ProfileUpdateForm(request.POST,request.FILES, instance = request.user.userprofile)
        if updateform.is_valid():
            updateform.save()
            return redirect('profile')
        updateform= ProfileUpdateForm()
        context = {
            'updateform':updateform
        }
        return render(request, 'account/profile.html',context)
        return render('profile')   
    else:
        updateform= ProfileUpdateForm()
        context = {
            'updateform':updateform
        }
        return render(request, 'account/profile.html',context)
    
# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

