from django.core.management.base import BaseCommand
from news.fetch_news import fetch_from_news_api, fetch_from_rss

class Command(BaseCommand):
    help = 'Fetches and saves the latest news articles from configured sources.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting news import process...'))

        # Fetch from RSS (e.g., PunchNG)
        self.stdout.write('Fetching from RSS feed...')
        rss_count = fetch_from_rss()
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {rss_count} new posts from RSS.'))

        # Fetch from NewsAPI
        self.stdout.write('Fetching from NewsAPI...')
        api_count = fetch_from_news_api()
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {api_count} new posts from NewsAPI.'))

        self.stdout.write(self.style.SUCCESS('News import process finished.'))