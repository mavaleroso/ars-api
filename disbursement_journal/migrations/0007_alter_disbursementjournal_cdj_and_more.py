# Generated by Django 4.2.4 on 2023-10-05 07:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('disbursement_journal', '0006_remove_disbursementjournal_cdj_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disbursementjournal',
            name='cdj',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='disbursement_journal.cdj'),
        ),
        migrations.AlterField(
            model_name='disbursementjournal',
            name='check_tmp',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]
