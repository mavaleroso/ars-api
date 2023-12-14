from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum,  DecimalField, IntegerField, F, ExpressionWrapper
from django.db.models.functions import Coalesce
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
        df = pd.read_excel(file, keep_default_na=False, skiprows=2)

        rename_columns = {
            df.columns[0]: 'date',
            df.columns[1]: 'jev_no',
            df.columns[2]: 'particulars',
            df.columns[3]: 'uacs_object_code',
            df.columns[4]: 'p',
            df.columns[5]: 'amount_debit',
            df.columns[6]: 'amount_credit'
        }

        df = df[df[df.columns[4]] != '']

        df.loc[df[df.columns[4]] !=
               '', df.columns[4]] = 1

        df.iloc[:, 5] = pd.to_numeric(
            df.iloc[:, 5], errors='coerce')

        df.iloc[:, 6] = pd.to_numeric(
            df.iloc[:, 6], errors='coerce')

        df.iloc[:, 5] = df.iloc[:, 5].fillna('')
        df.iloc[:, 6] = df.iloc[:, 6].fillna('')

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


@api_view(['GET'])
def FetchGJ(request):
    # response = Journal.objects.all().order_by('-id')
    response = Journal.objects.annotate(
        debit=ExpressionWrapper(
            Sum('generaljournal__amount_debit', output_field=DecimalField()),
            output_field=DecimalField()
        ),
        credit=ExpressionWrapper(
            Sum('generaljournal__amount_credit', output_field=DecimalField()),
            output_field=DecimalField()
        ),
    ).values('id', 'sheet_no', 'month', 'year', 'remarks', 'created_at', 'updated_at', 'debit', 'credit').order_by('id')
    serializer = JournalSerializer(response, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def DeleteGJ(request, pk):
    JournalData = get_object_or_404(Journal, pk=pk)
    JournalData.delete()
    response_data = {"status": "General Journal Deleted Successfully"}
    return Response(response_data, status=status.HTTP_200_OK)


def Fetch(request, pk):
    journal_response = Journal.objects.get(pk=pk)
    journal_serializer = JournalSerializer(journal_response, many=False)

    gj_response = GeneralJournal.objects.filter(journal=pk)
    gj_serializer = GeneralJournalSerializer(gj_response, many=True)

    data = {
        'journal': journal_serializer.data,
        'receipts_journal': gj_serializer.data
    }

    return JsonResponse(data, safe=False)


@api_view(['POST'])
def UpdateJournal(request, pk):
    sheet_no = request.POST.get('sheet_no')
    month = request.POST.get('month')
    year = request.POST.get('year')
    remarks = request.POST.get('remarks')
    user_id = request.user.id

    journal_data = Journal.objects.get(pk=pk)
    journal_data.sheet_no = sheet_no
    journal_data.month = month
    journal_data.year = year
    journal_data.remarks = remarks
    journal_data.author_id = user_id
    journal_data.save()

    response_data = {"status": "Journal Updated Successfully"}
    return Response(response_data, status=status.HTTP_200_OK)
