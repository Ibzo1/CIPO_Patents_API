from django.contrib import admin
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

@admin.register(ApplicationClassification)
class ApplicationClassificationAdmin(admin.ModelAdmin):
    list_display = (
        "application_number",
        "classification_number",
        "classification_kind",
        "classification_primary",
        "id",
    )
    search_fields = (
        "application_number", 
        "classification_number",
        "product_description",
        "id",
    )

# ---------------------------------------------------------------------------------------

@admin.register(ApplicationCorrection)
class ApplicationCorrectionAdmin(admin.ModelAdmin):
    list_display = (
        "application_number",
        "publication_identifier",
        "publication_section",
        "correction_date",
        "id",
    )
    search_fields = (
        "application_number", 
        "publication_identifier", 
        "id",
    )

# ---------------------------------------------------------------------------------------

@admin.register(ApplicationDescription)
class ApplicationDescriptionAdmin(admin.ModelAdmin):
    list_display = (
        "application_number",
        "design_description_language_code",
        "design_description_text_sequence_number",
        "id",
    )
    search_fields = (
        "application_number", 
        "design_description", 
        "id",
    )

# ---------------------------------------------------------------------------------------

@admin.register(ApplicationDescriptionTxtFormat)
class ApplicationDescriptionTxtFormatAdmin(admin.ModelAdmin):
    list_display  = (
        "application_number",
        "design_description_language_code",
        "id",
    )
    search_fields = (
        "application_number", 
        "id",
    )

# ---------------------------------------------------------------------------------------

@admin.register(ApplicationImage)
class ApplicationImageAdmin(admin.ModelAdmin):
    list_display = (
        "application_number", 
        "filename", 
        "image_kind_code",
        "colour_type",
        "id",
    )
    search_fields = (
        "application_number", 
        "filename",
        "id",
    )

# ---------------------------------------------------------------------------------------

@admin.register(ApplicationInterestedParty)
class ApplicationInterestedPartyAdmin(admin.ModelAdmin):
    list_display  = (
        "application_number",
        "first_name",
        "last_name",
        "organization_name",
        "role_code",
        "id",
    )
    search_fields = (
        "application_number", 
        "last_name", 
        "organization_name"
        "id",
    )

# ---------------------------------------------------------------------------------------

@admin.register(ApplicationMain)
class ApplicationMainAdmin(admin.ModelAdmin):
    list_display = (
        "application_number",
        "design_status",
        "filing_date",
        "publication_date",
        "registration_date",
        "registration_expiry_date",
        "priority_country_code",
        "priority_date",
        "total_graphical_images",
        "total_number_of_designs",
        "id",
    )
    search_fields = (
        "application_number",
        "design_title",
        "priority_number",
        "registration_number",
        "id",
    )
    list_filter = (
        "design_status",
        "application_language_code",
        "filing_country_code",
        "designated_country_code",
    )
    ordering = ("-filing_date",)

# ---------------------------------------------------------------------------------------

@admin.register(AssignmentCorrection)
class AssignmentCorrectionAdmin(admin.ModelAdmin):
    list_display  = (
        "assignment_number",
        "publication_identifier",
        "publication_section",
        "correction_date",
        "id",
    )
    search_fields = (
        "assignment_number", 
        "publication_identifier",
        "id",
    )
# ---------------------------------------------------------------------------------------

@admin.register(AssignmentInterestedParty)
class AssignmentInterestedPartyAdmin(admin.ModelAdmin):
    list_display  = (
        "assignment_number",
        "first_name",
        "last_name",
        "organization_name",
        "role_code",
        "id",
    )
    search_fields = (
        "assignment_number", 
        "last_name", 
        "organization_name",
        "id",
    )

# ---------------------------------------------------------------------------------------

@admin.register(AssignmentMain)
class AssignmentMainAdmin(admin.ModelAdmin):
    list_display = (
        "assignment_number",
        "application_number",
        "assignment_registration_date",
        "assignment_status",
        "assignment_type",
        "id",
    )
    search_fields = (
        "assignment_number", 
        "application_number",
        "id",
    )
    list_filter = (
        "assignment_status", 
        "assignment_type_code",
    )