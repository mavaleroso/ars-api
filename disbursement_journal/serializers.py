from rest_framework import serializers
from disbursement_journal.models import DisbursementJournal, CDJ


class DisbursementJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisbursementJournal
        fields = '__all__'


class CDJSerializer(serializers.ModelSerializer):

    class Meta:
        model = CDJ
        fields = '__all__'
