from django.core.management.base import BaseCommand
from api.models import Quote
from google import genai
from google.genai import types
import os
import numpy as np
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

class Command(BaseCommand):
    def handle(self, *args, **options):
        quotes = Quote.objects.filter(embedding=[])
        for q in quotes:
            resp = client.models.embed_content(
                model = "gemini-embedding-001",
                contents=q.content,
                config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
            )
            q.embedding = resp.embeddings[0].values
            q.save()
            self.stdout.write(f"Embedded quote {q.id} - {q.author}")