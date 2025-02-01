# messaging_app/chats/filters.py
import django_filters
from .models import Message
from django_filters import DateFilter

class MessageFilter(django_filters.FilterSet):
    sender_email = django_filters.CharFilter(field_name='sender__email', lookup_expr='icontains', label='Sender Email')
    date_range = DateFilter(field_name='created_at', lookup_expr='gte', label='Start Date')  # For filtering messages after a certain date
    end_date = DateFilter(field_name='created_at', lookup_expr='lte', label='End Date')  # For filtering messages before a certain date

    class Meta:
        model = Message
        fields = ['sender_email', 'date_range', 'end_date']
