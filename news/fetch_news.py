import requests
import feedparser
from dateutil import parser
from django.conf import settings
from .models import Post

def fetch_from_news_api():
    """Fetches news from NewsAPI and saves new articles to the database."""
    api_key = getattr(settings, 'NEWS_API_KEY', None)
    if not api_key or api_key == 'YOUR_API_KEY_HERE':
        print("NEWS_API_KEY not found or not configured in settings.py.")
        return 0

    url = f"https://newsapi.org/v2/top-headlines?country=ng&apiKey={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch from NewsAPI: {e}")
        return 0

    articles = response.json().get('articles', [])
    new_posts_count = 0
    
    for article in articles:
        # Avoid saving duplicates by checking the post_url
        if not Post.objects.filter(post_url=article['url']).exists():
            try:
                published_dt = parser.parse(article['publishedAt'])
                Post.objects.create(
                    title=article['title'],
                    short_description=article.get('description', ''),
                    content=article.get('content', article.get('description', '')),
                    image_url=article.get('urlToImage', ''),
                    post_url=article['url'],
                    published_at=published_dt,
                    category='News'
                )
                new_posts_count += 1
            except Exception as e:
                print(f"Error saving article '{article.get('title')}': {e}")
    
    return new_posts_count

def fetch_from_rss(feed_url='https://punchng.com/feed/'):
    """Fetches news from an RSS feed and saves new articles."""
    feed = feedparser.parse(feed_url)
    new_posts_count = 0
    for entry in feed.entries:
        if not Post.objects.filter(post_url=entry.link).exists():
            try:
                published_dt = parser.parse(entry.published)
                Post.objects.create(
                    title=entry.title,
                    short_description=entry.get('summary', ''),
                    content=entry.get('content', [{}])[0].get('value', entry.get('summary', '')),
                    post_url=entry.link,
                    published_at=published_dt,
                    category='News'
                )
                new_posts_count += 1
            except Exception as e:
                print(f"Error saving RSS entry '{entry.get('title')}': {e}")
    return new_posts_count