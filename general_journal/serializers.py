from rest_framework import serializers
from general_journal.models import GeneralJournal, Journal


class GeneralJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralJournal
        fields = '__all__'


class JournalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Journal
        fields = '__all__'
