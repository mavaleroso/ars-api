from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from disbursement_journal.models import DisbursementJournal, CDJ
from disbursement_journal.models import DisbursementJournalResource

# Register your models here.


@admin.register(DisbursementJournal)
class DisbursementJournalAdmin(ImportExportModelAdmin):
    resource_class = DisbursementJournalResource
