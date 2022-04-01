from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import ToDo, User,InProgress,Done
# Create your views here.

def index(request):
    to_do_activities =  ToDo.objects.all()
    to_do_list = {}
    for to_do in to_do_activities:
        user = User.objects.get(id = to_do.user_id_id)
        to_do_list[to_do] = user
    in_progress = InProgress.objects.all()
    in_progress_list = {}
    for in_progress in in_progress:
        user = User.objects.get(id = in_progress.user_id_id)
        in_progress_list[in_progress] = user
    done_tasks = Done.objects.all()
    done_task_list = {}
    for done_task in done_tasks:
        user = User.objects.get(id = done_task.user_id_id)
        done_task_list[done_task] = user
    return render(request,"ticket/ticket.html",{'context':to_do_list,'context_inprogress':in_progress_list,"done_task_list":done_task_list })

def move_to_inprogress(request):
    if request.method =="POST":

        
        user_id = request.POST['user_id']
        user_object  = User.objects.get(id=user_id)
        if request.POST.get('submit') == "Move to Inprogess":
            done_id =  request.POST['id']
            done_data  = Done.objects.get(id = done_id)
            InProgress_task = InProgress.objects.create(user_id=user_object,assignee_name=done_data.assignee_name,\
                task_name=done_data.task_name, description = done_data.description,total_work_log = done_data.total_work_log,\
                    updated_worklog = done_data.updated_worklog,created_task_time = done_data.created_task_time,
                    update_task_time = done_data.update_task_time,Priority = done_data.Priority )
            done_data.delete()
        else:
            to_do_id =  request.POST['id']
            task_data  = ToDo.objects.get(id = to_do_id)
            InProgress_task = InProgress.objects.create(user_id=user_object,assignee_name=task_data.assignee_name,\
                task_name=task_data.task_name, description = task_data.description,total_work_log = task_data.total_work_log,\
                    updated_worklog = task_data.updated_worklog,created_task_time = task_data.created_task_time,
                    update_task_time = task_data.update_task_time,Priority = task_data.Priority )
            task_data.delete()
            InProgress_task.save()
        
        return redirect('index')
        

def move_to_done(request):
    if request.method =="POST":
        to_do_id =  request.POST['id']
        task_data  = InProgress.objects.get(id = to_do_id)
        user_id = request.POST['user_id']
        user_object  = User.objects.get(id=user_id)
        if request.POST.get('submit') == "Move to TO-DO":
            to_do_task = ToDo.objects.create(user_id=user_object,assignee_name=task_data.assignee_name,\
            task_name=task_data.task_name, description = task_data.description,total_work_log = task_data.total_work_log,\
                 updated_worklog = task_data.updated_worklog,created_task_time = task_data.created_task_time,
                 update_task_time = task_data.update_task_time,Priority = task_data.Priority )
            to_do_task.save()
        else:
            done_task = Done.objects.create(user_id=user_object,assignee_name=task_data.assignee_name,\
                task_name=task_data.task_name, description = task_data.description,total_work_log = task_data.total_work_log,\
                    updated_worklog = task_data.updated_worklog,created_task_time = task_data.created_task_time,
                    update_task_time = task_data.update_task_time,Priority = task_data.Priority )
            done_task.save()
        task_data.delete()
        return redirect('index')



    