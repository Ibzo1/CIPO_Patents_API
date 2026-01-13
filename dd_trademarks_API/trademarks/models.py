# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TmApplicantClassifications(models.Model):
    application_number = models.OneToOneField('TmMain', models.DO_NOTHING, db_column='application_number', primary_key=True)  # The composite primary key (application_number, classification_sequence_number, classification_indicator_line_sequence_number) found, that is not supported. The first column is selected.
    classification_sequence_number = models.TextField()
    classification_indicator_line_sequence_number = models.IntegerField()
    classification_indicator_description = models.TextField(blank=True, null=True)
    nice_edition_number = models.SmallIntegerField(blank=True, null=True)
    nice_classification_code = models.SmallIntegerField(blank=True, null=True)
    nice_classification = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tm_applicant_classifications'
        unique_together = (('application_number', 'classification_sequence_number', 'classification_indicator_line_sequence_number'),)


class TmApplicationDisclaimer(models.Model):
    application_number = models.OneToOneField('TmMain', models.DO_NOTHING, db_column='application_number', primary_key=True)  # The composite primary key (application_number, language_code, disclaimer_text_sequence_number) found, that is not supported. The first column is selected.
    language_code = models.TextField()
    disclaimer_text_sequence_number = models.IntegerField()
    disclaimer_text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tm_application_disclaimer'
        unique_together = (('application_number', 'language_code', 'disclaimer_text_sequence_number'),)


class TmApplicationText(models.Model):
    application_number = models.OneToOneField('TmMain', models.DO_NOTHING, db_column='application_number', primary_key=True)  # The composite primary key (application_number, application_text_code, sequence_number, secondary_sequence_number) found, that is not supported. The first column is selected.
    application_text_code = models.SmallIntegerField()
    sequence_number = models.IntegerField()
    secondary_sequence_number = models.IntegerField()
    application_text_details = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tm_application_text'
        unique_together = (('application_number', 'application_text_code', 'sequence_number', 'secondary_sequence_number'),)


class TmCancellationCase(models.Model):
    application_number = models.OneToOneField('TmMain', models.DO_NOTHING, db_column='application_number', primary_key=True)  # The composite primary key (application_number, section_44_45_case_number) found, that is not supported. The first column is selected.
    section_44_45_case_number = models.IntegerField()
    legal_proceeding_type_description_in_english = models.TextField(blank=True, null=True)
    legal_proceeding_type_description_in_french = models.TextField(blank=True, null=True)
    section_44_45_filing_date = models.DateField(blank=True, null=True)
    wipo_section_44_45_status_category_code = models.SmallIntegerField(blank=True, null=True)
    section_44_45_status_code = models.SmallIntegerField(blank=True, null=True)
    section_44_45_status_date = models.DateField(blank=True, null=True)
    entity_name_of_the_legal_proceeding_defendant = models.TextField(blank=True, null=True)
    defendant_language_code = models.TextField(blank=True, null=True)
    defendant_address_line_1 = models.TextField(blank=True, null=True)
    defendant_address_line_2 = models.TextField(blank=True, null=True)
    defendant_address_line_3 = models.TextField(blank=True, null=True)
    defendant_country_code = models.TextField(blank=True, null=True)
    contact_name_of_defendant = models.TextField(blank=True, null=True)
    contact_language_code_of_defendant = models.TextField(blank=True, null=True)
    contact_address_line_1_of_defendant = models.TextField(blank=True, null=True)
    contact_address_line_2_of_defendant = models.TextField(blank=True, null=True)
    contact_address_line_3_of_defendant = models.TextField(blank=True, null=True)
    contact_province_name_of_defendant = models.TextField(blank=True, null=True)
    contact_country_code_of_defendant = models.TextField(blank=True, null=True)
    contact_postal_code_of_defendant = models.TextField(blank=True, null=True)
    agent_name_of_defendant = models.TextField(blank=True, null=True)
    agent_language_code_of_defendant = models.TextField(blank=True, null=True)
    agent_address_line_1_of_defendant = models.TextField(blank=True, null=True)
    agent_address_line_2_of_defendant = models.TextField(blank=True, null=True)
    agent_address_line_3_of_defendant = models.TextField(blank=True, null=True)
    agent_province_name_of_defendant = models.TextField(blank=True, null=True)
    agent_country_code_of_defendant = models.TextField(blank=True, null=True)
    agent_postal_code_of_defendant = models.TextField(blank=True, null=True)
    plaintiff_name = models.TextField(blank=True, null=True)
    plaintiff_legal_name = models.TextField(blank=True, null=True)
    plaintiff_language_code = models.TextField(blank=True, null=True)
    plaintiff_address_line_1 = models.TextField(blank=True, null=True)
    plaintiff_address_line_2 = models.TextField(blank=True, null=True)
    plaintiff_address_line_3 = models.TextField(blank=True, null=True)
    plaintiff_country_code = models.TextField(blank=True, null=True)
    contact_name_of_plaintiff = models.TextField(blank=True, null=True)
    contact_language_code_of_plaintiff = models.TextField(blank=True, null=True)
    contact_address_line_1_of_plaintiff = models.TextField(blank=True, null=True)
    contact_address_line_2_of_plaintiff = models.TextField(blank=True, null=True)
    contact_address_line_3_of_plaintiff = models.TextField(blank=True, null=True)
    contact_province_name_of_plaintiff = models.TextField(blank=True, null=True)
    contact_country_code_of_plaintiff = models.TextField(blank=True, null=True)
    contact_postal_code_of_plaintiff = models.TextField(blank=True, null=True)
    agent_number_of_plaintiff = models.IntegerField(blank=True, null=True)
    agent_name_of_plaintiff = models.TextField(blank=True, null=True)
    agent_language_code_of_plaintiff = models.TextField(blank=True, null=True)
    agent_address_line_1_of_plaintiff = models.TextField(blank=True, null=True)
    agent_address_line_2_of_plaintiff = models.TextField(blank=True, null=True)
    agent_address_line_3_of_plaintiff = models.TextField(blank=True, null=True)
    agent_province_name_of_plaintiff = models.TextField(blank=True, null=True)
    agent_country_code_of_plaintiff = models.TextField(blank=True, null=True)
    agent_postal_code_of_plaintiff = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tm_cancellation_case'
        unique_together = (('application_number', 'section_44_45_case_number'),)


class TmCancellationCaseAction(models.Model):
    cancellation_case_action_id = models.AutoField(primary_key=True)
    application_number = models.ForeignKey(TmCancellationCase, models.DO_NOTHING, db_column='application_number')
    section_44_45_case_number = models.IntegerField()
    additional_comment = models.TextField(blank=True, null=True)
    proceeding_effective_date = models.DateField(blank=True, null=True)
    legal_proceeding_type_description_in_english = models.TextField(blank=True, null=True)
    legal_proceeding_type_description_in_french = models.TextField(blank=True, null=True)
    section_44_45_filing_date = models.DateField(blank=True, null=True)
    wipo_section_44_45_status_category_code = models.SmallIntegerField(blank=True, null=True)
    section_44_45_status_code = models.SmallIntegerField(blank=True, null=True)
    section_44_45_status_date = models.DateField(blank=True, null=True)
    section_44_45_stage_code = models.IntegerField(blank=True, null=True)
    section_44_45_case_status = models.TextField(blank=True, null=True)
    section_44_45_actions_code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tm_cancellation_case_action'


class TmCipoClassifications(models.Model):
    application_number = models.OneToOneField('TmMain', models.DO_NOTHING, db_column='application_number', primary_key=True)  # The composite primary key (application_number, nice_classification_code) found, that is not supported. The first column is selected.
    classification_kind_code = models.TextField(blank=True, null=True)
    nice_classification_code = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'tm_cipo_classifications'
        unique_together = (('application_number', 'nice_classification_code'),)


class TmClaim(models.Model):
    application_number = models.OneToOneField('TmMain', models.DO_NOTHING, db_column='application_number', primary_key=True)  # The composite primary key (application_number, claim_type, claim_number) found, that is not supported. The first column is selected.
    claim_type = models.SmallIntegerField()
    claim_number = models.IntegerField()
    claim_text = models.TextField(blank=True, null=True)
    claim_code = models.SmallIntegerField(blank=True, null=True)
    structure_claim_date = models.DateField(blank=True, null=True)
    claim_year_number = models.SmallIntegerField(blank=True, null=True)
    claim_month_number = models.SmallIntegerField(blank=True, null=True)
    claim_day_number = models.SmallIntegerField(blank=True, null=True)
    claim_country_code = models.TextField(blank=True, null=True)
    foreign_registration_number = models.TextField(blank=True, null=True)
    goods_services_reference_identifier = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tm_claim'
        unique_together = (('application_number', 'claim_type', 'claim_number'),)


class TmEvent(models.Model):
    event_id = models.AutoField(primary_key=True)
    application_number = models.ForeignKey('TmMain', models.DO_NOTHING, db_column='application_number')
    action_date = models.DateField(blank=True, null=True)
    response_date = models.DateField(blank=True, null=True)
    additional_information_comment = models.TextField(blank=True, null=True)
    wipo_action_type = models.TextField(blank=True, null=True)
    cipo_action_code = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tm_event'


class TmFootnote(models.Model):
    application_number = models.OneToOneField('TmMain', models.DO_NOTHING, db_column='application_number', primary_key=True)  # The composite primary key (application_number, footnote_number, footnote_text_line_sequence_number) found, that is not supported. The first column is selected.
    footnote_number = models.IntegerField()
    footnote_text_line_sequence_number = models.IntegerField()
    footnote_text_line_description = models.TextField(blank=True, null=True)
    footnote_category_code = models.SmallIntegerField(blank=True, null=True)
    footnote_change_date = models.DateField(blank=True, null=True)
    footnote_registration_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tm_footnote'
        unique_together = (('application_number', 'footnote_number', 'footnote_text_line_sequence_number'),)


class TmFootnoteFormatted(models.Model):
    application_number = models.OneToOneField('TmMain', models.DO_NOTHING, db_column='application_number', primary_key=True)  # The composite primary key (application_number, footnote_number, footnote_formatted_text_sequence_number) found, that is not supported. The first column is selected.
    footnote_number = models.IntegerField()
    footnote_formatted_text_sequence_number = models.IntegerField()
    footnote_formatted_text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tm_footnote_formatted'
        unique_together = (('application_number', 'footnote_number', 'footnote_formatted_text_sequence_number'),)


class TmHeading(models.Model):
    application_number = models.OneToOneField('TmMain', models.DO_NOTHING, db_column='application_number', primary_key=True)  # The composite primary key (application_number, index_heading_number) found, that is not supported. The first column is selected.
    index_heading_number = models.IntegerField()
    index_heading_comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tm_heading'
        unique_together = (('application_number', 'index_heading_number'),)


class TmInterestedParty(models.Model):
    interested_party_id = models.AutoField(primary_key=True)
    application_number = models.ForeignKey('TmMain', models.DO_NOTHING, db_column='application_number')
    party_type_code = models.SmallIntegerField(blank=True, null=True)
    party_language_code = models.TextField(blank=True, null=True)
    party_name = models.TextField(blank=True, null=True)
    party_address_line_1 = models.TextField(blank=True, null=True)
    party_address_line_2 = models.TextField(blank=True, null=True)
    party_address_line_3 = models.TextField(blank=True, null=True)
    party_address_line_4 = models.TextField(blank=True, null=True)
    party_address_line_5 = models.TextField(blank=True, null=True)
    party_province_name = models.TextField(blank=True, null=True)
    party_country_code = models.TextField(blank=True, null=True)
    party_postal_code = models.TextField(blank=True, null=True)
    contact_language_code = models.TextField(blank=True, null=True)
    contact_name = models.TextField(blank=True, null=True)
    contact_address_line_1 = models.TextField(blank=True, null=True)
    contact_address_line_2 = models.TextField(blank=True, null=True)
    contact_address_line_3 = models.TextField(blank=True, null=True)
    contact_province_name = models.TextField(blank=True, null=True)
    contact_country_code = models.TextField(blank=True, null=True)
    contact_postal_code = models.TextField(blank=True, null=True)
    current_owner_legal_name = models.TextField(blank=True, null=True)
    agent_number = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tm_interested_party'


class TmMain(models.Model):
    application_number = models.TextField(primary_key=True)
    filing_date = models.DateField(blank=True, null=True)
    publication_date = models.DateField(blank=True, null=True)
    registration_date = models.DateField(blank=True, null=True)
    registration_office_country_code = models.TextField(blank=True, null=True)
    receiving_office_country_code = models.TextField(blank=True, null=True)
    receiving_office_date = models.DateField(blank=True, null=True)
    assigning_office_country_code = models.TextField(blank=True, null=True)
    registration_number = models.CharField(max_length=255, blank=True, null=True)
    legislation_code = models.IntegerField(blank=True, null=True)
    filing_place = models.TextField(blank=True, null=True)
    application_reference_number = models.TextField(blank=True, null=True)
    application_language_code = models.TextField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    termination_date = models.DateField(blank=True, null=True)
    wipo_status_code = models.IntegerField(blank=True, null=True)
    current_status_date = models.DateField(blank=True, null=True)
    association_category_id = models.TextField(blank=True, null=True)
    associated_application_number = models.BigIntegerField(blank=True, null=True)
    mark_category = models.TextField(blank=True, null=True)
    divisional_application_country_code = models.TextField(blank=True, null=True)
    divisional_application_number = models.BigIntegerField(blank=True, null=True)
    divisional_application_date = models.DateField(blank=True, null=True)
    international_registration_number = models.CharField(max_length=255, blank=True, null=True)
    mark_type_code = models.IntegerField(blank=True, null=True)
    mark_verbal_element_text = models.TextField(blank=True, null=True)
    mark_significant_verbal_element_text = models.TextField(blank=True, null=True)
    mark_translation_text = models.TextField(blank=True, null=True)
    expungement_indicator = models.BooleanField(blank=True, null=True)
    distinctiveness_indicator = models.BooleanField(blank=True, null=True)
    distinctiveness_description = models.TextField(blank=True, null=True)
    evidence_of_use_indicator = models.BooleanField(blank=True, null=True)
    evidence_of_use_description = models.TextField(blank=True, null=True)
    restriction_of_use_description = models.TextField(blank=True, null=True)
    cipo_standard_message_description = models.TextField(blank=True, null=True)
    opposition_start_date = models.DateField(blank=True, null=True)
    opposition_end_date = models.DateField(blank=True, null=True)
    total_nice_classifications_number = models.IntegerField(blank=True, null=True)
    foreign_application_indicator = models.BooleanField(blank=True, null=True)
    foreign_registration_indicator = models.BooleanField(blank=True, null=True)
    used_in_canada_indicator = models.BooleanField(blank=True, null=True)
    proposed_use_in_canada_indicator = models.BooleanField(blank=True, null=True)
    classification_term_office_country_code = models.TextField(blank=True, null=True)
    classification_term_source_category = models.TextField(blank=True, null=True)
    classification_term_english_description = models.TextField(blank=True, null=True)
    publication_id = models.TextField(blank=True, null=True)
    publication_status = models.TextField(blank=True, null=True)
    authorization_of_use_date = models.DateField(blank=True, null=True)
    authorization_code = models.IntegerField(blank=True, null=True)
    authorization_description = models.TextField(blank=True, null=True)
    register_code = models.TextField(blank=True, null=True)
    application_abandoned_date = models.DateField(blank=True, null=True)
    allowed_date = models.DateField(blank=True, null=True)
    renewal_date = models.DateField(blank=True, null=True)
    trademark_class_code = models.IntegerField(blank=True, null=True)
    geographical_indication_kind_category_code = models.IntegerField(blank=True, null=True)
    geographical_indication_translation_sequence_number = models.IntegerField(blank=True, null=True)
    geographical_indication_translation_text = models.TextField(blank=True, null=True)
    doubtful_case_application_number = models.CharField(max_length=255, blank=True, null=True)
    doubtful_case_registration_number = models.CharField(max_length=255, blank=True, null=True)
    cipo_status_code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tm_main'


class TmMarkDescription(models.Model):
    application_number = models.OneToOneField(TmMain, models.DO_NOTHING, db_column='application_number', primary_key=True)
    language_code = models.TextField(blank=True, null=True)
    mark_description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tm_mark_description'


class TmOppositionCase(models.Model):
    application_number = models.OneToOneField(TmMain, models.DO_NOTHING, db_column='application_number', primary_key=True)  # The composite primary key (application_number, opposition_case_number) found, that is not supported. The first column is selected.
    opposition_case_number = models.IntegerField()
    opposition_case_type_english_name = models.TextField(blank=True, null=True)
    opposition_case_type_french_name = models.TextField(blank=True, null=True)
    opposition_date = models.DateField(blank=True, null=True)
    wipo_opposition_case_status = models.TextField(blank=True, null=True)
    opposition_wipo_status_date = models.DateField(blank=True, null=True)
    wipo_opposition_status_category = models.SmallIntegerField(blank=True, null=True)
    opposition_case_status_code = models.SmallIntegerField(blank=True, null=True)
    cipo_opposition_status_date = models.DateField(blank=True, null=True)
    entity_name_of_the_opposition_proceeding_defendant = models.TextField(blank=True, null=True)
    defendant_language_code = models.TextField(blank=True, null=True)
    defendant_address_line_1 = models.TextField(blank=True, null=True)
    defendant_address_line_2 = models.TextField(blank=True, null=True)
    defendant_address_line_3 = models.TextField(blank=True, null=True)
    defendant_country_code = models.TextField(blank=True, null=True)
    contact_name_of_defendant = models.TextField(blank=True, null=True)
    contact_language_code_of_defendant = models.TextField(blank=True, null=True)
    contact_address_line_1_of_defendant = models.TextField(blank=True, null=True)
    contact_address_line_2_of_defendant = models.TextField(blank=True, null=True)
    contact_address_line_3_of_defendant = models.TextField(blank=True, null=True)
    contact_province_name_of_defendant = models.TextField(blank=True, null=True)
    contact_country_code_of_defendant = models.TextField(blank=True, null=True)
    contact_postal_code_of_defendant = models.TextField(blank=True, null=True)
    agent_name_of_defendant = models.TextField(blank=True, null=True)
    agent_language_code_of_defendant = models.TextField(blank=True, null=True)
    agent_address_line_1_of_defendant = models.TextField(blank=True, null=True)
    agent_address_line_2_of_defendant = models.TextField(blank=True, null=True)
    agent_address_line_3_of_defendant = models.TextField(blank=True, null=True)
    agent_province_name_of_defendant = models.TextField(blank=True, null=True)
    agent_country_code_of_defendant = models.TextField(blank=True, null=True)
    agent_postal_code_of_defendant = models.TextField(blank=True, null=True)
    plaintiff_name = models.TextField(blank=True, null=True)
    plaintiff_legal_name = models.TextField(blank=True, null=True)
    plaintiff_language_code = models.TextField(blank=True, null=True)
    plaintiff_address_line_1 = models.TextField(blank=True, null=True)
    plaintiff_address_line_2 = models.TextField(blank=True, null=True)
    plaintiff_address_line_3 = models.TextField(blank=True, null=True)
    plaintiff_country_code = models.TextField(blank=True, null=True)
    contact_name_of_plaintiff = models.TextField(blank=True, null=True)
    contact_language_code_of_plaintiff = models.TextField(blank=True, null=True)
    contact_address_line_1_of_plaintiff = models.TextField(blank=True, null=True)
    contact_address_line_2_of_plaintiff = models.TextField(blank=True, null=True)
    contact_address_line_3_of_plaintiff = models.TextField(blank=True, null=True)
    contact_province_name_of_plaintiff = models.TextField(blank=True, null=True)
    contact_country_code_of_plaintiff = models.TextField(blank=True, null=True)
    contact_postal_code_of_plaintiff = models.TextField(blank=True, null=True)
    agent_number_of_plaintiff = models.IntegerField(blank=True, null=True)
    agent_name_of_plaintiff = models.TextField(blank=True, null=True)
    agent_language_code_of_plaintiff = models.TextField(blank=True, null=True)
    agent_address_line_1_of_plaintiff = models.TextField(blank=True, null=True)
    agent_address_line_2_of_plaintiff = models.TextField(blank=True, null=True)
    agent_address_line_3_of_plaintiff = models.TextField(blank=True, null=True)
    agent_province_name_of_plaintiff = models.TextField(blank=True, null=True)
    agent_country_code_of_plaintiff = models.TextField(blank=True, null=True)
    agent_postal_code_of_plaintiff = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tm_opposition_case'
        unique_together = (('application_number', 'opposition_case_number'),)


class TmOppositionCaseAction(models.Model):
    opposition_case_action_id = models.AutoField(primary_key=True)
    application_number = models.ForeignKey(TmOppositionCase, models.DO_NOTHING, db_column='application_number')
    opposition_case_number = models.IntegerField()
    additional_comment = models.TextField(blank=True, null=True)
    proceeding_effective_date = models.DateField(blank=True, null=True)
    opposition_case_type_english_name = models.TextField(blank=True, null=True)
    opposition_case_type_french_name = models.TextField(blank=True, null=True)
    opposition_date = models.DateField(blank=True, null=True)
    wipo_opposition_case_status = models.TextField(blank=True, null=True)
    opposition_wipo_status_date = models.DateField(blank=True, null=True)
    wipo_opposition_status_category = models.SmallIntegerField(blank=True, null=True)
    opposition_case_status_code = models.SmallIntegerField(blank=True, null=True)
    cipo_opposition_status_date = models.DateField(blank=True, null=True)
    opposition_stage_code = models.IntegerField(blank=True, null=True)
    opposition_action_category = models.TextField(blank=True, null=True)
    opposition_action_code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tm_opposition_case_action'


class TmPriorityClaim(models.Model):
    application_number = models.ForeignKey(TmMain, models.DO_NOTHING, db_column='application_number')
    priority_application_number = models.TextField(blank=True, null=True)
    classification_sequence_number = models.TextField(blank=True, null=True)
    secondary_sequence_number = models.IntegerField(blank=True, null=True)
    priority_claim_text = models.TextField(blank=True, null=True)
    priority_country_code = models.TextField(blank=True, null=True)
    priority_filing_date = models.DateField(blank=True, null=True)
    classification_description = models.TextField(blank=True, null=True)
    nice_edition_number = models.SmallIntegerField(blank=True, null=True)
    nice_classification_code = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tm_priority_claim'


class TmRepresentation(models.Model):
    application_number = models.ForeignKey(TmMain, models.DO_NOTHING, db_column='application_number')
    representation_type_code = models.SmallIntegerField(blank=True, null=True)
    vienna_code = models.IntegerField(blank=True, null=True)
    vienna_division_number = models.IntegerField(blank=True, null=True)
    vienna_section_number = models.IntegerField(blank=True, null=True)
    image_colour_claimed_sequence_number = models.IntegerField(blank=True, null=True)
    vienna_description = models.TextField(blank=True, null=True)
    vienna_description_fr = models.TextField(blank=True, null=True)
    file_name = models.TextField(blank=True, null=True)
    file_format = models.TextField(blank=True, null=True)
    image_colour_claimed = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tm_representation'


class TmTransliteration(models.Model):
    application_number = models.OneToOneField(TmMain, models.DO_NOTHING, db_column='application_number', primary_key=True)
    mark_transliteration_text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tm_transliteration'
