# Generated by Django 4.2.4 on 2023-10-17 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receipts_journal', '0003_alter_receiptsjournal_dep_date_of_deposit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receiptsjournal',
            name='col_credit_or_no',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]