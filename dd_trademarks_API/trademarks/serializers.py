from rest_framework import serializers
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
    TmOppositionCaseAction
)

class TmMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = TmMain
        fields = '__all__'  # This will include all fields from the table

class TmClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = TmClaim
        fields = '__all__'

class TmMarkDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TmMarkDescription
        fields = '__all__'

class TmCipoClassificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TmCipoClassifications
        fields = '__all__'

class TmApplicantClassificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TmApplicantClassifications
        fields = '__all__'

class TmRepresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TmRepresentation
        fields = '__all__'

class TmInterestedPartySerializer(serializers.ModelSerializer):
    class Meta:
        model = TmInterestedParty
        fields = '__all__'

class TmPriorityClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = TmPriorityClaim
        fields = '__all__'

class TmEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TmEvent
        fields = '__all__'

class TmApplicationDisclaimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TmApplicationDisclaimer
        fields = '__all__'

class TmApplicationTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = TmApplicationText
        fields = '__all__'

class TmTransliterationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TmTransliteration
        fields = '__all__'

class TmFootnoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TmFootnote
        fields = '__all__'

class TmFootnoteFormattedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TmFootnoteFormatted
        fields = '__all__'

class TmHeadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TmHeading
        fields = '__all__'

class TmCancellationCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TmCancellationCase
        fields = '__all__'

class TmCancellationCaseActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TmCancellationCaseAction
        fields = '__all__'

class TmOppositionCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TmOppositionCase
        fields = '__all__'

class TmOppositionCaseActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TmOppositionCaseAction
        fields = '__all__'