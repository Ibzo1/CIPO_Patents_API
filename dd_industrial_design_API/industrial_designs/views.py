from rest_framework import viewsets
from rest_framework import filters as drf_filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
import django_filters as df

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

from .serializers import (
    ApplicationClassificationSerializer,
    ApplicationCorrectionSerializer,
    ApplicationDescriptionSerializer,
    ApplicationDescriptionTxtFormatSerializer,
    ApplicationImageSerializer,
    ApplicationInterestedPartySerializer,
    ApplicationMainSerializer,
    AssignmentCorrectionSerializer,
    AssignmentInterestedPartySerializer,
    AssignmentMainSerializer,
)

class OmitFilterBackend(drf_filters.BaseFilterBackend):
    param = "omit"

    def filter_queryset(self, request, queryset, view):
        raw = request.query_params.get(self.param, "")
        if not raw:
            return queryset

        parts = [p.strip() for p in raw.split(",") if p.strip()]
        if not parts:
            return queryset

        text_cols = {
            f.name for f in queryset.model._meta.get_fields()
            if isinstance(f, (models.CharField, models.TextField))
               and not f.many_to_many and not f.one_to_many
        }

        overall_q = models.Q()
        for token in parts:
            if ":" in token:
                col, word = token.split(":", 1)
                if col in text_cols:
                    overall_q |= models.Q(**{f"{col}__icontains": word})
            else:
                word = token
                q = models.Q()
                for col in text_cols:
                    q |= models.Q(**{f"{col}__icontains": word})
                overall_q |= q

        return queryset.exclude(overall_q)

COMMON_FILTERS = [
    OmitFilterBackend,
    DjangoFilterBackend,
    drf_filters.OrderingFilter,
    drf_filters.SearchFilter,
]

def make_ab_filterset(model):
    range_types = (
        models.DateField, models.DateTimeField,
        models.IntegerField, models.BigIntegerField,
        models.FloatField, models.DecimalField,
    )

    attrs = {"Meta": type("Meta", (), {"model": model, "fields": "__all__"})}

    for f in model._meta.get_fields():
        if isinstance(f, range_types) and not f.many_to_many and not f.one_to_many:
            attrs[f"{f.name}_after"]  = df.Filter(field_name=f.name, lookup_expr="gte")
            attrs[f"{f.name}_before"] = df.Filter(field_name=f.name, lookup_expr="lte")

    return type(f"{model.__name__}FilterSet", (df.FilterSet,), attrs)

class ReadOnlyMixin(viewsets.ReadOnlyModelViewSet):
    lookup_field = "id"
    lookup_url_kwarg = "pk"
    pagination_class = None
    filter_backends = COMMON_FILTERS
    ordering_fields = "__all__"
    search_fields = "__all__"

    # helper route
    @property
    def filterset_class(self):
        if not hasattr(self, "_ab_filterset"):
            self._ab_filterset = make_ab_filterset(self.queryset.model)
        return self._ab_filterset
    
    @action(detail=False, url_path=r"by-number/(?P<number>[^/]+)")
    def by_number(self, request, number=None):
        field = getattr(self, "number_field", "application_number")
        qs = self.filter_queryset(self.get_queryset().filter(**{field: number}))
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(self.get_serializer(page, many=True).data)
        return Response(self.get_serializer(qs, many=True).data)

class ApplicationClassificationViewSet(ReadOnlyMixin):
    queryset = ApplicationClassification.objects.all()
    serializer_class = ApplicationClassificationSerializer
    number_field = "application_number"
    filterset_fields = ["classification_number"]
    search_fields = ["application_number", "classification_number", "product_description"]
    ordering_fields = ["application_number", "classification_number"]

# ---------------------------------------------------------------------------------------

class ApplicationCorrectionViewSet(ReadOnlyMixin):
    queryset = ApplicationCorrection.objects.all()
    serializer_class = ApplicationCorrectionSerializer
    filter_backends = COMMON_FILTERS
    search_fields = ["application_number", "publication_identifier"]
    ordering_fields = ["application_number", "correction_date"]

# ---------------------------------------------------------------------------------------

class ApplicationDescriptionViewSet(ReadOnlyMixin):
    queryset = ApplicationDescription.objects.all()
    serializer_class = ApplicationDescriptionSerializer
    filter_backends = COMMON_FILTERS
    search_fields = ["application_number", "design_description"]
    ordering_fields = ["application_number", "design_description_text_sequence_number"]

# ---------------------------------------------------------------------------------------

class ApplicationDescriptionTxtFormatViewSet(ReadOnlyMixin):
    queryset = ApplicationDescriptionTxtFormat.objects.all()
    serializer_class = ApplicationDescriptionTxtFormatSerializer
    filter_backends = COMMON_FILTERS
    search_fields = ["application_number", "design_description"]
    ordering_fields = ["application_number"]

# ---------------------------------------------------------------------------------------

class ApplicationImageViewSet(ReadOnlyMixin):
    queryset = ApplicationImage.objects.all()
    serializer_class = ApplicationImageSerializer
    filter_backends = COMMON_FILTERS
    search_fields = ["application_number", "filename"]
    ordering_fields = ["application_number", "filename"]

# ---------------------------------------------------------------------------------------

class ApplicationInterestedPartyViewSet(ReadOnlyMixin):
    queryset = ApplicationInterestedParty.objects.all()
    serializer_class = ApplicationInterestedPartySerializer
    filter_backends = COMMON_FILTERS
    search_fields = ["application_number", "last_name", "organization_name"]
    ordering_fields = ["application_number", "last_name", "organization_name"]

# ---------------------------------------------------------------------------------------

class ApplicationMainViewSet(ReadOnlyMixin):
    queryset = ApplicationMain.objects.all()
    serializer_class = ApplicationMainSerializer
    filter_backends = COMMON_FILTERS
    search_fields = ["application_number", "design_title", "registration_number"]
    ordering_fields = ["application_number", "filing_date", "publication_date"]

# ---------------------------------------------------------------------------------------

class AssignmentCorrectionViewSet(ReadOnlyMixin):
    queryset = AssignmentCorrection.objects.all()
    serializer_class = AssignmentCorrectionSerializer
    number_field = "assignment_number"
    filter_backends = COMMON_FILTERS
    search_fields = ["assignment_number", "publication_identifier", "publication_section"]
    ordering_fields = ["assignment_number", "correction_date"]

# ---------------------------------------------------------------------------------------

class AssignmentInterestedPartyViewSet(ReadOnlyMixin):
    queryset = AssignmentInterestedParty.objects.all()
    serializer_class = AssignmentInterestedPartySerializer
    number_field = "assignment_number"
    filter_backends = COMMON_FILTERS
    search_fields = ["assignment_number", "last_name", "organization_name"]
    ordering_fields = ["assignment_number", "last_name", "organization_name"]

# ---------------------------------------------------------------------------------------

class AssignmentMainViewSet(ReadOnlyMixin):
    queryset = AssignmentMain.objects.all()
    serializer_class = AssignmentMainSerializer
    filter_backends = COMMON_FILTERS
    search_fields = ["assignment_number", "application_number"]
    ordering_fields = [
        "assignment_number",
        "assignment_registration_date",
        "assignment_status",
    ]
