from django.db import models
from import_export import resources
# Create your models here.

class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        return super(SoftDeletionManager, self).get_queryset().filter(deleted=False)

class Accounts(models.Model):
    id = models.BigAutoField(primary_key=True)
    uacs_object_code = models.CharField(
        max_length=100, blank=False, null=False, default=0)
    account_title = models.TextField(
        blank=False, null=False, max_length=255, default='none')
    rca_code = models.CharField(
        max_length=100, blank=False, null=False, default=0)
    uacs_subobject_code = models.CharField(
        max_length=100, blank=True, null=True)
    status = models.SmallIntegerField(default=1, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted = models.BooleanField(default=False)

    # Use the custom manager
    objects = SoftDeletionManager()

    def delete(self, *args, **kwargs):
        self.deleted_at = True
        self.save()

    def undelete(self):
        self.deleted_at = False
        self.save()
    class Meta:
        managed = True
        db_table = 'lib_accounts'


class AccountsResource(resources.ModelResource):

    class Meta:
        model = Accounts
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ['uacs_object_code']
