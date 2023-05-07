from django.http import HttpResponse
from .forms import SignupForm,LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Books,LibraryUsers
from .tokens import *
from django.utils.decorators import method_decorator
from .decorators import token_validator
from django.contrib.auth import logout
from django.urls import reverse

# Starting point/route/url of the app 
def home(request):
    return render(request, 'base.html')

#login view
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = LibraryUsers.objects.get(username=username,password=password)
            except LibraryUsers.DoesNotExist:
                return render(request, 'error.html',{'error_msg':'user not found try again with valid credentials'})
            return redirect(f'dashboard/{user.id}/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

#signup view
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_type = form.cleaned_data['user_type']
            try:
                existing_user = LibraryUsers.objects.get(username=username,user_type=user_type)
                return render(request, 'error.html',{'error_msg':'user already exists with this username try again'})
            except LibraryUsers.DoesNotExist:
                try:
                    created_user = LibraryUsers(username=username,password=password,user_type=user_type)
                    created_user.save()
                except Exception:
                    return render(request, 'signup_result.html',{'error':True})
                return render(request, 'signup_result.html',{'error':False})
        else:
            return render(request, 'signup_result.html',{'error':True})
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


#login success view/ landing page
def login_successfull_view(request,user_id):
    user  = LibraryUsers.objects.get(pk=int(user_id))
    token = create_jwt_token(user.id)
    is_member_user = True if user.user_type == 'Member' else False
    response = render(request, 'dashboard.html', {'is_member':is_member_user,'user':user})
    response.set_cookie('jwt_token', token)
    return response
    # return render(request, 'dashboard.html', {'is_member':is_member_user,'user':user})

@token_validator
def all_books_available_view(request,user_id):
    user = LibraryUsers.objects.get(pk=int(user_id))
    books = Books.objects.filter(book_status='AVAILABLE')
    return render(request,'all_books.html',{'query_results':books,'user':user})

@token_validator
def buy_book(request,user_id,book_id):
    user = LibraryUsers.objects.get(pk=int(user_id))
    book = Books.objects.get(pk=int(book_id))
    book.book_status='BORROWED'
    book.user = user
    book.save()
    return render(request,'buy_book_success.html',{'user_id':user.id})

@token_validator
def my_books(request,user_id):
    books = Books.objects.filter(user=user_id)
    return render(request,'my_books_list.html',{'user_id':user_id,'query_results':books})

@token_validator
def return_my_books(request,user_id,book_id):
    book = Books.objects.get(pk=int(book_id))
    book.user=None
    book.book_status = 'AVAILABLE'
    book.save()
    return render(request,'return_book_success.html',{'user_id':user_id})


@token_validator
def library_manage_books(request,user_id):
    search_param = request.GET.get('book_name',None)
    if search_param:
        books = Books.objects.filter(book_title__contains=search_param)
    else:
        books = Books.objects.all()
    return render(request,'manage_books_library.html',{'query_results':books,'user_id':user_id})

@token_validator
def library_update_book_status(request,book_id,user_id):
    book = Books.objects.get(pk=int(book_id))
    users = LibraryUsers.objects.all()
    is_available = True if book.book_status=='AVAILABLE' else False
    if not is_available:
        default_assigned_user = book.user.id
    else:
        default_assigned_user = None
    return render(request,'update_book_status.html',{'is_book_available':is_available,
    'query_results':users,'default_user':default_assigned_user,'book_id':book.id,'user_id':user_id})

@token_validator
def library_book_status_update_confirm(request,book_id,user_id):
    if request.method == "POST":
        book = Books.objects.get(pk=int(book_id))
        if request.POST['status'] == 'AVAILABLE':
            book.user = None
        else:
            book.user = LibraryUsers.objects.get(pk=int(request.POST['users']))
        book.book_status = request.POST['status']
        book.save()
        return render(request,'update_book_success.html',{'user_id':user_id})

@token_validator
def add_new_book(request,user_id):
    return render(request,'add_new_book.html',{'user_id':user_id})

@token_validator
def add_new_book_success(request,user_id):
    if request.method == "POST":
        new_book_title = request.POST['new_book_title']
        if not new_book_title:
            return  render(request,'dashboard_return_after_error.html',{'user_id':user_id})
        new_book = Books(book_title=new_book_title,book_status='AVAILABLE')
        new_book.save()
        return render(request,'new_book_add_success.html',{'user_id':user_id})

@token_validator
def delete_book(request,book_id,user_id):
    book = Books.objects.get(pk=book_id)
    book.delete()
    return render(request,'delete_book_success.html',{'user_id':user_id})

@token_validator
def library_manage_users(request,user_id):
    search_param = request.GET.get('username',None)
    if search_param:
        users = LibraryUsers.objects.filter(username__contains=search_param)
    else:
        users = LibraryUsers.objects.all()
    return render(request,'manage_users_library.html',{'query_results':users,'user_id':user_id})

@token_validator
def library_update_user_password(request,user_id,main_user_id):
    return render(request,'update_user_password.html',{'user_id':user_id,'main_user_id':main_user_id})

@token_validator
def library_update_user_password_success(request,user_id,main_user_id):
    if request.method == "POST":
        new_password = request.POST['new_password']
        if not new_password:
            return  render(request,'dashboard_return_after_error.html',{'user_id':main_user_id})
        user = LibraryUsers.objects.get(pk=user_id)
        user.password = new_password
        user.save()
    return render(request,'update_user_password_success.html',{'user_id':user_id,'main_user_id':main_user_id})

@token_validator
def delete_user(request,user_id,main_user_id):
    books_by_user = Books.objects.filter(user=user_id)
    for obj in books_by_user:
        obj.user = None
        obj.book_status = 'AVAILABLE'
        obj.save()
    user = LibraryUsers.objects.get(pk=user_id)
    user.delete()
    return render(request,'delete_user_success.html',{'main_user_id':main_user_id})

@token_validator
def add_new_user(request,user_id):
    return render(request,'add_new_user.html',{'user_id':user_id})

@token_validator
def add_new_user_success(request,user_id):
    if request.method == "POST":
        username = request.POST['new_user_username']
        password = request.POST['new_user_password']
        user_type = request.POST['new_user_type']
        if not username or not password:
            return  render(request,'dashboard_return_after_error.html',{'user_id':user_id})
        new_user = LibraryUsers(username=username,password=password,user_type=user_type)
        new_user.save()
        return render(request,'new_user_add_success.html',{'user_id':user_id})


@token_validator
def logout(request):
    logout(request)
    response = render(request,'logout_success.html')
    response.delete_cookie('jwt_token')
    return response
