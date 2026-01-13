from django.db import models

SCHEMA = 'id_csv_2024_03_07'

class BaseID(models.Model):
    id = models.BigAutoField(primary_key=True)
    class Meta:
        abstract = True
        managed = False
        default_permissions = ()

class ApplicationClassification(BaseID):
    application_number = models.TextField(db_index=True)
    extension_number = models.TextField()
    classification_kind_code = models.TextField()
    classification_kind = models.TextField()
    classification_number = models.TextField()
    classification_primary = models.TextField()
    classification_sub = models.TextField()
    classification_sub_sub = models.TextField()
    product_description = models.TextField()

    class Meta(BaseID.Meta):
        db_table = f'"{SCHEMA}"."application_classification"'
        verbose_name = "ID – application classification"

# ---------------------------------------------------------------------------------------

class ApplicationCorrection(BaseID):
    application_number = models.TextField(db_index=True)
    extension_number = models.TextField()
    publication_identifier = models.TextField()
    publication_section = models.TextField()
    correction_date = models.DateField()

    class Meta(BaseID.Meta):
        db_table = f'"{SCHEMA}"."application_correction"'
        verbose_name = "ID – application correction"

# ---------------------------------------------------------------------------------------

class ApplicationDescription(BaseID):
    application_number = models.TextField(db_index=True)
    extension_number = models.TextField()
    design_description_text_sequence_number = models.IntegerField()
    design_description_language_code = models.TextField()
    design_description = models.TextField()

    class Meta(BaseID.Meta):
        db_table = f'"{SCHEMA}"."application_description"'
        verbose_name = "ID – application description"

# ---------------------------------------------------------------------------------------

class ApplicationDescriptionTxtFormat(BaseID):
    application_number = models.TextField(db_index=True)
    extension_number = models.TextField()
    design_description_language_code = models.TextField()
    design_description = models.TextField()

    class Meta(BaseID.Meta):
        db_table = f'"{SCHEMA}"."application_description_txt_format"'
        verbose_name = "ID – application description TXT-format"

# ---------------------------------------------------------------------------------------

class ApplicationImage(BaseID):
    application_number = models.TextField(db_index=True)
    extension_number = models.TextField()
    filename = models.TextField()
    colour = models.TextField()
    colour_type = models.TextField()
    image_kind = models.TextField()
    image_kind_code = models.TextField()

    class Meta(BaseID.Meta):
        db_table = f'"{SCHEMA}"."application_image"'
        verbose_name = "ID – application image"

# ---------------------------------------------------------------------------------------

class ApplicationInterestedParty(BaseID):
    application_number = models.TextField(db_index=True)
    extension_number = models.TextField()
    first_name = models.TextField()
    last_name = models.TextField()
    organization_name = models.TextField()
    role = models.TextField()
    role_code = models.TextField()
    address = models.TextField()
    city = models.TextField()
    country = models.TextField()
    country_code = models.TextField()
    postal_code = models.TextField()
    province_state = models.TextField()

    class Meta(BaseID.Meta):
        db_table = f'"{SCHEMA}"."application_interested_party"'
        verbose_name = "ID – application interested party"

# ---------------------------------------------------------------------------------------

class ApplicationMain(BaseID):
    application_number = models.TextField(db_index=True)
    extension_number = models.TextField()
    parent_application_number = models.TextField()
    application_language_code = models.TextField()
    application_modified_date = models.DateField()
    design_current_status_code = models.TextField()
    design_status = models.TextField()
    design_title = models.TextField()
    design_title_language_code = models.TextField()
    designated_country_code = models.TextField()
    designated_country = models.TextField()
    filing_country = models.TextField()
    filing_country_code = models.TextField()
    international_application_kind = models.TextField()
    international_registration_number = models.TextField()
    maintenance_indicator_type = models.TextField()
    maintenance_indicator = models.TextField()
    novelty_statement = models.TextField()
    novelty_statement_language_type = models.TextField()
    novelty_statement_sequence_num = models.TextField()
    priority_claim_eu = models.TextField()
    priority_claim_kind = models.TextField()
    priority_country = models.TextField()
    priority_country_code = models.TextField()
    priority_number = models.TextField()
    priority_date = models.DateField()
    priority_sequence_num = models.TextField()
    priority_status_code = models.TextField()
    priority_status = models.TextField()
    publication_identifier = models.TextField()
    receiving_office_country_code = models.TextField()
    receiving_office_country = models.TextField()
    registration_date = models.DateField()
    registration_expiry_date = models.DateField()
    registration_file_name = models.TextField()
    registration_number = models.TextField()
    registration_office_country_code = models.TextField()
    registration_office_country = models.TextField()
    total_graphical_images = models.TextField()
    total_number_of_designs = models.TextField()
    filing_date = models.DateField()
    publication_date = models.DateField()

    class Meta(BaseID.Meta):
        db_table = f'"{SCHEMA}"."application_main"'
        verbose_name = "ID – application main"

# ---------------------------------------------------------------------------------------

class AssignmentCorrection(BaseID):
    assignment_number = models.TextField(db_index=True)
    publication_identifier = models.TextField()
    publication_section = models.TextField()
    correction_date = models.DateField()

    class Meta(BaseID.Meta):
        db_table = f'"{SCHEMA}"."assignment_correction"'
        verbose_name = "ID – assignment correction"

# ---------------------------------------------------------------------------------------

class AssignmentInterestedParty(BaseID):
    assignment_number  = models.TextField(db_index=True)
    first_name = models.TextField()
    last_name = models.TextField()
    organization_name = models.TextField()
    role = models.TextField()
    role_code = models.TextField()
    address = models.TextField()
    city = models.TextField()
    country = models.TextField()
    country_code = models.TextField()
    postal_code = models.TextField()
    province_state = models.TextField()

    class Meta(BaseID.Meta):
        db_table = f'"{SCHEMA}"."assignment_interested_party"'
        verbose_name = "ID – assignment interested party"

# ---------------------------------------------------------------------------------------

class AssignmentMain(BaseID):
    assignment_number = models.TextField(db_index=True)
    application_number = models.TextField()
    extension_number = models.TextField()
    assignment_registration_date = models.DateField()
    assignment_status_type = models.TextField()
    assignment_status = models.TextField()
    assignment_type_code = models.TextField()
    assignment_type = models.TextField()
    legal_disclaimer = models.TextField()
    ownership_change_prior_to_filing = models.TextField()

    class Meta(BaseID.Meta):
        db_table = f'"{SCHEMA}"."assignment_main"'
        verbose_name = "ID – assignment main"