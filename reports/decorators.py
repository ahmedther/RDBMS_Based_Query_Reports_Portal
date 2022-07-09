from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group

def unauthenticated_user(login_page):
    def wrapper_func(request, *args,**kwargs):
        if request.user.is_authenticated:
            return redirect('base')
        else :
            return login_page(request, *args, **kwargs)
    
    return wrapper_func


    

def allowed_users(allowed_roles):
    def decorator(view_func):
        def wrapper_func(request, *args,**kwargs):
            
            try : 
                groups = request.user.groups.get(name=allowed_roles)
            
            except Group.DoesNotExist:
                return render(request,'reports/base.html', { 'error':'You Are Not Authorized To Access This Page. Please Contact Your Administrator.' ,'user_name':request.user.username})

            
            if groups:
                    return view_func(request, *args,**kwargs)
            
            

        return wrapper_func
    return decorator

# def user_specific_webpage(view_func):
#     def wrapper_func(request, *args,**kwargs):

#         groups = request.user.groups.all()
#         for group in groups:
#             print(group)
    
#     return wrapper_func