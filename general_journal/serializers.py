from rest_framework import serializers
from django.contrib.auth.models import User
from general_journal.models import GeneralJournal, Journal
from django.db.models import Sum, DecimalField, ExpressionWrapper


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class GeneralJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralJournal
        fields = '__all__'


class JournalSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    debit = serializers.DecimalField(
        max_digits=15, decimal_places=2, read_only=True)
    credit = serializers.DecimalField(
        max_digits=15, decimal_places=2, read_only=True)

    class Meta:
        model = Journal
        fields = '__all__'
