from django.urls import path
from general_journal.views import ImportGeneralJournalData, FetchGJ, DeleteGJ, Fetch, UpdateJournal

urlpatterns = [
    path('import', ImportGeneralJournalData.as_view()),
    path('gj/fetch', FetchGJ),
    path('fetch/<int:pk>', Fetch),
    path('delete/<int:pk>', DeleteGJ),
    path('journal/update/<int:pk>', UpdateJournal),
]
