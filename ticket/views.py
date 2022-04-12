from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Admin, ToDo, User,InProgress,Done, Comment
from functools import wraps
# Create your views here.

def registration(request):
    if request.method == "POST":
        if request.POST.get("role") == "admin":
            admin_object  = Admin.objects.create(name=request.POST.get("username"),password = request.POST.get("password"),role =request.POST.get("role") ) 
            admin_object.save()
            return render(request, "ticket/login_page.html")
        if request.POST.get("role") == "user":
            user_object  = User.objects.create(name=request.POST.get("username"),password = request.POST.get("password"),role =request.POST.get("role") ) 
            user_object.save()
            return render(request, "ticket/login_page.html")
    return render(request, "ticket/registration.html") 



def login_decorator(function=None):
    def decorator(view_func):
        @wraps(view_func)
        def f(request, *args, **kwargs):
            if  'username' in request.session and 'password' in request.session and 'role' in request.session:
                return view_func(request, *args, **kwargs)
            return redirect('login_page')
        return f
    if function is not None:
        return decorator(function)
    return decorator


def login_page(request):
    return render(request, "ticket/login_page.html")


def login_process(request):
    if request.method ==  "POST":
        if  'username' not in request.session and 'password' not in request.session:
            username = request.POST.get("username")
            password = request.POST.get("password")
            role = request.POST.get("role")
        else:
            username = request.session.get("username")
            password =  request.session.get("password")
            role    = request.session.get("role")

        if role == "admin":
            admin = Admin.objects.filter(name=username,password = password).first()  
            if admin : 
                request.session['username'] = username
                request.session['password'] = password
                request.session['role'] = admin.role
                return redirect('get_task')
                

        if role == "user":
            user =  User.objects.filter(name=username,password = password).first()
            if user:
                request.session['username'] = username
                request.session['password'] = password
                request.session['role'] = user.role
                return redirect('index')
        
        return redirect('login_page')
    else:
        #need to add login failed message
        return render(request, "ticket/login_page.html")

# -----------------End login -------------------#

def logout(request):
    del request.session['username'] 
    del request.session['password'] 
    return redirect('login_page')

@login_decorator
def index(request,user=None):
    print("-----------dipen")
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
            return redirect('index' )
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
        

def get_task(request):
    users = User.objects.all()
    to_do_task  = ToDo.objects.all()
    in_progress_task = InProgress.objects.all()
    done_task = Done.objects.all()
    return render(request,"ticket/admin.html",{'users':users,'to_do_task':to_do_task,'in_progress':in_progress_task,'done_task':done_task})

def create_to_do_task(request):
    user = User.objects.get(id = request.POST.get("assign"))
    to_do_task = ToDo.objects.create(user_id = user,assignee_name=user.name,\
            task_name=request.POST.get("task_name"), description = request.POST.get("desc"),total_work_log = request.POST.get("work_log"),\
                 updated_worklog = 0,created_task_time = request.POST.get("datetime"),
                 update_task_time =datetime.now(),Priority = request.POST.get("priority") )
    to_do_task.save()
    return redirect('get_task')

def delete_task(request):
    if request.POST.get("task_id"):
        task_id = request.POST.get("task_id")
        user = ToDo.objects.filter(id=task_id).first()
        if not user :
            user = InProgress.objects.filter(id=task_id).first()
        user = user
        if not user :
            user = Done.objects.filter(id=task_id).first()
        user.delete()   
    if request.POST.get("user_id"):
        user = User.objects.get(id=request.POST.get("user_id"))
        user.delete()
    return redirect('get_task') 

            

