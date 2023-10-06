from django.urls import path, include
from disbursement_journal.views import ImportDisbursementJournalData, FetchCDJ, Fetch, DeleteCDJ

urlpatterns = [
    path('import', ImportDisbursementJournalData.as_view()),
    path('cdj/fetch', FetchCDJ),
    path('fetch/<int:pk>', Fetch),
    path('delete/<int:pk>', DeleteCDJ)
]
