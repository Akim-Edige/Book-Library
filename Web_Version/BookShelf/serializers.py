from rest_framework import serializers
from .models import Book
import django_filters
from django.db import models

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'year', 'status', 'description', 'cover_image']



class BookFilter(django_filters.FilterSet):

    # Filtering by author and title
    author = django_filters.CharFilter(field_name='author', lookup_expr='icontains', required=False)
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', required=False)

    # Quantity range filtering (greater than or equal to)
    year_min = django_filters.NumberFilter(field_name='year', lookup_expr='gte', required=False)
    year_max = django_filters.NumberFilter(field_name='year', lookup_expr='lte', required=False)


    # # Filtering by availability (True or False)
    status = django_filters.CharFilter(field_name='status', required=False)

    # Name search (case-insensitive match)
    search = django_filters.CharFilter(method='filter_search', required=False)

    class Meta:
        model = Book
        fields = ['author', 'title', 'id', 'year_min', 'year_max', 'status']


    def filter_search(self, queryset, name, value):
        if value:
            return queryset.filter(
                models.Q(id__icontains=value) |
                models.Q(title__icontains=value) |
                models.Q(author__icontains=value)
            )
        return queryset
