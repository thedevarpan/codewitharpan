from django.urls import path
from.import views

urlpatterns = [
    path("", views.BlogPost, name = "BlogPost"),
    path("blog-details/<slug:slug>", views.BlogDetails, name = "BlogDetails"),
    path("add-comment/", views.AddComment, name="AddComment"),
    path("add-subcomment/", views.AddSubComment, name="AddSubComment"),
    path("like-blog/<slug:slug>/", views.like_blog, name="like_blog"),
    path("dislike-blog/<slug:slug>/", views.dislike_blog, name="dislike_blog"),
] 
