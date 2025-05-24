from django.shortcuts import render
import csv
from io import TextIOWrapper
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from .serializers import UserSerializer
from .models import User

# Create your views here.

class CSVUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file uploaded'}, status=400)

        file = request.FILES['file']
        if not file.name.endswith('.csv'):
            return JsonResponse({'error': 'Only CSV files are allowed'}, status=400)

        csv_file = TextIOWrapper(file.file, encoding='utf-8')
        reader = csv.DictReader(csv_file)
        
        results = {
            'total_records': 0,
            'successful_records': 0,
            'failed_records': 0,
            'errors': []
        }

        for row_num, row in enumerate(reader, start=2):  # Start from 2 to account for header row
            results['total_records'] += 1
            try:
                # Convert age to integer
                row['age'] = int(row['age'])
                
                # Check if email already exists
                if User.objects.filter(email=row['email']).exists():
                    results['failed_records'] += 1
                    results['errors'].append({
                        'row': row_num,
                        'errors': {'email': ['Email already exists']}
                    })
                    continue

                # Validate and save the record
                serializer = UserSerializer(data=row)
                if serializer.is_valid():
                    serializer.save()
                    results['successful_records'] += 1
                else:
                    results['failed_records'] += 1
                    results['errors'].append({
                        'row': row_num,
                        'errors': serializer.errors
                    })
            except (ValueError, KeyError) as e:
                results['failed_records'] += 1
                results['errors'].append({
                    'row': row_num,
                    'errors': {'general': [str(e)]}
                })

        return JsonResponse(results)
