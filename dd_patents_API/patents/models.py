from django.db import models


class PT_Interested_Party(models.Model):
    patent_number = models.ForeignKey('PT_Main', on_delete=models.CASCADE, related_name='interested_parties')
    agent_type_code = models.CharField(max_length=50)
    applicant_type_code = models.CharField(max_length=50)
    interested_party_type_code = models.CharField(max_length=10)
    interested_party_type = models.CharField(max_length=50)
    owner_enable_date = models.DateField(null=True, blank=True)  
    ownership_end_date = models.DateField(null=True, blank=True)
    party_name = models.CharField(max_length=255)
    party_address_line_1 = models.CharField(max_length=255)
    party_address_line_2 = models.CharField(max_length=255, blank=True)
    party_address_line_3 = models.CharField(max_length=255, blank=True)
    party_address_line_4 = models.CharField(max_length=255, blank=True)
    party_address_line_5 = models.CharField(max_length=255, blank=True)
    party_city = models.CharField(max_length=100)
    party_province_code = models.CharField(max_length=10, blank=True)
    party_province = models.CharField(max_length=100, blank=True)
    party_postal_code = models.CharField(max_length=20, blank=True)
    party_country_code = models.CharField(max_length=2)
    party_country = models.CharField(max_length=100)

    class Meta:
        db_table = 'pt_interested_party'
        unique_together = ('patent_number', 'party_name', 'owner_enable_date')

    def __str__(self):
        return f"{self.patent_number.patent_number} - {self.party_name}"



class PT_Abstract(models.Model):
    patent_number = models.ForeignKey('PT_Main', on_delete=models.CASCADE, related_name='abstracts')
    language_of_filing_code = models.CharField(max_length=2)
    abstract_language_code = models.CharField(max_length=2)
    abstract_text = models.TextField()
    abstract_text_sequence_number = models.IntegerField()

    class Meta:
        unique_together = ('patent_number', 'abstract_text_sequence_number')

    def __str__(self):
        return f"{self.patent_number.patent_number} - {self.abstract_text_sequence_number}"

class PT_Disclosure(models.Model):
    patent_number = models.ForeignKey('PT_Main', on_delete=models.CASCADE, related_name='disclosures')
    language_of_filing_code = models.CharField(max_length=2)
    disclosure_text = models.TextField()
    disclosure_text_sequence_number = models.IntegerField()

    class Meta:
        unique_together = ('patent_number', 'disclosure_text_sequence_number')

    def __str__(self):
        return f"{self.patent_number.patent_number} - {self.disclosure_text_sequence_number}"

class PT_Claim(models.Model):
    patent_number = models.ForeignKey('PT_Main', on_delete=models.CASCADE, related_name='claims')
    language_of_filing_code = models.CharField(max_length=2)
    claims_text = models.TextField()
    claim_text_sequence_number = models.IntegerField()

    class Meta:
        unique_together = ('patent_number', 'claim_text_sequence_number')

    def __str__(self):
        return f"{self.patent_number.patent_number} - {self.claim_text_sequence_number}"

class PT_IPC_Classification(models.Model):
    patent_number = models.ForeignKey('PT_Main', on_delete=models.CASCADE, related_name='ipc_classifications')
    ipc_classification_sequence_number = models.IntegerField()
    ipc_version_date = models.DateField()
    classification_level = models.CharField(max_length=1)
    classification_status_code = models.CharField(max_length=1)
    classification_status = models.CharField(max_length=1)
    ipc_section_code = models.CharField(max_length=1)
    ipc_section = models.CharField(max_length=350)  # Adjusted
    ipc_class_code = models.CharField(max_length=10)
    ipc_class = models.CharField(max_length=500)  # Adjusted
    ipc_subclass_code = models.CharField(max_length=10)
    ipc_subclass = models.CharField(max_length=500)  # Adjusted
    ipc_main_group_code = models.CharField(max_length=10)
    ipc_group = models.CharField(max_length=500)  # Adjusted
    ipc_subgroup_code = models.CharField(max_length=10)
    ipc_subgroup = models.CharField(max_length=500)  # Adjusted

    class Meta:
        db_table = 'pt_ipc_classification'
        unique_together = ('patent_number', 'ipc_classification_sequence_number')

    def __str__(self):
        return f"{self.patent_number.patent_number} - {self.ipc_classification_sequence_number}"

class PT_Main(models.Model):
    
    patent_number = models.CharField(max_length=50, primary_key=True, db_index=True)
    filing_date = models.DateField(null=True, blank=True)
    grant_date = models.DateField(null=True, blank=True)
    application_status_code = models.CharField(max_length=10, null=True, blank=True)
    application_type_code = models.CharField(max_length=20, null=True, blank=True)
    application_patent_title_french = models.CharField(max_length=500, null=True, blank=True)
    application_patent_title_english = models.CharField(max_length=500, null=True, blank=True)
    bibliographic_file_extract_date = models.DateField(null=True, blank=True)
    country_of_publication_code = models.CharField(max_length=10, null=True, blank=True)
    document_kind_type = models.CharField(max_length=10, null=True, blank=True)
    examination_request_date = models.DateField(null=True, blank=True)
    filing_country_code = models.CharField(max_length=10, null=True, blank=True)
    language_of_filing_code = models.CharField(max_length=10, null=True, blank=True)
    license_for_sale_indicator = models.BooleanField(default=False)
    pct_application_number = models.CharField(max_length=50, null=True, blank=True)
    pct_publication_number = models.CharField(max_length=50, null=True, blank=True)
    pct_publication_date = models.DateField(null=True, blank=True)
    parent_application_number = models.CharField(max_length=50, null=True, blank=True)
    pct_article_22_39_fulfilled_date = models.DateField(null=True, blank=True)
    pct_section_371_date = models.DateField(null=True, blank=True)
    pct_publication_country_code = models.CharField(max_length=10, null=True, blank=True)
    publication_kind_type = models.CharField(max_length=10, null=True, blank=True)
    printed_as_amended_country_code = models.CharField(max_length=10, null=True, blank=True)
    
    

class PT_Priority_Claim(models.Model):
    patent_number = models.ForeignKey(PT_Main, on_delete=models.CASCADE, related_name='priority_claims')
    foreign_application_patent_number = models.CharField(max_length=50)
    priority_claim_kind_code = models.CharField(max_length=15)
    priority_claim_country_code = models.CharField(max_length=2)
    priority_claim_country = models.CharField(max_length=100)
    priority_claim_calendar_dt = models.DateField()

    class Meta:
        unique_together = ('patent_number', 'foreign_application_patent_number')

    def __str__(self):
        return f"{self.patent_number} - {self.foreign_application_patent_number}"

