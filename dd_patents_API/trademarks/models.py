from django.db import models

class TM_Main(models.Model):
    application_number = models.IntegerField(unique=True)
    filing_date = models.DateField(null=True, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    registration_date = models.DateField(null=True, blank=True)
    registration_office_country_code = models.CharField(max_length=2, null=True, blank=True)
    receiving_office_country_code = models.CharField(max_length=2, null=True, blank=True)
    receiving_office_date = models.DateField(null=True, blank=True)
    assigning_office_country_code = models.CharField(max_length=2, null=True, blank=True)
    registration_number = models.CharField(max_length=20, null=True, blank=True)
    legislation_code = models.IntegerField(null=True, blank=True)
    filing_place = models.CharField(max_length=50, null=True, blank=True)
    application_reference_number = models.CharField(max_length=50, null=True, blank=True)
    application_language_code = models.CharField(max_length=2, null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    termination_date = models.DateField(null=True, blank=True)
    wipo_status_code = models.IntegerField(null=True, blank=True)
    current_status_date = models.DateField(null=True, blank=True)
    association_category_id = models.CharField(max_length=50, blank=True, null=True)
    association_assigning_country_code = models.CharField(max_length=2, blank=True, null=True)
    associated_application_number = models.IntegerField(null=True, blank=True)
    mark_category = models.CharField(max_length=50, null=True, blank=True)
    divisional_application_country_code = models.CharField(max_length=2, null=True, blank=True)
    divisional_application_number = models.IntegerField(null=True, blank=True)
    divisional_application_date = models.DateField(null=True, blank=True)
    international_registration_number = models.IntegerField(null=True, blank=True)
    mark_type_code = models.IntegerField(null=True, blank=True)
    mark_verbal_element_description = models.TextField(null=True, blank=True)
    mark_significant_verbal_element_description = models.TextField(null=True, blank=True)
    mark_translation_description = models.TextField(null=True, blank=True)
    expungement_indicator = models.BooleanField(default=False)
    distinctiveness_indicator = models.BooleanField(default=False)
    distinctiveness_description = models.TextField(null=True, blank=True)
    evidence_of_use_indicator = models.BooleanField(default=False, null=True, blank=True)
    evidence_of_use_description = models.TextField(null=True, blank=True)
    restriction_of_use_description = models.TextField(null=True, blank=True)
    cipo_standard_message_description = models.TextField(null=True, blank=True)
    opposition_start_date = models.DateField(null=True, blank=True)
    opposition_end_date = models.DateField(null=True, blank=True)
    total_nice_classifications_number = models.IntegerField(null=True, blank=True)
    foreign_application_indicator = models.BooleanField(default=False)
    foreign_registration_indicator = models.BooleanField(default=False)
    used_in_canada_indicator = models.BooleanField(default=False)
    proposed_use_in_canada_indicator = models.BooleanField(default=False)
    classification_term_office_country_code = models.CharField(max_length=2, null=True, blank=True)
    classification_term_source_name = models.CharField(max_length=50, null=True, blank=True)
    classification_term_english_description = models.TextField(null=True, blank=True)
    publication_id = models.CharField(max_length=50, null=True, blank=True)
    publication_status = models.CharField(max_length=50, null=True, blank=True)
    authorization_of_use_date = models.DateField(null=True, blank=True)
    authorization_code = models.IntegerField(null=True, blank=True)
    authorization_description = models.TextField(null=True, blank=True)
    register_code = models.IntegerField(null=True, blank=True)
    application_abandoned_date = models.DateField(null=True, blank=True)
    cipo_status_code = models.IntegerField(null=True, blank=True)
    allowed_date = models.DateField(null=True, blank=True)
    renewal_date = models.DateField(null=True, blank=True)
    trademark_class_code = models.CharField(max_length=255, null=True, blank=True)
    geographical_indication_kind_category_code = models.IntegerField(null=True, blank=True)
    geographical_indication_translation_sequence_number = models.IntegerField(null=True, blank=True)
    geographical_indication_translation_text = models.TextField(null=True, blank=True)
    doubtful_case_application_number = models.IntegerField(null=True, blank=True)
    doubtful_case_registration_number = models.CharField(max_length=50, null=True, blank=True)
    legislation_description_code = models.CharField(max_length=255, null=True, blank=True)
    marktype_code = models.CharField(max_length=255, null=True, blank=True)
    mark_significant_description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return str(self.application_number)



class TM_Mark_Description(models.Model):
    application_number = models.IntegerField()
    language_code = models.CharField(max_length=2)
    mark_description = models.TextField()

    def __str__(self):
        return str(self.application_number)


class TM_CIPO_Classifications(models.Model):
    application_number = models.IntegerField()
    classification_kind_code = models.CharField(max_length=50)
    nice_classification_code = models.IntegerField()
    nice_classification = models.TextField()

    def __str__(self):
        return f"{self.application_number} - {self.classification_kind_code}"


class TM_Applicant_Classifications(models.Model):
    application_number = models.IntegerField()
    classification_sequence_number = models.CharField(max_length=50)
    classification_indicator_line_sequence_number = models.IntegerField()
    classification_indicator_description = models.TextField()
    nice_edition_number = models.IntegerField()
    nice_classification_code = models.IntegerField()
    nice_classification = models.TextField()

    def __str__(self):
        return f"{self.application_number} - {self.classification_sequence_number}"


class TM_Representation(models.Model):
    application_number = models.IntegerField()
    representation_type_code = models.IntegerField()
    vienna_code = models.IntegerField()
    vienna_division_number = models.IntegerField()
    vienna_section_number = models.IntegerField()
    vienna_description = models.TextField()
    vienna_description_fr = models.TextField()
    file_name = models.CharField(max_length=255)
    file_format = models.CharField(max_length=50)
    image_colour_claimed_sequence_number = models.IntegerField()
    image_colour_claimed = models.TextField()

    def __str__(self):
        return f"{self.application_number} - {self.representation_type_code}"


class TM_Interested_Party(models.Model):
    application_number = models.IntegerField()
    party_type_code = models.IntegerField()
    party_language_code = models.CharField(max_length=2)
    party_name = models.CharField(max_length=255)
    party_address_line1 = models.CharField(max_length=255)
    party_address_line2 = models.CharField(max_length=255, blank=True, null=True)
    party_address_line3 = models.CharField(max_length=255, blank=True, null=True)
    party_address_line4 = models.CharField(max_length=255, blank=True, null=True)
    party_address_line5 = models.CharField(max_length=255, blank=True, null=True)
    party_province_name = models.CharField(max_length=100, blank=True, null=True)
    party_country_code = models.CharField(max_length=2)
    party_postal_code = models.CharField(max_length=20, blank=True, null=True)
    contact_language_code = models.CharField(max_length=2)
    contact_name = models.CharField(max_length=255)
    contact_address_line1 = models.CharField(max_length=255)
    contact_address_line2 = models.CharField(max_length=255, blank=True, null=True)
    contact_address_line3 = models.CharField(max_length=255, blank=True, null=True)
    contact_province_name = models.CharField(max_length=100, blank=True, null=True)
    contact_country_code = models.CharField(max_length=2)
    contact_postal_code = models.CharField(max_length=20, blank=True, null=True)
    current_owner_legal_name = models.CharField(max_length=255)
    agent_number = models.IntegerField()

    def __str__(self):
        return f"{self.application_number} - {self.party_name}"


class TM_Claim(models.Model):
    application_number = models.IntegerField()
    claim_text = models.TextField()
    claim_type = models.IntegerField()
    claim_number = models.IntegerField()
    claim_code = models.IntegerField()
    structure_claim_date = models.DateField(null=True, blank=True)
    claim_year_number = models.IntegerField(null=True, blank=True)
    claim_month_number = models.IntegerField(null=True, blank=True)
    claim_day_number = models.IntegerField(null=True, blank=True)
    claim_country_code = models.CharField(max_length=2, null=True, blank=True)
    foreign_registration_number = models.CharField(max_length=50, null=True, blank=True)
    goods_services_reference_identifier = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.application_number} - {self.claim_number}"


class TM_Priority_Claim(models.Model):
    application_number = models.IntegerField()
    priority_claim_text = models.TextField()
    priority_country_code = models.CharField(max_length=2)
    priority_application_number = models.CharField(max_length=50)
    priority_filing_date = models.DateField()
    classification_sequence_number = models.CharField(max_length=50)
    classification_description = models.TextField()
    secondary_sequence_number = models.IntegerField()
    nice_edition_number = models.IntegerField()
    nice_classification_code = models.IntegerField()

    def __str__(self):
        return f"{self.application_number} - {self.priority_application_number}"


class TM_Event(models.Model):
    application_number = models.IntegerField()
    action_date = models.DateField(null=True, blank=True)
    response_date = models.DateField(null=True, blank=True)
    additional_information_comment = models.TextField(null=True, blank=True)
    wipo_action_type = models.TextField(null=True, blank=True)
    cipo_action_code = models.IntegerField()

    def __str__(self):
        return f"{self.application_number} - {self.cipo_action_code}"
    

class TM_Application_Disclaimer(models.Model):
    application_number = models.IntegerField()
    language_code = models.CharField(max_length=2)
    disclaimer_text_sequence_number = models.IntegerField()
    disclaimer_text = models.TextField()

    def __str__(self):
        return f"{self.application_number} - {self.disclaimer_text_sequence_number}"


class TM_Application_Text(models.Model):
    application_number = models.IntegerField()
    application_text_code = models.IntegerField()
    sequence_number = models.IntegerField()
    secondary_sequence_number = models.IntegerField(null=True, blank=True)
    application_text_changed_date = models.DateField()
    application_text_details = models.TextField()

    def __str__(self):
        return f"{self.application_number} - {self.sequence_number}"


class TM_Transliteration(models.Model):
    application_number = models.IntegerField()
    mark_transliteration_text = models.TextField()

    def __str__(self):
        return f"{self.application_number}"


class TM_Footnote(models.Model):
    application_number = models.IntegerField()
    footnote_text_line_sequence_number = models.IntegerField()
    footnote_text_line_description = models.TextField()
    footnote_number = models.IntegerField()
    footnote_category_code = models.IntegerField()
    footnote_change_date = models.DateField(null=True, blank=True)
    footnote_registration_date = models.DateField(null=True, blank=True)


    def __str__(self):
        return f"{self.application_number} - {self.footnote_number}"


class TM_Footnote_Formatted(models.Model):
    application_number = models.IntegerField()
    footnote_number = models.IntegerField()
    footnote_formatted_text_sequence_number = models.IntegerField()
    footnote_formatted_text = models.TextField()

    def __str__(self):
        return f"{self.application_number} - {self.footnote_number}"
    

class TM_Heading(models.Model):
    application_number = models.IntegerField()
    index_heading_number = models.IntegerField()
    index_heading_comment = models.TextField()

    def __str__(self):
        return f"{self.application_number} - {self.index_heading_number}"
    

class TM_Cancellation_Case(models.Model):
    application_number = models.IntegerField()
    section_44_45_case_number = models.IntegerField()
    legal_proceeding_type_description_english = models.TextField()
    legal_proceeding_type_description_french = models.TextField()
    section_44_45_filing_date = models.DateField()
    wipo_section_44_45_status_category_code = models.IntegerField()
    section_44_45_status_code = models.IntegerField()
    section_44_45_status_date = models.DateField()
    entity_name_of_defendant = models.TextField()
    defendant_language_code = models.CharField(max_length=2)
    defendant_address_line_1 = models.TextField()
    defendant_address_line_2 = models.TextField(null=True, blank=True)
    defendant_address_line_3 = models.TextField(null=True, blank=True)
    defendant_country_code = models.CharField(max_length=2)
    contact_name_of_defendant = models.TextField()
    contact_language_code_of_defendant = models.CharField(max_length=2)
    contact_address_line_1_of_defendant = models.TextField()
    contact_address_line_2_of_defendant = models.TextField(null=True, blank=True)
    contact_address_line_3_of_defendant = models.TextField(null=True, blank=True)
    contact_province_name_of_defendant = models.TextField()
    contact_country_code_of_defendant = models.CharField(max_length=2)
    contact_postal_code_of_defendant = models.TextField()
    agent_name_of_defendant = models.TextField()
    agent_language_code_of_defendant = models.CharField(max_length=2)
    agent_address_line_1_of_defendant = models.TextField()
    agent_address_line_2_of_defendant = models.TextField(null=True, blank=True)
    agent_address_line_3_of_defendant = models.TextField(null=True, blank=True)
    agent_province_name_of_defendant = models.TextField()
    agent_country_code_of_defendant = models.CharField(max_length=2)
    agent_postal_code_of_defendant = models.TextField()
    plaintiff_name = models.TextField()
    plaintiff_legal_name = models.TextField()
    plaintiff_language_code = models.CharField(max_length=2)
    plaintiff_address_line_1 = models.TextField()
    plaintiff_address_line_2 = models.TextField(null=True, blank=True)
    plaintiff_address_line_3 = models.TextField(null=True, blank=True)
    plaintiff_country_code = models.CharField(max_length=2)
    contact_name_of_plaintiff = models.TextField()
    contact_language_code_of_plaintiff = models.CharField(max_length=2)
    contact_address_line_1_of_plaintiff = models.TextField()
    contact_address_line_2_of_plaintiff = models.TextField(null=True, blank=True)
    contact_address_line_3_of_plaintiff = models.TextField(null=True, blank=True)
    contact_province_name_of_plaintiff = models.TextField()
    contact_country_code_of_plaintiff = models.CharField(max_length=2)
    contact_postal_code_of_plaintiff = models.TextField()
    agent_number_of_plaintiff = models.IntegerField()
    agent_name_of_plaintiff = models.TextField()
    agent_language_code_of_plaintiff = models.CharField(max_length=2)
    agent_address_line_1_of_plaintiff = models.TextField()
    agent_address_line_2_of_plaintiff = models.TextField(null=True, blank=True)
    agent_address_line_3_of_plaintiff = models.TextField(null=True, blank=True)
    agent_province_name_of_plaintiff = models.TextField()
    agent_country_code_of_plaintiff = models.CharField(max_length=2)
    agent_postal_code_of_plaintiff = models.TextField()

    def __str__(self):
        return f"{self.application_number} - {self.section_44_45_case_number}"


class TM_Cancellation_Case_Action(models.Model):
    application_number = models.IntegerField()
    additional_comment = models.TextField(null=True, blank=True)
    proceeding_effective_date = models.DateField()
    section_44_45_case_number = models.IntegerField()
    legal_proceeding_type_description_english = models.TextField()
    legal_proceeding_type_description_french = models.TextField()
    section_44_45_filing_date = models.DateField()
    wipo_section_44_45_status_category_code = models.IntegerField()
    section_44_45_status_code = models.IntegerField()
    section_44_45_status_date = models.DateField()
    section_44_45_stage_code = models.IntegerField()
    section_44_45_case_status = models.TextField()
    section_44_45_actions_code = models.IntegerField()

    def __str__(self):
        return f"{self.application_number} - {self.section_44_45_case_number}"

class TM_Opposition_Case(models.Model):
    application_number = models.IntegerField()
    opposition_case_number = models.IntegerField()
    opposition_case_type_english_name = models.TextField()
    opposition_case_type_french_name = models.TextField()
    opposition_date = models.DateField()
    wipo_opposition_case_status = models.TextField()
    opposition_wipo_status_date = models.DateField()
    wipo_opposition_status_category = models.IntegerField()
    opposition_case_status_code = models.IntegerField()
    cipo_opposition_status_date = models.DateField()
    entity_name_of_defendant = models.TextField()
    defendant_language_code = models.CharField(max_length=2)
    defendant_address_line_1 = models.TextField()
    defendant_address_line_2 = models.TextField(null=True, blank=True)
    defendant_address_line_3 = models.TextField(null=True, blank=True)
    defendant_country_code = models.CharField(max_length=2)
    contact_name_of_defendant = models.TextField()
    contact_language_code_of_defendant = models.CharField(max_length=2)
    contact_address_line_1_of_defendant = models.TextField()
    contact_address_line_2_of_defendant = models.TextField(null=True, blank=True)
    contact_address_line_3_of_defendant = models.TextField(null=True, blank=True)
    contact_province_name_of_defendant = models.TextField()
    contact_country_code_of_defendant = models.CharField(max_length=2)
    contact_postal_code_of_defendant = models.TextField()
    agent_name_of_defendant = models.TextField()
    agent_language_code_of_defendant = models.CharField(max_length=2)
    agent_address_line_1_of_defendant = models.TextField()
    agent_address_line_2_of_defendant = models.TextField(null=True, blank=True)
    agent_address_line_3_of_defendant = models.TextField(null=True, blank=True)
    agent_province_name_of_defendant = models.TextField()
    agent_country_code_of_defendant = models.CharField(max_length=2)
    agent_postal_code_of_defendant = models.TextField()
    plaintiff_name = models.TextField()
    plaintiff_legal_name = models.TextField()
    plaintiff_language_code = models.CharField(max_length=2)
    plaintiff_address_line_1 = models.TextField()
    plaintiff_address_line_2 = models.TextField(null=True, blank=True)
    plaintiff_address_line_3 = models.TextField(null=True, blank=True)
    plaintiff_country_code = models.CharField(max_length=2)
    contact_name_of_plaintiff = models.TextField()
    contact_language_code_of_plaintiff = models.CharField(max_length=2)
    contact_address_line_1_of_plaintiff = models.TextField()
    contact_address_line_2_of_plaintiff = models.TextField(null=True, blank=True)
    contact_address_line_3_of_plaintiff = models.TextField(null=True, blank=True)
    contact_province_name_of_plaintiff = models.TextField()
    contact_country_code_of_plaintiff = models.CharField(max_length=2)
    contact_postal_code_of_plaintiff = models.TextField()
    agent_number_of_plaintiff = models.IntegerField()
    agent_name_of_plaintiff = models.TextField()
    agent_language_code_of_plaintiff = models.CharField(max_length=2)
    agent_address_line_1_of_plaintiff = models.TextField()
    agent_address_line_2_of_plaintiff = models.TextField(null=True, blank=True)
    agent_address_line_3_of_plaintiff = models.TextField(null=True, blank=True)
    agent_province_name_of_plaintiff = models.TextField()
    agent_country_code_of_plaintiff = models.CharField(max_length=2)
    agent_postal_code_of_plaintiff = models.TextField()

    def __str__(self):
        return f"{self.application_number} - {self.opposition_case_number}"


class TM_Opposition_Case_Action(models.Model):
    application_number = models.IntegerField()
    additional_comment = models.TextField(null=True, blank=True)
    proceeding_effective_date = models.DateField()
    opposition_case_number = models.IntegerField()
    opposition_case_type_english_name = models.TextField()
    opposition_case_type_french_name = models.TextField()
    opposition_date = models.DateField()
    wipo_opposition_case_status = models.TextField()
    opposition_wipo_status_date = models.DateField()
    wipo_opposition_status_category = models.IntegerField()
    opposition_case_status_code = models.IntegerField()
    cipo_opposition_status_date = models.DateField()
    opposition_stage_code = models.IntegerField()
    opposition_action_category = models.TextField()
    opposition_action_code = models.IntegerField()

    def __str__(self):
        return f"{self.application_number} - {self.opposition_case_number}"


