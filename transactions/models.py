from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.functional import cached_property
from django.db.models import Sum,Count
from django.utils import timezone
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import calendar

class Transaction(models.Model):
    enlisting_date=models.DateTimeField(default=timezone.now)
    defaulters_name=models.CharField(max_length=200)
    defaulters_phone=models.CharField(max_length=200)
    defaulters_id_number=models.CharField(max_length=20)
    default_amount=models.IntegerField(default=0)
    enlister=models.ForeignKey(User,on_delete=models.CASCADE)

    

    def __str__(self):
        return self.enlisting_company

    def get_absolute_url(self):
        return reverse("reports_home")    

    @cached_property
    def the_date_today(self):
        now = datetime.now()
        return now    


    @cached_property
    def defaulter_number(self):
        result= Transaction.objects.filter(enlister=self.enlister).aggregate(total=Count('defaulters_name'))
        return result[ 'total']

    @cached_property
    def amount(self):
        result= Transaction.objects.filter(enlister=self.enlister).aggregate(total=Sum('default_amount'))
        return result[ 'total']    
#  ============================admin panel ======================================
    @cached_property
    def admin_defaulters(self):
        result=Transaction.objects.aggregate(total=Count('defaulters_name'))
        return result[ 'total']

    @cached_property
    def admin_amount(self):
        result=Transaction.objects.aggregate(total=Sum('default_amount'))
        return result[ 'total']    

    @cached_property
    def admin_users(self):
        result=User.objects.aggregate(total=Count('username'))
        return result[ 'total']    

    