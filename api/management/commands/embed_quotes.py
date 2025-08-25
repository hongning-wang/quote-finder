from django.core.management.base import BaseCommand
from api.models import Quote
from api.retrieval import embed_text


class Command(BaseCommand):
    def handle(self, *args, **options):
        quotes = Quote.objects.filter(embedding=[])
        for q in quotes:
            resp = embed_text(q.content)
            q.embedding = resp.embeddings[0].values
            q.save()
            self.stdout.write(f"Embedded quote {q.id} - {q.author}")