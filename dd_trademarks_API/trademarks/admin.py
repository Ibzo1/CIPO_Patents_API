from django.contrib import admin


from .models import (
    TmMain,
    TmMarkDescription,
    TmCipoClassifications,
    TmApplicantClassifications,
    TmRepresentation,
    TmInterestedParty,
    TmClaim,
    TmPriorityClaim,
    TmEvent,
    TmApplicationDisclaimer,
    TmApplicationText,
    TmTransliteration,
    TmFootnote,
    TmFootnoteFormatted,
    TmHeading,
    TmCancellationCase,
    TmCancellationCaseAction,
    TmOppositionCase,
    TmOppositionCaseAction
)

admin.site.register(TmMain)
admin.site.register(TmMarkDescription)
admin.site.register(TmCipoClassifications)
admin.site.register(TmApplicantClassifications)
admin.site.register(TmRepresentation)
admin.site.register(TmInterestedParty)
admin.site.register(TmClaim)
admin.site.register(TmPriorityClaim)
admin.site.register(TmEvent)
admin.site.register(TmApplicationDisclaimer)
admin.site.register(TmApplicationText)
admin.site.register(TmTransliteration)
admin.site.register(TmFootnote)
admin.site.register(TmFootnoteFormatted)
admin.site.register(TmHeading)
admin.site.register(TmCancellationCase)
admin.site.register(TmCancellationCaseAction)
admin.site.register(TmOppositionCase)
admin.site.register(TmOppositionCaseAction)

