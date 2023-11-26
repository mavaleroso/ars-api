from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from general_journal.models import GeneralJournalResource, GeneralJournal, Journal
from general_journal.serializers import GeneralJournalSerializer, JournalSerializer
from rest_framework.decorators import api_view
from rest_framework import generics, parsers, status
from rest_framework.response import Response
import pandas as pd
from tablib import Dataset

# Create your views here.


class ImportGeneralJournalData(generics.GenericAPIView):
    parser_classes = [parsers.MultiPartParser]

    def post(self, request, *args, **kwargs):
        sheet_no = request.POST.get('sheet')
        month = request.POST.get('month')
        year = request.POST.get('year')
        remarks = request.POST.get('remarks')
        user_id = request.user.id

        journal_query = Journal(sheet_no=sheet_no, month=month,
                                remarks=remarks, year=year, author_id=user_id)

        journal_query.save()

        file = request.FILES['attachment']
        df = pd.read_excel(file, keep_default_na=False, skiprows=3)

        rename_columns = {
            df.columns[0]: 'rcd',
            df.columns[1]: 'jev_no',
            df.columns[2]: 'name_of_collecting_officer',
            df.columns[3]: 'col_debit_amount',
            df.columns[4]: 'col_debit_uacs_object_code',
            df.columns[5]: 'col_credit_or_no',
            df.columns[6]: 'col_credit_transaction',
            df.columns[7]: 'col_credit_payor',
            df.columns[8]: 'col_credit_uacs_name',
            df.columns[9]: 'col_credit_sundry_uacs_object_code',
            df.columns[10]: 'col_credit_sundry_p',
            df.columns[11]: 'col_credit_sundry_amount',
            df.columns[12]: 'dep_debit_deposited_account',
            df.columns[13]: 'dep_date_of_deposit',
            df.columns[14]: 'dep_debit_sundry_uacs_object_code',
            df.columns[15]: 'dep_debit_sundry_p',
            df.columns[16]: 'dep_debit_sundry_amount',
            df.columns[17]: 'dep_credit_uacs_object_code',
            df.columns[18]: 'dep_credit_amount'
        }

        df['journal_id'] = journal_query.id

        df.rename(columns=rename_columns, inplace=True)

        # Call the Student Resource Model and make its instance
        receipts_journal_resource = GeneralJournalResource()

        # Load the pandas dataframe into a tablib dataset
        dataset = Dataset().load(df)

        # Call the import_data hook and pass the tablib dataset
        result = receipts_journal_resource.import_data(
            dataset, dry_run=True, raise_errors=True)
        # print(dataset)
        if not result.has_errors():
            result = receipts_journal_resource.import_data(
                dataset, dry_run=False)
            return Response({"status": "General Journal Data Imported Successfully"})

        return Response({"status": "Failed to import General Journal Data! Please contact your the developer"}, status=status.HTTP_400_BAD_REQUEST)
