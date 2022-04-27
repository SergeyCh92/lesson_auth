from random import choices
from django_filters import rest_framework as filters
from django_filters.rest_framework import DateFromToRangeFilter, ChoiceFilter, NumberFilter
from advertisements.models import Advertisement, AdvertisementStatusChoices


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    created_at = DateFromToRangeFilter()
    status = ChoiceFilter(choices=AdvertisementStatusChoices.choices)
    creator = NumberFilter()

    class Meta:
        model = Advertisement
        fields = ['created_at', 'status', 'creator']
