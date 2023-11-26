from django.urls import path
from general_journal.views import ImportGeneralJournalData

urlpatterns = [
    path('import', ImportGeneralJournalData.as_view()),
]
