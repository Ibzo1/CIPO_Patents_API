import django_filters

class OmitFilter(django_filters.CharFilter):
    """
    Filters to exclude a comma-separated list of values.
    Example: ?field_to_omit=value1,value2,value3
    """
    def filter(self, qs, value):
        if value:
            values = [v.strip() for v in value.split(',')]
            lookup = f'{self.field_name}__in'
            return qs.exclude(**{lookup: values})
        return qs

class ListFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    """
    Filters for a comma-separated list of values.
    Example: ?field__in=value1,value2,value3
    """
    pass
