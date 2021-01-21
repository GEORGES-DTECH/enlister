
from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin,UserPassesTestMixin
from .models import Transaction
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse




# ======================TRANSACTIONS=======================================


class TransactionHomeView(LoginRequiredMixin,ListView):
    model = Transaction
    template_name = 'transactions/transactionshome.html'
    context_object_name = 'transactions'
    
    # def get_queryset(self):
        # enlister = self.request.user
        # queryset = Transaction.objects.filter(enlister=enlister)
        # return queryset
class AdminHomeView(LoginRequiredMixin,ListView):
    model = Transaction
    template_name = 'transactions/admin.html'
    context_object_name = 'transactions'

class AdminUserView(LoginRequiredMixin,ListView):
    model = User
    template_name = 'transactions/admin.html'
    context_object_name = 'users'
    paginate_by = 30
         

class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = 'transactions/transactionshome.html'
    fields = [
    'defaulters_name',
    'defaulters_phone',
    'defaulters_id_number',
    'default_amount',
 ]
 
    def form_valid(self, form):
        form.instance.enlister = self.request.user
        return super().form_valid(form)
   
class TransactionUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Transaction
    template_name = 'transactions/transactionshome.html'
    fields = [
    'defaulters_name',
    'defaulters_phone',
    'defaulters_id_number',
    'default_amount',
    ]

    def form_valid(self, form):
        form.instance.enlister = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        transaction=self.get_object()
        
        if self.request.user==transaction.enlister\
            or self.request.user.username == 'root'\
            or self.request.user.username == 'admin':
            return True
        else:
            return False    


class TransactionDeleteView(LoginRequiredMixin,UserPassesTestMixin,  DeleteView,):
    model = Transaction
    template_name = 'transactions/transaction_confirm_delete.html'
    context_object_name = 'transaction'
    success_url = reverse_lazy('reports_home')
    
    def test_func(self):
        transaction=self.get_object()
        
        if self.request.user==transaction.enlister\
            or self.request.user.username == 'root'\
            or self.request.user.username == 'admin':
            return True
        else:
            return False    
    



class ResultView(ListView):
    model = Transaction
    context_object_name = 'transaction'
    template_name = 'transactions/reports.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Transaction.objects.filter(
            Q(defaulters_id_number__icontains=query) | Q(defaulters_name__icontains=query) | Q(defaulters_phone__icontains=query))
        return object_list


class ReportHome(ListView):
    model = Transaction
    template_name = 'transactions/reports.html'
    context_object_name = 'reports'
    paginate_by=30
    ordering = ['-enlisting_date']
    
    
    
   
    

