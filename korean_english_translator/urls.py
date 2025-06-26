from django.urls import path
from .views import TranslateAPIView, PhraseLookupAPIView

urlpatterns = [
    path('api/v0/translate/', TranslateAPIView.as_view(), name='translate'),
    path('api/v0/phrase-lookup/', PhraseLookupAPIView.as_view(), name='phrase-lookup'),
]
