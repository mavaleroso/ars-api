from django.db import models
from django.contrib.auth.models import User
from import_export import resources, widgets
from import_export.fields import Field
# Create your models here.


class CDJ(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.TextField(blank=True, max_length=255, null=True)
    month = models.CharField(max_length=100, null=True, blank=True)
    year = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.TextField(blank=True, max_length=255, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'tbl_cdj'


class DisbursementJournal(models.Model):
    id = models.BigAutoField(primary_key=True)
    cdj = models.ForeignKey(
        CDJ, on_delete=models.CASCADE, null=True, blank=True)
    recon_no = models.IntegerField(null=True, blank=True)
    seq = models.IntegerField(null=True, blank=True)
    month = models.CharField(max_length=100, null=True, blank=True)
    date = models.CharField(max_length=100, null=True, blank=True)
    year = models.CharField(max_length=100, null=True, blank=True)
    check_no = models.CharField(max_length=100, null=True, blank=True)
    dv_year = models.CharField(max_length=100, null=True, blank=True)
    dv_month = models.CharField(max_length=100, null=True, blank=True)
    dv_no = models.CharField(max_length=100, null=True, blank=True)
    source = models.CharField(max_length=100, null=True, blank=True)
    payee = models.TextField(max_length=100, null=True, blank=True)
    nature_of_payment = models.TextField(max_length=100, null=True, blank=True)
    check_tmp = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    cash = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    tax = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    tax_percent = models.CharField(max_length=100, null=True, blank=True)
    tax2 = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    tax2_percent = models.CharField(max_length=100, null=True, blank=True)
    remittance = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    rod = models.CharField(max_length=100, null=True, blank=True)
    cash_position = models.CharField(max_length=255, null=True, blank=True)
    ppa = models.CharField(max_length=100, null=True, blank=True)
    charge_center = models.CharField(max_length=100, null=True, blank=True)
    set = models.CharField(max_length=100, null=True, blank=True)
    purpose = models.CharField(max_length=100, null=True, blank=True)
    fund = models.CharField(max_length=100, null=True, blank=True)
    account_code = models.CharField(max_length=100, null=True, blank=True)
    old_code = models.CharField(max_length=100, null=True, blank=True)
    alobs_year = models.CharField(max_length=100, null=True, blank=True)
    alobs_month = models.CharField(max_length=100, null=True, blank=True)
    alobs_no = models.CharField(max_length=100, null=True, blank=True)
    sa_aamt = models.CharField(max_length=100, null=True, blank=True)
    earmark = models.CharField(max_length=100, null=True, blank=True)
    debit = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    credit = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    ap_charge_from = models.CharField(max_length=100, null=True, blank=True)
    old_code2 = models.CharField(max_length=100, null=True, blank=True)
    payment_remarks = models.TextField(max_length=100, blank=True, null=True)
    budget_code = models.CharField(max_length=100, null=True, blank=True)
    expense_class = models.CharField(max_length=100, null=True, blank=True)
    authorization = models.CharField(max_length=255, null=True, blank=True)
    bur_ap = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    quarter = models.CharField(max_length=255, null=True, blank=True)
    saa_no = models.CharField(max_length=100, null=True, blank=True)
    rao_ref = models.CharField(max_length=100, null=True, blank=True)
    uacs_description = models.CharField(max_length=255, null=True, blank=True)
    cmf_dr = models.CharField(max_length=100, null=True, blank=True)
    bur = models.CharField(max_length=100, null=True, blank=True)
    aa = models.CharField(max_length=100, null=True, blank=True)
    dd_nyd = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'tbl_disbursement_journal'


class DisbursementJournalResource(resources.ModelResource):
    cdj = Field(
        column_name='cdj_id',
        attribute='cdj',
        widget=widgets.ForeignKeyWidget(CDJ, 'id')
    )

    class Meta:
        model = DisbursementJournal
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ['recon_no', 'check_no']
