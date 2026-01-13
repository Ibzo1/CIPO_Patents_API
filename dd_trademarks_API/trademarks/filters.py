import django_filters
from .models import TmMain

class TmMainFilter(django_filters.FilterSet):
    # For text fields, 'icontains' allows for a case-insensitive "contains" search.
    mark_verbal_element_text = django_filters.CharFilter(lookup_expr='icontains')

    # For date fields, we can create filters for ranges.
    # 'gte' means "greater than or equal to" (e.g., a start date).
    filing_date_after = django_filters.DateFilter(field_name='filing_date', lookup_expr='gte')
    # 'lte' means "less than or equal to" (e.g., an end date).
    filing_date_before = django_filters.DateFilter(field_name='filing_date', lookup_expr='lte')

    # For number fields, we can check for greater or less than.
    # 'gt' means "greater than".
    total_nice_classifications_gt = django_filters.NumberFilter(field_name='total_nice_classifications_number', lookup_expr='gt')

    class Meta:
        model = TmMain
        # Include fields that should still use the default exact-match filtering.
        fields = ['application_number', 'registration_number']