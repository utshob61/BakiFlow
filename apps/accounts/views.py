from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from apps.businesses.models import Business, BusinessMember
from django.utils.text import slugify
from django.db import transaction

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                business_name = form.cleaned_data.get('business_name')
                
                # Create Business
                business = Business.objects.create(
                    name=business_name,
                    slug=slugify(business_name),
                    owner=user
                )
                
                # Create Membership
                BusinessMember.objects.create(
                    business=business,
                    user=user,
                    role='OWNER'
                )
                
                login(request, user)
                return redirect('dashboard')
    else:
        form = RegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})
