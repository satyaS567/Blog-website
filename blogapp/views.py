from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    blogs = Blog.objects.filter(hidden=False)
    categories = Category.objects.all()
    authors = Author.objects.all()

    latest_blog = Blog.objects.all().order_by('-id')[:6]
    popular_post= Blog.objects.all().order_by('-id')[5:10]

    context = {
        'blogs': blogs, 
        'categories':categories,
        'authors':authors,
        'latest_blog':latest_blog,
        'popular_post':popular_post,
    }
    return render(request,'index.html',context)


@login_required(login_url='/signin')
def base(request):
    return render(request,'base.html')


@login_required(login_url='/signin')
def contact(request):
    return render(request,'contact.html')


@login_required(login_url='/signin')
def blog(request,id):
    blog = Blog.objects.get(id=id)
    categories = Category.objects.all()
    authors = Author.objects.all()
    popular_post= Blog.objects.all().order_by('-id')[5:10]

    context = {
        'blog': blog, 
        'authors':authors,
        'categories':categories,
        'popular_post':popular_post,
    }

    return render(request, 'blog.html', context)

@login_required(login_url='/signin')
def blogs(request):
    blogs = Blog.objects.filter(hidden=False)
    categories = Category.objects.all()
    authors = Author.objects.all()

    latest_blog = Blog.objects.all().order_by('-id')[:6]
    popular_post= Blog.objects.all().order_by('-id')[:3]

    context = {
        'blogs': blogs, 
        'categories':categories,
        'authors':authors,
        'latest_blog':latest_blog,
        'popular_post':popular_post,
    }
    return render(request,'blogs.html',context)

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confrimpassword =request.POST['confrimpassword']
        if password == confrimpassword:
            if User.objects.filter(email=email).exists():
                messages.error(request,'Email already in use')
                return redirect('/register')
            if User.objects.filter(username=username).exists():
                messages.error(request,'Username already used')
                return redirect('/register')
            else:
                User.objects.create_user(username=username,email=email,password=password)
                messages.success(request,'Account created successfully.Goto login page')
                return redirect('/signin')
        else:
            messages.error(request,'password do not match pls check password')
            return redirect('/register')

    return render(request,'register.html')
   

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'login successfully')
            return redirect('/')
        else:
            messages.error(request,'Invalid details')
            return redirect('/signin')

    return render(request,'signin.html')

def logout(request):
    if request.method =='POST':
        logout(request)
        messages.success(request,'logout successfully')
        return redirect('/')
    return render(request,'logout.html')

def register_author(request):
    user = request.user
    if request.method == "POST":
        # fetch form data
        age = request.POST['age']
        phone = request.POST['phone']
        image = request.FILES['image']

        # fetch name, email from database
        name = user.username
        email = request.user.email

        # create author object
        # save the object

        Author.objects.create(name=name, age=age, phone=phone, email=email, image=image, user=user)

        return redirect("/")
    return render(request, 'register_author.html')

def user_dashboard(request):
    # Fetch the author
    author = request.user.author

    # Filter the blogs by authors
    blogs = Blog.objects.filter(author=author)

    context = {
        'blogs':blogs,
    }

    return render(request, 'user_dashboard.html', context)

def add_blog(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        category = request.POST['category']
        image = request.FILES['image']
        author = request.user.author
        category_obj = Category.objects.get(name=category)

        Blog.objects.create(title=title, description=description, category=category_obj, author=author, image=image)

        return redirect("/user_dashboard")
    context = {
        'categories':categories,
    }

    return render(request, 'add_blog.html', context)

def blog_category(request,name):
    categories = Category.objects.all()
    category = Category.objects.get(name=name)
    blogs = Blog.objects.filter(category=category)
    latest_blog = Blog.objects.all().order_by('-id')[:3]
    authors = Author.objects.all()
    context = {
        'category': name, 
        'blogs': blogs,
        'latest_blog':latest_blog,
        'authors':authors,
        'categories':categories,

    }
    return render(request, 'blog_category.html', context)

def update_blog(request, id):
    blog = Blog.objects.get(id=id)
    categories = Category.objects.all()
    category_obj = None

    if request.method == 'POST':
        newtitle = request.POST['title']
        newdescription = request.POST['description']
        newcategory_name = request.POST['category']
        newimage = request.FILES['image']

        category_obj = Category.objects.get(name=newcategory_name)

        blog.title = newtitle
        blog.description = newdescription
        blog.category = category_obj
        blog.image = newimage
        blog.save()

        context = {
            'blog': blog,
            'categories': categories,
            'category': category_obj,
        }

        return redirect("/user_dashboard")

    # Define context in the 'GET' request branch as well
    context = {
        'blog': blog,
        'categories': categories,
        'category': category_obj,
    }

    return render(request, 'update_blog.html', context)

def delete_blog(request,id):
    blog = Blog.objects.get(id=id)
    blog.delete()
    return redirect('/user_dashboard')