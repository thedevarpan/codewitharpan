from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from.models import *
from django.http import JsonResponse
from account.models import CustomUser
from django.contrib.auth.decorators import login_required


User = CustomUser
# Create your views here.

def BlogPost(request):
    all_blogs = Blog.objects.all().order_by('-id')
    params = {'all_blogs':all_blogs}
    return render(request, 'myblog/blog-classic.html', params)



def BlogDetails(request, slug):
    blog = Blog.objects.get(slug=slug)
    number_of_comments = blog.comments.count()
    recent_posts = Blog.objects.all().order_by('-id')[:2]
    # Get all blogs ordered by their creation date
    all_blogs = Blog.objects.order_by('created_at')
    blog_index = list(all_blogs).index(blog)
    # Determine previous and next blogs
    prev_blog = all_blogs[blog_index - 1] if blog_index > 0 else None
    next_blog = all_blogs[blog_index + 1] if blog_index < len(all_blogs) - 1 else None

    #add blog comments

    params = {'blog': blog, 'prev_blog': prev_blog, 'next_blog': next_blog, 'recent_posts': recent_posts, 'number_of_comments': number_of_comments}
    return render(request, 'myblog/blog-details.html', params)



def like_blog(request, slug):
    if request.method == 'POST':
        blog = get_object_or_404(Blog, slug=slug)
        user = request.user

        # Get or create the interaction object
        interaction, created = BlogInteraction.objects.get_or_create(user=user, blog=blog)

        # Check if user has already interacted
        if interaction.like:
            return JsonResponse({'error': 'You have already liked this post.'}, status=400)

        if interaction.dislike:
            # Remove dislike if exists
            interaction.dislike = False
            blog.dislikes -= 1

        interaction.like = True
        blog.likes += 1
        interaction.save()
        blog.save()
        
        return JsonResponse({'likes': blog.likes, 'dislikes': blog.dislikes})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def dislike_blog(request, slug):
    if request.method == 'POST':
        blog = get_object_or_404(Blog, slug=slug)
        user = request.user

        # Get or create the interaction object
        interaction, created = BlogInteraction.objects.get_or_create(user=user, blog=blog)

        # Check if user has already interacted
        if interaction.dislike:
            return JsonResponse({'error': 'You have already disliked this post.'}, status=400)

        if interaction.like:
            # Remove like if exists
            interaction.like = False
            blog.likes -= 1

        interaction.dislike = True
        blog.dislikes += 1
        interaction.save()
        blog.save()

        return JsonResponse({'likes': blog.likes, 'dislikes': blog.dislikes})
    return JsonResponse({'error': 'Invalid request'}, status=400)



@login_required
def AddComment(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')
            post_slug = request.POST.get('post_slug')
            blog_post = get_object_or_404(Blog, slug=post_slug)

            # Create a new comment
            Comment.objects.create(
                post=blog_post,
                user=request.user,  # Use the logged-in user
                user_name=name,
                email=email,
                message=message
            )
            return redirect('BlogDetails', slug=post_slug)

    except Exception as e:
        print(e)
    return HttpResponse("This is home page")


@login_required
def AddSubComment(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')
            post_slug = request.POST.get('post_slug')
            parent_id = request.POST.get('parent_id')

            # Get the blog post and parent comment
            blog_post = get_object_or_404(Blog, slug=post_slug)
            parent_comment = get_object_or_404(Comment, id=parent_id)

            # Create a subcomment
            SubComment.objects.create(
                post=blog_post,
                comment=parent_comment,
                user=request.user,  # Use the logged-in user
                user_name=name,
                email=email,
                message=message
            )
            return redirect('BlogDetails', slug=post_slug)

    except Exception as e:
        print(e)
    return HttpResponse("This is home page")