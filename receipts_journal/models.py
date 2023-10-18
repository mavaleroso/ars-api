from django.db import models
from django.contrib.auth.models import User
from import_export import resources, widgets
from import_export.fields import Field

# Create your models here.


class CRJ(models.Model):
    id = models.BigAutoField(primary_key=True)
    sheet_no = models.CharField(max_length=100, blank=True, null=True)
    month = models.CharField(max_length=100, blank=True, null=True)
    year = models.CharField(max_length=100, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'tbl_crj'


class ReceiptsJournal(models.Model):
    id = models.BigAutoField(primary_key=True)
    crj = models.ForeignKey(
        CRJ, on_delete=models.CASCADE, null=True, blank=True)
    rcd = models.CharField(max_length=100, blank=True, null=True)
    jev_no = models.CharField(max_length=100, blank=True, null=True)
    name_of_collecting_officer = models.CharField(max_length=255, blank=True, null=True)
    col_debit_amount = models.DecimalField(max_digits=65, decimal_places=2, null=True, blank=True)
    col_debit_uacs_object_code = models.CharField(max_length=255, blank=True, null=True)
    col_credit_or_no = models.CharField(max_length=255, blank=True, null=True)
    col_credit_transaction = models.CharField(max_length=255, blank=True, null=True)
    col_credit_payor = models.CharField(max_length=255, blank=True, null=True)
    col_credit_uacs_name = models.CharField(max_length=255, blank=True, null=True)
    col_credit_sundry_uacs_object_code = models.CharField(max_length=255, blank=True, null=True)
    col_credit_sundry_p = models.CharField(max_length=100, blank=True, null=True)
    col_credit_sundry_amount = models.DecimalField(max_digits=65, decimal_places=2, blank=True, null=True)
    dep_debit_deposited_account = models.CharField(max_length=255, blank=True, null=True)
    dep_date_of_deposit = models.CharField(max_length=255, blank=True, null=True)
    dep_debit_sundry_uacs_object_code = models.CharField(max_length=255, blank=True, null=True)
    dep_debit_sundry_p = models.CharField(max_length=100, blank=True, null=True)
    dep_debit_sundry_amount = models.DecimalField(max_digits=65, decimal_places=2, blank=True, null=True)
    dep_credit_uacs_object_code = models.CharField(max_length=255, blank=True, null=True)
    dep_credit_amount = models.DecimalField(max_digits=65, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'tbl_receipts_journal'


class ReceiptsJournalResource(resources.ModelResource):
    crj = Field(
        column_name='crj_id',
        attribute='crj',
        widget=widgets.ForeignKeyWidget(CRJ, 'id')
    )

    class Meta:
        model = ReceiptsJournal
        # skip_unchanged = True
        # report_skipped = True
        skip_rows = 3
        # import_id_fields = ['rcd', 'jev_no']