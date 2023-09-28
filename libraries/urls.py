from django.urls import path, include
from libraries.views import ImportAccountsData, FetchAccounts, FetchAccount, CreateAccounts, DeleteAccounts

urlpatterns = [
    path('accounts/import', ImportAccountsData.as_view()),
    path('accounts/fetch', FetchAccounts),
    path('accounts/fetch/<int:pk>', FetchAccount),
    path('accounts/create', CreateAccounts),
    path('accounts/delete/<int:pk>', DeleteAccounts),
]
