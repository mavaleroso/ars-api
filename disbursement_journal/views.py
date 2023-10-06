from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from disbursement_journal.models import DisbursementJournalResource, DisbursementJournal, CDJ
from disbursement_journal.serializers import DisbursementJournalSerializer, CDJSerializer
from rest_framework.decorators import api_view
from rest_framework import generics, parsers, status
from rest_framework.response import Response
import pandas as pd
from tablib import Dataset

# Create your views here.


@api_view(['GET'])
def FetchCDJ(request):
    response = CDJ.objects.all().order_by('-id')
    serializer = CDJSerializer(response, many=True)
    return JsonResponse(serializer.data, safe=False)


def Fetch(request, pk):
    cdj_response = CDJ.objects.get(pk=pk)
    cdj_serializer = CDJSerializer(cdj_response, many=False)

    dj_response = DisbursementJournal.objects.filter(cdj=pk)
    dj_serializer = DisbursementJournalSerializer(dj_response, many=True)

    data = {
        'cdj': cdj_serializer.data,
        'disbursement_journal': dj_serializer.data
    }

    return JsonResponse(data, safe=False)


class ImportDisbursementJournalData(generics.GenericAPIView):
    parser_classes = [parsers.MultiPartParser]

    def post(self, request, *args, **kwargs):
        description = request.POST.get('description')
        month = request.POST.get('month')
        year = request.POST.get('year')
        remarks = request.POST.get('remarks')
        user_id = request.user.id

        cdj_query = CDJ(description=description, month=month,
                        year=year, remarks=remarks, author_id=user_id)

        cdj_query.save()

        file = request.FILES['attachment']
        df = pd.read_excel(file, keep_default_na=False)

        """Rename the headeers in the excel file
           to match Django models fields"""

        rename_columns = {
            "RECON": "recon_no",
            "SEQ": "seq",
            "MONTH": "month",
            "DATE": "date",
            "YEAR": "year",
            "CHECK NO.": "check_no",
            "DV YEAR": "dv_year",
            "DV MONTH": "dv_month",
            "DV NO.": "dv_no",
            "SOURCE": "source",
            "PAYEE": "payee",
            "NATURE OF PAYMENT": "nature_of_payment",
            "CHECK": "check_tmp",
            "CASH": "cash",
            "TAX": "tax",
            "%": "tax_percent",
            "TAX2": "tax2",
            "%2": "tax2_percent",
            "REMITTANCE": "remittance",
            "ROD": "rod",
            "CASH POSITION": "cash_position",
            "PPA": "ppa",
            "PROJ / CHRGE CNTR": "charge_center",
            "SET": "set",
            "PURPOSE": "purpose",
            "Fund": "fund",
            "ACCOUNT CODE": "account_code",
            "Old Code": "old_code",
            "ALOBS Yr": "alobs_year",
            "ALOBS MO": "alobs_month",
            "ALOBS No.2": "alobs_no",
            "SAA AMT": "sa_aamt",
            "Earmark": "earmark",
            "DEBIT2": "debit",
            "CREDIT": "credit",
            "AP CHRGD FROM": "ap_charge_from",
            "Old Code2": "old_code2",
            "Payment Remarks": "payment_remarks",
            "BUDGET CODE": "budget_code",
            "Expense Class": "expense_class",
            "Authorization": "authorization",
            "BUR AP": "bur_ap",
            "Type": "type",
            "Quarter": "quarter",
            "SAA #": "saa_no",
            "RAO REF#2": "rao_ref",
            "UACS DESCRIPTION": "uacs_description",
            "CMF/DR ": "cmf_dr",
            "BUR": "bur",
            "aa": "aa",
            "DD/NYD": "dd_nyd",
        }
        df['cdj_id'] = cdj_query.id

        df.rename(columns=rename_columns, inplace=True)

        # Call the Student Resource Model and make its instance
        disbursement_journal_resource = DisbursementJournalResource()

        # Load the pandas dataframe into a tablib dataset
        dataset = Dataset().load(df)

        # Call the import_data hook and pass the tablib dataset
        result = disbursement_journal_resource.import_data(
            dataset, dry_run=True, raise_errors=True)
        # print(dataset)
        if not result.has_errors():
            result = disbursement_journal_resource.import_data(
                dataset, dry_run=False)
            return Response({"status": "Disbursement Journal Data Imported Successfully"})

        return Response({"status": "Failed to import Disbursement Journal Data! Please contact your the developer"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def DeleteCDJ(request, pk):
    CDJData = get_object_or_404(CDJ, pk=pk)
    CDJData.delete()
    response_data = {"status": "CDJ Deleted Successfully"}
    return Response(response_data, status=status.HTTP_200_OK)
