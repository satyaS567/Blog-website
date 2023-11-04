from django.urls import path
from .import views
urlpatterns = [
    path('',views.index),
    path('base',views.base),
    path('contact',views.contact),
    path('blog/<int:id>',views.blog),
    path('blogs',views.blogs),
    path('register',views.register),
    path('signin',views.signin),
    path('logout',views.logout),
    path('user_dashboard',views.user_dashboard),
    path('register_author',views.register_author),
    path('blog_category/<str:name>',views.blog_category),
    path('add_blog',views.add_blog),
    path('update_blog/<int:id>',views.update_blog),
    path('delete_blog/<int:id>',views.delete_blog),
]