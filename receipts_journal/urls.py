from django.urls import path
from receipts_journal.views import ImportReceiptsJournalData, FetchCRJ, Fetch, DeleteCRJ

urlpatterns = [
    path('import', ImportReceiptsJournalData.as_view()),
    path('crj/fetch', FetchCRJ),
    path('fetch/<int:pk>', Fetch),
    path('delete/<int:pk>', DeleteCRJ)
]
