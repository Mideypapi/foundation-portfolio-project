from django.urls import path

from . import views

urlpatterns = [

    # auth
    path('registration/signup', views.signup, name="signup"),
    path('registration/login', views.login, name="login"),
    path('logout', views.logout, name="logout"),


    path('', views.home, name="home"),
    path('new/', views.new, name="new"),
    path('profile/', views.mypage, name="profile"),
    path('detail/<slug:slug>', views.detail, name="detail"),
    path('edit/<slug:slug>', views.edit, name="edit"),
    path('delete/<slug:slug>', views.delete, name="delete"),
    path('delete_comment/<int:post_pk>/<int:comment_pk>',
         views.delete_comment, name="delete_comment"),
    path('like', views.like, name="like"),
    path('liked_post', views.liked_posts, name="liked_post"),
    path('scrap', views.scrap, name="scrap"),
    path('scraps', views.saved_posts, name="scraps"),
    path('myposts', views.myposts, name="mypost"),
]
