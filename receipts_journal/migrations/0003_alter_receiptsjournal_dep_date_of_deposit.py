# Generated by Django 4.2.4 on 2023-10-17 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receipts_journal', '0002_alter_receiptsjournal_crj'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receiptsjournal',
            name='dep_date_of_deposit',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
