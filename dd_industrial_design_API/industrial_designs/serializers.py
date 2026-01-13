from rest_framework import serializers
from .models import (
    ApplicationClassification,
    ApplicationCorrection,
    ApplicationDescription,
    ApplicationDescriptionTxtFormat,
    ApplicationImage,
    ApplicationInterestedParty,
    ApplicationMain,
    AssignmentCorrection,
    AssignmentInterestedParty,
    AssignmentMain,
)

class ApplicationClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationClassification
        fields = "__all__"

class ApplicationCorrectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationCorrection
        fields = "__all__"

class ApplicationDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationDescription
        fields = "__all__"

class ApplicationDescriptionTxtFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationDescriptionTxtFormat
        fields = "__all__"

class ApplicationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationImage
        fields = "__all__"

class ApplicationInterestedPartySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationInterestedParty
        fields = "__all__"

class ApplicationMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationMain
        fields = "__all__"

class AssignmentCorrectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentCorrection
        fields = "__all__"

class AssignmentInterestedPartySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentInterestedParty
        fields = "__all__"

class AssignmentMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentMain
        fields = "__all__"