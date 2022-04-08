from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import ToDo, User,InProgress,Done, Comment
# Create your views here.

def index(request):
    to_do_activities =  ToDo.objects.all()
    to_do_list = []
    for to_do in to_do_activities:
        user = User.objects.get(id = to_do.user_id_id)
        comment = Comment.objects.filter(task_id_to_do=to_do.id)
        # to_do_list[to_do] = user
        to_do_dict = {'to_do_object':to_do,'user':user,'comment':comment}
        to_do_list.append(to_do_dict)
    
    in_progress = InProgress.objects.all()
    in_progress_list = []
    for in_progress in in_progress:
        user = User.objects.get(id = in_progress.user_id_id)
        comment = Comment.objects.filter(task_id_inprogress=in_progress.id)
        in_progress_dict = {'in_progress_object':in_progress,'user':user,'comment':comment}
        in_progress_list.append(in_progress_dict)
    
    done_tasks = Done.objects.all()
    done_task_list = []
    for done_task in done_tasks:
        user = User.objects.get(id = done_task.user_id_id)
        comment = Comment.objects.filter(task_id_done=done_task.id)
        done_task_dict = {'done_task_list':done_task,'user':user,'comment':comment}
        done_task_list.append(done_task_dict)
    return render(request,"ticket/ticket.html",{'to_do_list':to_do_list,'in_progress_list':in_progress_list,"done_task_list":done_task_list })

def move_to_inprogress(request):
    if request.method =="POST":
        user_id = request.POST['user_id']
        user_object  = User.objects.get(id=user_id)
        if request.POST.get('submit') == "Move to Inprogess":
            done_id =  request.POST['done_id']
            done_data  = Done.objects.get(id = done_id)
            InProgress_task = InProgress.objects.create(user_id=user_object,assignee_name=done_data.assignee_name,\
                task_name=done_data.task_name, description = done_data.description,total_work_log = done_data.total_work_log,\
                    updated_worklog = done_data.updated_worklog,created_task_time = done_data.created_task_time,
                    update_task_time = done_data.update_task_time,Priority = done_data.Priority )
            
            comments_objects =  Comment.objects.filter(task_id_done=done_id)
            for comment in comments_objects:
                comment.task_id_inprogress.add(InProgress_task)
                comment.task_id_done.remove(done_id)
                comment.save()
            done_data.delete()
            return redirect('index')
        else:
            to_do_id =  request.POST['to_do_id']
            task_data  = ToDo.objects.get(id = to_do_id)
            InProgress_task = InProgress.objects.create(user_id=user_object,assignee_name=task_data.assignee_name,\
                task_name=task_data.task_name, description = task_data.description,total_work_log = task_data.total_work_log,\
                    updated_worklog = task_data.updated_worklog,created_task_time = task_data.created_task_time,
                    update_task_time = task_data.update_task_time,Priority = task_data.Priority )
            InProgress_task.save()
            comments_objects =  Comment.objects.filter(task_id_to_do=task_data.id)
            for comment in comments_objects:
                comment.task_id_inprogress.add(InProgress_task)
                comment.task_id_to_do.remove(to_do_id)
                comment.save()
            task_data.delete()
            return redirect('index')
        return redirect('index')
        

def move_to_done(request):
    if request.method =="POST":
        inprogress_id =  request.POST['inprogress_id']
        task_data  = InProgress.objects.get(id = inprogress_id)
        user_id = request.POST['user_id']
        user_object  = User.objects.get(id=user_id)
        if request.POST.get('submit') == "Move to TO-DO":
            to_do_task = ToDo.objects.create(user_id=user_object,assignee_name=task_data.assignee_name,\
            task_name=task_data.task_name, description = task_data.description,total_work_log = task_data.total_work_log,\
                 updated_worklog = task_data.updated_worklog,created_task_time = task_data.created_task_time,
                 update_task_time = task_data.update_task_time,Priority = task_data.Priority )
            to_do_task.save()
            comments_objects =  Comment.objects.filter(task_id_inprogress=inprogress_id)
            for comment in comments_objects:
                comment.task_id_to_do.add(to_do_task.id)
                comment.task_id_inprogress.remove(inprogress_id)
                comment.save()
            task_data.delete()
            return redirect('index')
        else:
            done_task = Done.objects.create(user_id=user_object,assignee_name=task_data.assignee_name,\
                task_name=task_data.task_name, description = task_data.description,total_work_log = task_data.total_work_log,\
                    updated_worklog = task_data.updated_worklog,created_task_time = task_data.created_task_time,
                    update_task_time = task_data.update_task_time,Priority = task_data.Priority )
            done_task.save()
            comments_objects =  Comment.objects.filter(task_id_inprogress=inprogress_id)
            for comment in comments_objects:
                comment.task_id_done.add(done_task.id)
                comment.task_id_inprogress.remove(inprogress_id)
                comment.save()
            task_data.delete()
            return redirect('index')

def create_comment(request):
    if request.method == "POST":
        _comment = request.POST.get('comment')
        user_id = request.POST.get('user_id')
        if request.POST.get('to_id'):    
            id  = request.POST.get('to_id')
            comment_object = Comment.objects.create(comment=_comment)
            comment_object.task_id_to_do.add(id)
            comment_object.save()
            return redirect('index')
        if request.POST.get('inprogress_id'):
            id  = request.POST.get('inprogress_id')
            comment_object = Comment.objects.create(comment=_comment)
            comment_object.task_id_inprogress.add(id)
            comment_object.save()
            return redirect('index')
        if request.POST.get('done_id'):
            id  = request.POST.get('done_id')
            comment_object = Comment.objects.create(comment=_comment)
            comment_object.task_id_done.add(id)
            comment_object.save()
            return redirect('index')
        


 