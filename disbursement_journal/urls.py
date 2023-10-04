from django.urls import path, include
from disbursement_journal.views import ImportDisbursementJournalData

urlpatterns = [
    path('import', ImportDisbursementJournalData.as_view()),

]
