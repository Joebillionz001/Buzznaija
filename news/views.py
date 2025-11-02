from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, NewsletterSubscriber
from django.db.models import Q, Count, F
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib import messages

def homepage(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    
    posts_list = Post.objects.all()

    # Search functionality
    if query:
        posts_list = posts_list.filter(
            Q(title__icontains=query) | Q(short_description__icontains=query)
        ).distinct()

    # Category filtering
    if category and category != 'All':
        posts_list = posts_list.filter(category__iexact=category)

    # Pagination
    paginator = Paginator(posts_list, 10) # Show 10 posts per page.
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    # For the sidebar and navbar
    one_week_ago = timezone.now() - timezone.timedelta(days=7)
    trending_posts = Post.objects.filter(published_at__gte=one_week_ago).order_by('-view_count', '-published_at')[:5]

    context = {
        'posts': posts,
        'trending_posts': trending_posts,
        'current_category': category,
    }
    return render(request, 'news/homepage.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Increment view count safely using an F() expression
    post.view_count = F('view_count') + 1
    post.save(update_fields=['view_count'])
    post.refresh_from_db() # Load the updated value from the database

    comments = post.comments.all().order_by('-created_at')
    related_posts = Post.objects.filter(category=post.category).exclude(pk=pk)[:4]

    # Handle comment submission
    if request.method == 'POST':
        author = request.POST.get('author')
        body = request.POST.get('body')
        if author and body:
            Comment.objects.create(post=post, author=author, body=body)
            # Re-fetch comments to show the new one immediately
            comments = post.comments.all().order_by('-created_at')
    
    context = {
        'post': post,
        'comments': comments,
        'related_posts': related_posts,
        'current_category': post.category,
        'meta_title': f"{post.title} - BuzzNaija",
        'meta_description': post.short_description or ' '.join(post.content.split()[:25]),
    }
    return render(request, 'news/post_detail.html', context)

def subscribe_newsletter(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()

        if not name or not email:
            messages.error(request, 'Name and email are required.')
            return redirect(request.META.get('HTTP_REFERER', 'homepage'))

        if NewsletterSubscriber.objects.filter(email=email).exists():
            messages.warning(request, f'The email {email} is already subscribed.')
        else:
            NewsletterSubscriber.objects.create(name=name, email=email)
            messages.success(request, 'Thank you for subscribing to our newsletter!')
    
    return redirect(request.META.get('HTTP_REFERER', 'homepage'))
