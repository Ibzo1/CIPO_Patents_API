from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import PTMainWithDetailsSerializer
from django.db.models import Prefetch

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


# class PTMainViewSet(viewsets.ModelViewSet):
#     queryset = PT_Main.objects.all()
#     serializer_class = PTMainSerializer
#     lookup_field = 'patent_number'
#     http_method_names = ['get']

# class PTPriorityClaimViewSet(viewsets.ModelViewSet):
#     queryset = PT_Priority_Claim.objects.all()
#     serializer_class = PTPriorityClaimSerializer
#     lookup_field = 'patent_number'
#     http_method_names = ['get']

# class PTInterestedPartyViewSet(viewsets.ModelViewSet):
#     queryset = PT_Interested_Party.objects.all()
#     serializer_class = PTInterestedPartySerializer
#     lookup_field = 'patent_number'
#     http_method_names = ['get']

# class PTAbstractViewSet(viewsets.ModelViewSet):
#     queryset = PT_Abstract.objects.all()
#     serializer_class = PTAbstractSerializer
#     lookup_field = 'patent_number'
#     http_method_names = ['get']

# class PTDisclosureViewSet(viewsets.ModelViewSet):
#     queryset = PT_Disclosure.objects.all()
#     serializer_class = PTDisclosureSerializer
#     lookup_field = 'patent_number'
#     http_method_names = ['get']

# class PTClaimViewSet(viewsets.ModelViewSet):
#     queryset = PT_Claim.objects.all()
#     serializer_class = PTClaimSerializer
#     lookup_field = 'patent_number'
#     http_method_names = ['get']

# class PTIPCClassificationViewSet(viewsets.ModelViewSet):
#     queryset = PT_IPC_Classification.objects.all()
#     serializer_class = PTIPCClassificationSerializer
#     lookup_field = 'patent_number'
#     http_method_names = ['get']

# class PTMainWithDetailsViewSet(viewsets.ModelViewSet):
#     serializer_class = PTMainWithDetailsSerializer
#     filter_backends = [DjangoFilterBackend, SearchFilter]
#     filterset_fields = ['filing_date']
#     search_fields = ['patent_number', 'application_patent_title_english', 'application_patent_title_french']
#     http_method_names = ['get']
    
    # def get_queryset(self):
    #     queryset = PT_Main.objects.prefetch_related(
    #         'abstracts',
    #         'disclosures',
    #         'claims',
    #         'interested_parties',
    #         'priority_claims',
    #         'ipc_classifications'
    #     )

    #     # Apply search filtering
    #     search = self.request.query_params.get('search', None)
    #     if search:
    #         queryset = queryset.filter(patent_number__icontains=search)
    #     else:
    #         # Default to returning only the first 100 records if no filter is applied
    #         queryset = queryset[:100]

    #     return queryset



