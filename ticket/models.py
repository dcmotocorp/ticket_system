from django.db import models

# Create your models here.

class Admin(models.Model):
    name = models.TextField(max_length=20)
    password = models.CharField(max_length=20)
    role = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class User(models.Model):
    name = models.TextField(max_length=20)
    password = models.CharField(max_length=20)
    role = models.CharField(max_length=20,default='user')
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

class Comment(models.Model):
    comment = models.TextField()
    task_id_done = models.ManyToManyField('Done')
    task_id_inprogress = models.ManyToManyField('InProgress')
    task_id_to_do = models.ManyToManyField('ToDo')

class Sprint(models.Model):
    pass 
