# Generated by Django 4.2.4 on 2023-10-03 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('disbursement_journal', '0004_cdj_disbursementjournal_cdj_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='disbursementjournal',
            name='tax_total',
        ),
    ]
