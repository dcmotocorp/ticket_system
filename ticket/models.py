
from secrets import choice
from django.db import models
from urllib3 import Retry
# Create your models here.

class Admin(models.Model):
    pass

class User(models.Model):
    name = models.TextField(max_length=20)
    password = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class ToDo(models.Model):
    user_id = models.ForeignKey('User',on_delete=models.CASCADE)
    assignee_name = models.TextField()
    task_name = models.TextField(null=False)
    description = models.TextField()
    total_work_log = models.IntegerField()
    updated_worklog =models.IntegerField()
    created_task_time = models.DateTimeField(auto_now_add=True)
    update_task_time = models.DateTimeField(auto_created=True)
    Priority = models.TextField(choices= [('HIGH', 'HIGH'),('LOW','LOW'),('MEDIUM','MEDIUM')])

    def __str__(self):
        return self.task_name

class InProgress(models.Model):
    user_id = models.ForeignKey('User',on_delete=models.CASCADE)
    assignee_name = models.TextField()
    task_name = models.TextField(null=False)
    description = models.TextField()
    total_work_log = models.IntegerField()
    updated_worklog =models.IntegerField()
    created_task_time = models.DateTimeField(auto_now_add=True)
    update_task_time = models.DateTimeField(auto_created=True)
    Priority = models.TextField(choices= [('HIGH', 'HIGH'),('LOW','LOW'),('MEDIUM','MEDIUM')])


class Done(models.Model):
    user_id = models.ForeignKey('User',on_delete=models.CASCADE)
    assignee_name = models.TextField()
    task_name = models.TextField(null=False)
    description = models.TextField()
    total_work_log = models.IntegerField()
    updated_worklog =models.IntegerField()
    created_task_time = models.DateTimeField(auto_now_add=True)
    update_task_time = models.DateTimeField(auto_created=True)
    Priority = models.TextField(choices = [('HIGH', 'HIGH'),('LOW','LOW'),('MEDIUM','MEDIUM')])


class Sprint(models.Model):
    pass 
