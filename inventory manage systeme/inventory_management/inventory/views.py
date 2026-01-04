from typing import Self
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View,CreateView,UpdateView,DeleteView
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm,InventoryItemForm
from .models import  InventoryItem
from inventory_management.settings import LOW_QUANTITY
from django.contrib import messages

class Index(TemplateView):
    template_name = 'inventory/index.html'
    
    
class Dashboard(LoginRequiredMixin,View):
    def get(self, request):
        items = InventoryItem.objects.filter(user=self.request.user.id).order_by('-date_creation')
        return render(request, 'inventory/dashboard.html', {'items': items})
    
    
class signUpView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'inventory/signup.html', {'form': form})
        
    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            return redirect('index')
        return render(request, 'inventory/signup.html', {'form': form})
class logoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('index')  # Redirect to home page
    
    def post(self, request):
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('index')
    

class AddItem(CreateView,LoginRequiredMixin):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Item ajouté avec succès!')
        return super().form_valid(form)

class EditItem(UpdateView,LoginRequiredMixin):
    model=InventoryItem
    form_class=InventoryItemForm
    template_name='inventory/item_form.html'
    success_url=reverse_lazy('dashboard')
    
    
class DeleteItem(LoginRequiredMixin,DeleteView):
    model=InventoryItem
    template_name='inventory/delete_item.html'
    success_url=reverse_lazy('dashboard')
    context_object_name='item'