from rest_framework import serializers
from .models import Quote

class QuoteSerializer(serializers.ModelSerializer):
    """
    A serializer for the Quote model.
    """
    class Meta:
        model = Quote
        fields = '__all__'