from django.shortcuts import render
from rest_framework import generics, status
from api.retrieval import build_index, add_quote, embed_text, search_quotes
from api.models import Quote
from api.serializers import QuoteSerializer
from rest_framework.response import Response

index = build_index()
class QuoteListCreateView(generics.ListCreateAPIView):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer

    def perform_create(self, serializer):
        """
        Add a quote to the database via an api call.
        """
        content = serializer.validated_data.get('content')
        if not content:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        embedding_vector = embed_text(content, type="RETRIEVAL_DOCUMENT")

        if embedding_vector is not None:
            serializer.validated_data['embedding'] = embedding_vector.embeddings[0].values
        
        quote = serializer.save()
        add_quote(quote)

    def list(self, request, *args, **kwargs):
        """Query for quotes in the database with a similar idea"""
        query = request.query_params.get('content', None)
        if not query:
            return super().list(request, *args, **kwargs)

        quotes = search_quotes(query)
        
        pk_order = [q.pkid for q in quotes]
        queryset_ordered = sorted(quotes, key=lambda x: pk_order.index(x.pkid))

        serializer = self.get_serializer(queryset_ordered, many=True)
        return Response(serializer.data)

        