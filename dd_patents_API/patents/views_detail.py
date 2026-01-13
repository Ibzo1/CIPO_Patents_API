from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from drf_yasg.utils import swagger_auto_schema          
from patents.schema import IncludeParam                 
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from .models import PT_Main
from .serializers import PTMainDetailSerializer

class PTMainDetailFilter(django_filters.FilterSet):
    patent_number       = django_filters.NumberFilter(field_name='patent_number', lookup_expr='exact')
    patent_number_after = django_filters.NumberFilter(field_name='patent_number', lookup_expr='gte')
    patent_number_before= django_filters.NumberFilter(field_name='patent_number', lookup_expr='lte')
    filing_date         = django_filters.DateFromToRangeFilter(field_name='filing_date')

    class Meta:
        model  = PT_Main
        fields = ['patent_number', 'patent_number_after', 'patent_number_before',
                  'filing_date']

class PTMainDetailViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Return a single PT_Main with optional nested tables.
    Control nested sets via `include=` query‑param.
        ?include=abstracts,claims          # only those 2
        ?include=all                       # every relation
        (default)                          # abstracts + claims
    """
    serializer_class = PTMainDetailSerializer
    filter_backends  = [SearchFilter, DjangoFilterBackend]
    filterset_class  = PTMainDetailFilter
    search_fields    = ['patent_number', 'application_patent_title_english']

    # Map query‑param tokens → related names
    _REL_MAP = {
        'abstracts':          'abstracts',
        'claims':             'claims',
        'disclosures':        'disclosures',
        'interested_parties': 'interested_parties',
        'priority_claims':    'priority_claims',
        'ipc_classifications':'ipc_classifications',
    }
    _DEFAULT_RELATIONS = ['abstracts', 'claims']

    def get_queryset(self):
        qs = PT_Main.objects.all()
        include_raw = self.request.query_params.get('include', None)

        # Decide which relations to prefetch
        if include_raw:
            include = [x.strip().lower() for x in include_raw.split(',')]
            if 'all' in include:
                rels = list(self._REL_MAP.values())
            else:
                rels = [self._REL_MAP[t] for t in include if t in self._REL_MAP]
        else:
            rels = self._DEFAULT_RELATIONS

        # Apply prefetches
        if rels:
            qs = qs.prefetch_related(*rels)

        return qs
    

    @swagger_auto_schema(
        query_serializer=IncludeParam,
        operation_summary="Detailed patent with selectable nested tables",
        operation_description="""
**Examples**

* Default — main patent plus abstracts & claims  
  `/api/pt_main_detail/?patent_number=2738890`

* Custom include — add priority_claims  
  `/api/pt_main_detail/?patent_number=2738890&include=priority_claims`

* Trim fields — only top‑level patent_number + filing_date + abstract text  
  `/api/pt_main_detail/?patent_number=2738890`
  `&include=abstracts`
  `&fields=patent_number,filing_date,abstracts.abstract_text`
""",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
