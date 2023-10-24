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
        df = pd.read_excel(file, keep_default_na=False, skiprows=1)

        """Rename the headeers in the excel file
           to match Django models fields"""

        rename_columns = {
            df.columns[0]: "recon_no",
            df.columns[1]: "seq",
            df.columns[2]: "month",
            df.columns[3]: "date",
            df.columns[4]: "year",
            df.columns[5]: "check_no",
            df.columns[6]: "dv_year",
            df.columns[7]: "dv_month",
            df.columns[8]: "dv_no",
            df.columns[9]: "source",
            df.columns[10]: "payee",
            df.columns[11]: "nature_of_payment",
            df.columns[12]: "check_tmp",
            df.columns[13]: "cash",
            df.columns[14]: "tax",
            df.columns[15]: "tax_percent",
            df.columns[16]: "tax2",
            df.columns[17]: "tax2_percent",
            df.columns[18]: "remittance",
            df.columns[20]: "rod",
            df.columns[21]: "cash_position",
            df.columns[22]: "ppa",
            df.columns[23]: "charge_center",
            df.columns[24]: "set",
            df.columns[25]: "purpose",
            df.columns[26]: "fund",
            df.columns[27]: "account_code",
            df.columns[28]: "old_code",
            df.columns[29]: "alobs_year",
            df.columns[30]: "alobs_month",
            df.columns[31]: "alobs_no",
            df.columns[32]: "sa_aamt",
            df.columns[33]: "earmark",
            df.columns[34]: "debit",
            df.columns[35]: "credit",
            df.columns[36]: "ap_charge_from",
            df.columns[37]: "old_code2",
            df.columns[38]: "payment_remarks",
            df.columns[39]: "budget_code",
            df.columns[40]: "expense_class",
            df.columns[41]: "authorization",
            df.columns[42]: "bur_ap",
            df.columns[43]: "type",
            df.columns[44]: "quarter",
            df.columns[45]: "saa_no",
            df.columns[46]: "rao_ref",
            df.columns[47]: "uacs_description",
            df.columns[48]: "cmf_dr",
            df.columns[49]: "bur",
            df.columns[50]: "aa",
            df.columns[51]: "dd_nyd",
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
