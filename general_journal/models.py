from django.db import models
from django.contrib.auth.models import User
from import_export import resources, widgets
from import_export.fields import Field
# Create your models here.


class Journal(models.Model):
    id = models.BigAutoField(primary_key=True)
    sheet_no = models.TextField(blank=True, max_length=255, null=True)
    month = models.CharField(max_length=100, null=True, blank=True)
    year = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.TextField(blank=True, max_length=255, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'tbl_journal'


class GeneralJournal(models.Model):
    id = models.BigAutoField(primary_key=True)
    journal = models.ForeignKey(
        Journal, on_delete=models.CASCADE, null=True, blank=True)
    date = models.CharField(max_length=100, null=True, blank=True)
    jev_no = models.CharField(max_length=100, null=True, blank=True)
    particulars = models.TextField(max_length=100, null=True, blank=True)
    uacs_object_code = models.CharField(max_length=100, null=True, blank=True)
    p = models.BooleanField(default=False)
    amount_debit = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    amount_credit = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'tbl_general_journal'


class GeneralJournalResource(resources.ModelResource):
    journal = Field(
        column_name='journal_id',
        attribute='journal',
        widget=widgets.ForeignKeyWidget(Journal, 'id')
    )

    class Meta:
        model = GeneralJournal
        report_skipped = True
