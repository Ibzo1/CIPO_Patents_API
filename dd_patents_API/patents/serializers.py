from rest_framework import serializers
from drf_dynamic_fields import DynamicFieldsMixin

from .models import (
    PT_Main,
    PT_Priority_Claim,
    PT_Interested_Party,
    PT_Abstract,
    PT_Disclosure,
    PT_Claim,
    PT_IPC_Classification,
)

# ---------------------------------------------------------------------------
# 1.  ORIGINAL “table → JSON” SERIALIZERS (unchanged)
# ---------------------------------------------------------------------------

class PTMainSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model  = PT_Main
        fields = "__all__"


class PTPriorityClaimSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model  = PT_Priority_Claim
        fields = "__all__"


class PTInterestedPartySerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model  = PT_Interested_Party
        fields = "__all__"


class PTAbstractSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    patent_number = serializers.CharField(source='patent_number.patent_number', read_only=True)

    class Meta:
        model  = PT_Abstract
        fields = [
            "patent_number",
            "language_of_filing_code",
            "abstract_language_code",
            "abstract_text",
            "abstract_text_sequence_number",
        ]


class PTDisclosureSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    patent_number = serializers.CharField(source='patent_number.patent_number', read_only=True)

    class Meta:
        model  = PT_Disclosure
        fields = [
            "patent_number",
            "language_of_filing_code",
            "disclosure_text",
            "disclosure_text_sequence_number",
        ]


class PTClaimSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    patent_number = serializers.CharField(source='patent_number.patent_number', read_only=True)

    class Meta:
        model  = PT_Claim
        fields = [
            "patent_number",
            "language_of_filing_code",
            "claims_text",
            "claim_text_sequence_number",
        ]


class PTIPCClassificationSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model  = PT_IPC_Classification
        fields = "__all__"


# ---------------------------------------------------------------------------
# 2.  NEW  “mini / nested” SERIALIZERS  (used inside the detail endpoint)
# ---------------------------------------------------------------------------

class PTAbstractNested(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model  = PT_Abstract
        fields = ["language_of_filing_code", "abstract_text"]


class PTClaimNested(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model  = PT_Claim
        fields = ["language_of_filing_code", "claims_text"]


class PTPriorityClaimNested(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model  = PT_Priority_Claim
        fields = ["priority_claim_country_code", "foreign_application_patent_number"]


# ---------------------------------------------------------------------------
# 3.  PATENT “DETAIL” SERIALIZER – NESTS RELATED DATA
#     (used by the new `PTMainDetailViewSet`)
# ---------------------------------------------------------------------------

class PTMainDetailSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    abstracts           = PTAbstractNested(many=True,  read_only=True)
    claims              = PTClaimNested(many=True,     read_only=True)
    disclosures         = PTDisclosureSerializer(many=True, read_only=True)
    interested_parties  = PTInterestedPartySerializer(many=True, read_only=True)
    priority_claims     = PTPriorityClaimNested(many=True, read_only=True)
    ipc_classifications = PTIPCClassificationSerializer(many=True, read_only=True)

    class Meta:
        model  = PT_Main
        fields = [
            "patent_number",
            "filing_date",
            "application_patent_title_english",
            # nested / joined relations
            "abstracts",
            "claims",
            "disclosures",
            "interested_parties",
            "priority_claims",
            "ipc_classifications",
        ]