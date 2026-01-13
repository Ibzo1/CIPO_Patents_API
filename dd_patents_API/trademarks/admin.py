from django.contrib import admin


from .models import (
    TM_Main,
    TM_Mark_Description,
    TM_CIPO_Classifications,
    TM_Applicant_Classifications,
    TM_Representation,
    TM_Interested_Party,
    TM_Claim,
    TM_Priority_Claim,
    TM_Event,
    TM_Application_Disclaimer,
    TM_Application_Text,
    TM_Transliteration,
    TM_Footnote,
    TM_Footnote_Formatted,
    TM_Heading,
    TM_Cancellation_Case,
    TM_Cancellation_Case_Action,
    TM_Opposition_Case,
    TM_Opposition_Case_Action
)

admin.site.register(TM_Main)
admin.site.register(TM_Mark_Description)
admin.site.register(TM_CIPO_Classifications)
admin.site.register(TM_Applicant_Classifications)
admin.site.register(TM_Representation)
admin.site.register(TM_Interested_Party)
admin.site.register(TM_Claim)
admin.site.register(TM_Priority_Claim)
admin.site.register(TM_Event)
admin.site.register(TM_Application_Disclaimer)
admin.site.register(TM_Application_Text)
admin.site.register(TM_Transliteration)
admin.site.register(TM_Footnote)
admin.site.register(TM_Footnote_Formatted)
admin.site.register(TM_Heading)
admin.site.register(TM_Cancellation_Case)
admin.site.register(TM_Cancellation_Case_Action)
admin.site.register(TM_Opposition_Case)
admin.site.register(TM_Opposition_Case_Action)

