from rest_framework import serializers
from receipts_journal.models import ReceiptsJournal, CRJ


class ReceiptsJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptsJournal
        fields = '__all__'


class CRJSerializer(serializers.ModelSerializer):

    class Meta:
        model = CRJ
        fields = '__all__'
