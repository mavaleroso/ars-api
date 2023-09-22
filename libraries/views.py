from django.shortcuts import render
from django.http import JsonResponse
from libraries.models import AccountsResource, Accounts
from libraries.serializers import AccountsSerializer
from rest_framework.decorators import api_view
from rest_framework import generics, parsers, status
from rest_framework.response import Response
import pandas as pd
from tablib import Dataset

# Create your views here.


@api_view(['GET'])
def FetchAccounts(request):
    response = Accounts.objects.all()
    serializer = AccountsSerializer(response, many=True)
    return JsonResponse(serializer.data, safe=False)


class ImportAccountsData(generics.GenericAPIView):
    parser_classes = [parsers.MultiPartParser]

    def post(self, request, *args, **kwargs):
        print(request)
        file = request.FILES['attachment']
        df = pd.read_excel(file)

        """Rename the headeers in the excel file
           to match Django models fields"""

        rename_columns = {"UACS Object Code": "uacs_object_code", "Account Title": "account_title",
                          "RCA Code": "rca_code", "UACS Sub Object Code": "uacs_subobject_code"}

        df.rename(columns=rename_columns, inplace=True)

        # Call the Student Resource Model and make its instance
        accounts_resource = AccountsResource()

        # Load the pandas dataframe into a tablib dataset
        dataset = Dataset().load(df)

        # Call the import_data hook and pass the tablib dataset
        result = accounts_resource.import_data(
            dataset, dry_run=True, raise_errors=True)

        if not result.has_errors():
            result = accounts_resource.import_data(dataset, dry_run=False)
            return Response({"status": "Accounts Data Imported Successfully"})

        return Response({"status": "Not Imported Accounts Data"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def CreateAccounts(request):
    serializer = AccountsSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

