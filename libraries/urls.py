from django.urls import path, include
from libraries.views import ImportAccountsData, FetchAccounts, CreateAccounts

urlpatterns = [
    path('accounts/import', ImportAccountsData.as_view()),
    path('accounts/fetch', FetchAccounts),
    path('accounts/create', CreateAccounts),
]
