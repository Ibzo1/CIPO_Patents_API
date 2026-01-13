from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

from .filters import OmitFilter
from .models import (
    PT_Main,
    PT_Priority_Claim,
    PT_Interested_Party,
    PT_Abstract,
    PT_Disclosure,
    PT_Claim,
    PT_IPC_Classification
)
from .serializers import (
    PTMainSerializer,
    PTPriorityClaimSerializer,
    PTInterestedPartySerializer,
    PTAbstractSerializer,
    PTDisclosureSerializer,
    PTClaimSerializer,
    PTIPCClassificationSerializer
)

#
# PT_Main
#
class PTMainFilter(django_filters.FilterSet):
    # Exact match: ?patent_number=2738890
    patent_number = django_filters.NumberFilter(field_name='patent_number', lookup_expr='exact')
    # Range queries: ?patent_number_after=X&patent_number_before=Y
    patent_number_after = django_filters.NumberFilter(field_name='patent_number', lookup_expr='gte')
    patent_number_before = django_filters.NumberFilter(field_name='patent_number', lookup_expr='lte')
    patent_number_omit = OmitFilter(field_name='patent_number')
    
    # Improved filing date filters that handle null values properly
    filing_date = django_filters.DateFromToRangeFilter(field_name='filing_date')
    filing_date_after = django_filters.DateFilter(field_name='filing_date', lookup_expr='gte')
    filing_date_before = django_filters.DateFilter(field_name='filing_date', lookup_expr='lte')
    filing_date_exact = django_filters.DateFilter(field_name='filing_date', lookup_expr='exact')
    # Filter to exclude null filing dates
    has_filing_date = django_filters.BooleanFilter(field_name='filing_date', lookup_expr='isnull', exclude=True)

    class Meta:
        model = PT_Main
        fields = [
            'patent_number',
            'patent_number_after',
            'patent_number_before',
            'patent_number_omit',
            'filing_date',
            'filing_date_after',
            'filing_date_before', 
            'filing_date_exact',
            'has_filing_date',
            'application_patent_title_english',
            'application_patent_title_french',
            'country_of_publication_code'
        ]

class PTMainViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PT_Main.objects.all()
    serializer_class = PTMainSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = [
        'patent_number',
        'application_patent_title_english',
        'application_patent_title_french',
        'country_of_publication_code'
    ]
    filterset_class = PTMainFilter


#
# PT_Priority_Claim
#
class PTPriorityClaimFilter(django_filters.FilterSet):
    patent_number = django_filters.NumberFilter(field_name='patent_number__patent_number', lookup_expr='exact')
    patent_number_after = django_filters.NumberFilter(field_name='patent_number__patent_number', lookup_expr='gte')
    patent_number_before = django_filters.NumberFilter(field_name='patent_number__patent_number', lookup_expr='lte')
    
    class Meta:
        model = PT_Priority_Claim
        fields = [
            'patent_number',
            'patent_number_after',
            'patent_number_before',
            'priority_claim_country_code'
        ]

class PTPriorityClaimViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PT_Priority_Claim.objects.all()
    serializer_class = PTPriorityClaimSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['patent_number__patent_number', 'priority_claim_country_code']
    filterset_class = PTPriorityClaimFilter


#
# PT_Interested_Party
#
class PTInterestedPartyFilter(django_filters.FilterSet):
    patent_number = django_filters.NumberFilter(field_name='patent_number__patent_number', lookup_expr='exact')
    patent_number_after = django_filters.NumberFilter(field_name='patent_number__patent_number', lookup_expr='gte')
    patent_number_before = django_filters.NumberFilter(field_name='patent_number__patent_number', lookup_expr='lte')
    
    class Meta:
        model = PT_Interested_Party
        fields = [
            'patent_number',
            'patent_number_after',
            'patent_number_before',
            'party_name',
            'party_country_code'
        ]

class PTInterestedPartyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PT_Interested_Party.objects.all()
    serializer_class = PTInterestedPartySerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['patent_number__patent_number', 'party_name', 'party_country_code']
    filterset_class = PTInterestedPartyFilter


#
# PT_Abstract
#
class PTAbstractFilter(django_filters.FilterSet):
    patent_number = django_filters.NumberFilter(field_name='patent_number__patent_number', lookup_expr='exact')
    patent_number_after = django_filters.NumberFilter(field_name='patent_number__patent_number', lookup_expr='gte')
    patent_number_before = django_filters.NumberFilter(field_name='patent_number__patent_number', lookup_expr='lte')
    
    class Meta:
        model = PT_Abstract
        fields = [
            'patent_number',
            'patent_number_after',
            'patent_number_before',
            'language_of_filing_code'
        ]

class PTAbstractViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PT_Abstract.objects.all()
    serializer_class = PTAbstractSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['patent_number__patent_number', 'language_of_filing_code']
    filterset_class = PTAbstractFilter


#
# PT_Disclosure
#
class PTDisclosureFilter(django_filters.FilterSet):
    patent_number = django_filters.NumberFilter(field_name='patent_number__patent_number', lookup_expr='exact')
    patent_number_after = django_filters.NumberFilter(field_name='patent_number__patent_number', lookup_expr='gte')
    patent_number_before = django_filters.NumberFilter(field_name='patent_number__patent_number', lookup_expr='lte')
    
    class Meta:
        model = PT_Disclosure
        fields = [
            'patent_number',
            'patent_number_after',
            'patent_number_before',
            'language_of_filing_code'
        ]

class PTDisclosureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PT_Disclosure.objects.all()
    serializer_class = PTDisclosureSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['patent_number__patent_number', 'language_of_filing_code']
    filterset_class = PTDisclosureFilter


#
# PT_Claim
#
class PTClaimFilter(django_filters.FilterSet):
    patent_number = django_filters.NumberFilter(field_name='patent_number__patent_number', lookup_expr='exact')
    patent_number_after = django_filters.NumberFilter(field_name='patent_number__patent_number', lookup_expr='gte')
    patent_number_before = django_filters.NumberFilter(field_name='patent_number__patent_number', lookup_expr='lte')
    
    class Meta:
        model = PT_Claim
        fields = [
            'patent_number',
            'patent_number_after',
            'patent_number_before',
            'language_of_filing_code'
        ]

class PTClaimViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PT_Claim.objects.all()
    serializer_class = PTClaimSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['patent_number__patent_number', 'language_of_filing_code']
    filterset_class = PTClaimFilter


#
# PT_IPC_Classification
#
class PTIPCClassificationFilter(django_filters.FilterSet):
    patent_number = django_filters.NumberFilter(field_name='patent_number__patent_number', lookup_expr='exact')
    patent_number_after = django_filters.NumberFilter(field_name='patent_number__patent_number', lookup_expr='gte')
    patent_number_before = django_filters.NumberFilter(field_name='patent_number__patent_number', lookup_expr='lte')
    ipc_class = django_filters.CharFilter(field_name='ipc_class', lookup_expr='icontains')

    class Meta:
        model = PT_IPC_Classification
        fields = [
            'patent_number',
            'patent_number_after',
            'patent_number_before',
            'ipc_class'
        ]

class PTIPCClassificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PT_IPC_Classification.objects.all()
    serializer_class = PTIPCClassificationSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['patent_number__patent_number', 'ipc_class']
    filterset_class = PTIPCClassificationFilter
