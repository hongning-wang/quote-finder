import requests
from django.core.management.base import BaseCommand
from api.serializers import QuoteSerializer

BASE_URL = 'https://api.quotable.kurokeita.dev/api/quotes'
LAST_PAGE = 210

class Command(BaseCommand):
    def handle(self, *args, **options):
        for page in range(0, LAST_PAGE+1):
            resp = requests.get(BASE_URL, params={"page":page}, timeout = 10)
            resp.raise_for_status()
            data = resp.json()['data']
            for q in data:
                serializer = QuoteSerializer(data = {
                    'id': q['id'],
                    'author': q['author']['name'],
                    'content': q['content'],
                    'tags': q['tags']
                })
                if serializer.is_valid():
                    serializer.save()
                else:
                    self.stderr.write(str(serializer.errors))
            self.stdout.write(f"Fetched page {page}/{LAST_PAGE}")

