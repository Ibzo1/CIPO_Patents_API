from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'main', ApplicationMainViewSet, basename='id_main')
router.register(r'application_classification', ApplicationClassificationViewSet, basename='id_classification')
router.register(r'application_correction', ApplicationCorrectionViewSet, basename='id_correction')
router.register(r'application_description', ApplicationDescriptionViewSet, basename='id_description')
router.register(r'application_description_txt_format', ApplicationDescriptionTxtFormatViewSet, basename='id_description_txt_format')
router.register(r'application_image', ApplicationImageViewSet, basename='id_image')
router.register(r'application_interested_party', ApplicationInterestedPartyViewSet, basename='id_interested_party')
router.register(r'assignment_correction', AssignmentCorrectionViewSet, basename='id_assignment_correction')
router.register(r'assignment_interested_party', AssignmentInterestedPartyViewSet, basename='id_assignment_interested_party')
router.register(r'assignment_main', AssignmentMainViewSet, basename='id_assignment_main')

urlpatterns = router.urls