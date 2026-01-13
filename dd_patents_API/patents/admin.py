
from django.contrib import admin
from .models import PT_Main, PT_Priority_Claim, PT_Interested_Party, PT_Abstract, PT_Disclosure, PT_Claim, PT_IPC_Classification

class PTMainAdmin(admin.ModelAdmin):
    list_display = ('patent_number', 'filing_date', 'grant_date', 'application_patent_title_english')
    search_fields = ('patent_number', 'application_patent_title_english')

class PTPriorityClaimAdmin(admin.ModelAdmin):
    list_display = ('patent_number', 'foreign_application_patent_number', 'priority_claim_kind_code')
    search_fields = ('patent_number__patent_number', 'foreign_application_patent_number')

class PTInterestedPartyAdmin(admin.ModelAdmin):
    list_display = ('patent_number', 'party_name', 'interested_party_type')
    search_fields = ('patent_number__patent_number', 'party_name')

class PTAbstractAdmin(admin.ModelAdmin):
    list_display = ('patent_number', 'abstract_text_sequence_number', 'abstract_text')
    search_fields = ('patent_number__patent_number', 'abstract_text')

class PTDisclosureAdmin(admin.ModelAdmin):
    list_display = ('patent_number', 'disclosure_text_sequence_number', 'disclosure_text')
    search_fields = ('patent_number__patent_number', 'disclosure_text')

class PTClaimAdmin(admin.ModelAdmin):
    list_display = ('patent_number', 'claim_text_sequence_number', 'claims_text')
    search_fields = ('patent_number__patent_number', 'claims_text')

class PTIPCClassificationAdmin(admin.ModelAdmin):
    list_display = ('patent_number', 'ipc_classification_sequence_number', 'ipc_section_code')
    search_fields = ('patent_number__patent_number', 'ipc_section_code')

admin.site.register(PT_Main, PTMainAdmin)
admin.site.register(PT_Priority_Claim, PTPriorityClaimAdmin)
admin.site.register(PT_Interested_Party, PTInterestedPartyAdmin)
admin.site.register(PT_Abstract, PTAbstractAdmin)
admin.site.register(PT_Disclosure, PTDisclosureAdmin)
admin.site.register(PT_Claim, PTClaimAdmin)
admin.site.register(PT_IPC_Classification, PTIPCClassificationAdmin)
