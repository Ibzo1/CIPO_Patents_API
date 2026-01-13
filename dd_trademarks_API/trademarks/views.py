from rest_framework import generics
from .models import (
    TmMain, 
    TmClaim, 
    TmMarkDescription, 
    TmCipoClassifications, 
    TmApplicantClassifications, 
    TmRepresentation, 
    TmInterestedParty, 
    TmPriorityClaim, 
    TmEvent,
    TmApplicationDisclaimer,
    TmApplicationText,
    TmTransliteration,
    TmFootnote,
    TmFootnoteFormatted,
    TmHeading,
    TmCancellationCase,
    TmCancellationCaseAction,
    TmOppositionCase,
    TmOppositionCaseAction,

)
from .serializers import (
    TmMainSerializer, 
    TmClaimSerializer, 
    TmMarkDescriptionSerializer, 
    TmCipoClassificationsSerializer, 
    TmApplicantClassificationsSerializer, 
    TmRepresentationSerializer, 
    TmInterestedPartySerializer,
    TmPriorityClaimSerializer,
    TmEventSerializer,
    TmApplicationDisclaimerSerializer,
    TmApplicationTextSerializer,
    TmTransliterationSerializer,
    TmFootnoteSerializer,
    TmFootnoteFormattedSerializer,
    TmHeadingSerializer,
    TmCancellationCaseSerializer,
    TmCancellationCaseActionSerializer,
    TmOppositionCaseSerializer,
    TmOppositionCaseActionSerializer
)

from .filters import TmMainFilter

class TmMainListView(generics.ListAPIView):
    """
    A view that returns a list of all trademarks, with support for filtering.
    """
    # The queryset defines the collection of objects to be returned.
    # Here, we are getting all records from the TmMain table.
    queryset = TmMain.objects.all()

    # The serializer_class tells the view how to format the data.
    # We are using the TmMainSerializer we just created.
    serializer_class = TmMainSerializer

    # This enables filtering on the API. Users can add query parameters
    # to the URL to search for specific records.
    filterset_class = TmMainFilter

class TmClaimListView(generics.ListAPIView):
    queryset = TmClaim.objects.all()
    serializer_class = TmClaimSerializer
    filterset_fields = ['application_number', 'claim_type', 'claim_number']

class TmMarkDescriptionListView(generics.ListAPIView):
    queryset = TmMarkDescription.objects.all()
    serializer_class = TmMarkDescriptionSerializer
    filterset_fields = ['application_number', 'language_code']

class TmCipoClassificationsListView(generics.ListAPIView):
    queryset = TmCipoClassifications.objects.all()
    serializer_class = TmCipoClassificationsSerializer
    filterset_fields = ['application_number', 'nice_classification_code']

class TmApplicantClassificationsListView(generics.ListAPIView):
    queryset = TmApplicantClassifications.objects.all()
    serializer_class = TmApplicantClassificationsSerializer
    filterset_fields = [
        'application_number', 
        'classification_sequence_number',
        'nice_classification_code'
    ]

class TmRepresentationListView(generics.ListAPIView):
    queryset = TmRepresentation.objects.all()
    serializer_class = TmRepresentationSerializer
    filterset_fields = [
        'application_number', 
        'vienna_code',
        'file_name'
    ]

class TmInterestedPartyListView(generics.ListAPIView):
    queryset = TmInterestedParty.objects.all()
    serializer_class = TmInterestedPartySerializer
    filterset_fields = [
        'application_number', 
        'party_name',
        'party_type_code',
        'agent_number'
    ]

class TmPriorityClaimListView(generics.ListAPIView):
    queryset = TmPriorityClaim.objects.all()
    serializer_class = TmPriorityClaimSerializer
    filterset_fields = [
        'application_number', 
        'priority_application_number',
        'priority_country_code'
    ]

class TmEventListView(generics.ListAPIView):
    queryset = TmEvent.objects.all()
    serializer_class = TmEventSerializer
    filterset_fields = [
        'application_number', 
        'action_date',
        'cipo_action_code'
    ]

class TmApplicationDisclaimerListView(generics.ListAPIView):
    queryset = TmApplicationDisclaimer.objects.all()
    serializer_class = TmApplicationDisclaimerSerializer
    filterset_fields = [
        'application_number', 
        'language_code',
        'disclaimer_text_sequence_number'
    ]

class TmApplicationTextListView(generics.ListAPIView):
    queryset = TmApplicationText.objects.all()
    serializer_class = TmApplicationTextSerializer
    filterset_fields = [
        'application_number', 
        'application_text_code',
        'sequence_number'
    ]

class TmTransliterationListView(generics.ListAPIView):
    queryset = TmTransliteration.objects.all()
    serializer_class = TmTransliterationSerializer
    filterset_fields = ['application_number']

class TmFootnoteListView(generics.ListAPIView):
    queryset = TmFootnote.objects.all()
    serializer_class = TmFootnoteSerializer
    filterset_fields = [
        'application_number', 
        'footnote_number',
        'footnote_category_code'
    ]

class TmFootnoteFormattedListView(generics.ListAPIView):
    queryset = TmFootnoteFormatted.objects.all()
    serializer_class = TmFootnoteFormattedSerializer
    filterset_fields = [
        'application_number', 
        'footnote_number',
        'footnote_formatted_text_sequence_number'
    ]

class TmHeadingListView(generics.ListAPIView):
    queryset = TmHeading.objects.all()
    serializer_class = TmHeadingSerializer
    filterset_fields = ['application_number', 'index_heading_number']

class TmCancellationCaseListView(generics.ListAPIView):
    queryset = TmCancellationCase.objects.all()
    serializer_class = TmCancellationCaseSerializer
    filterset_fields = [
        'application_number', 
        'section_44_45_case_number',
        'plaintiff_name'
    ]

class TmCancellationCaseActionListView(generics.ListAPIView):
    queryset = TmCancellationCaseAction.objects.all()
    serializer_class = TmCancellationCaseActionSerializer
    filterset_fields = [
        'application_number', 
        'section_44_45_case_number',
        'section_44_45_actions_code'
    ]

class TmOppositionCaseListView(generics.ListAPIView):
    queryset = TmOppositionCase.objects.all()
    serializer_class = TmOppositionCaseSerializer
    filterset_fields = [
        'application_number', 
        'opposition_case_number',
        'plaintiff_name'
    ]

class TmOppositionCaseActionListView(generics.ListAPIView):
    queryset = TmOppositionCaseAction.objects.all()
    serializer_class = TmOppositionCaseActionSerializer
    filterset_fields = [
        'application_number', 
        'opposition_case_number',
        'opposition_action_code'
    ]