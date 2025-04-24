from django.shortcuts import render ,redirect
from django.http import HttpResponse
import requests
import socket
import validators
from django.utils import timezone
from .models import HallOfFame, HallOfShame,RecentScan, GradeSummary
from django.db.models import Count,Sum



# Create your views here.
# def index(request):
#     return render(request, "scanner/index.html")

def index(request):
    recent_scans = RecentScan.objects.order_by('-id')[:9]
    hall_of_fame = HallOfFame.objects.all()[:9]
    hall_of_shame = HallOfShame.objects.all()[:9]
    grade_summary = GradeSummary.objects.all()
    total_count = GradeSummary.objects.aggregate(total=Sum('count'))['total'] or 0


    context = {
        "recent_scans": recent_scans,
        "hall_of_fame": hall_of_fame,
        "hall_of_shame": hall_of_shame,
        "grade_summary": grade_summary,
        "total_count": total_count  
    }

    return render(request, "myproject/scanner/templates/scanner/index.html",context)                     
def about(request):
     return render(request,'myproject/scanner/templates/scanner/about.html')
def fa(request):
     return render(request,'myproject/scanner/templates/scanner/fa.html')
def api(request):
     return render(request,'myproject/scanner/templates/scanner/api.html')
def terms(request):
     return render(request,'myproject/scanner/templates/scanner/terms.html')
def docs(request):
     return render(request,'myproject/scanner/templates/scanner/docs.html')

def grade(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        if not url:
            return render(request, 'myproject/scanner/templates/scanner/index.html', {'error': 'No URL provided'})
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url
        
        if not validators.url(url):
            return render(request, 'myproject/scanner/templates/scanner/invalid_url.html', {'error': 'Invalid URL format. Please enter a valid site URL.'})
        try:
            headers_req = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            }
            response = requests.get(url,headers=headers_req, timeout=10)
            headers = response.headers

            expected_headers = [
                'Content-Security-Policy',
                'Strict-Transport-Security',
                'Referrer-Policy',
                'X-Frame-Options',
                'X-Content-Type-Options',
                'Permissions-Policy'
            ]

            present_headers = []
            for header in expected_headers:
                if header in headers:
                    present_headers.append(header)
            header_statuses = []
            for header in expected_headers:
                header_statuses.append({
                    'name': header,
                    'present': header in present_headers
                })

            grade = "F"
            count = len(present_headers)
            if count == 6:
                grade = "A+"
            elif count == 5:
                grade = "A"
            elif count == 4:
                grade = "B"
            elif count == 3:
                grade = "C"
            elif count == 2:
                grade = "D"
            elif count == 1:
                grade = "E"
            

            domain = url.split('/')[2]
            try:
                ip_address = socket.gethostbyname(domain)
            except socket.gaierror:
                return render(request, 'myproject/scanner/templates/scanner/invalid_url.html', {'error': 'Failed to resolve domain. Please check the URL.'})
            # RecentScan.objects.create(url=url.strip(), grade=grade)
          
            try:
                if grade in ["A", "A+"]:
                    HallOfFame.objects.get_or_create(url=url.strip(), defaults={'grade': grade})
                elif grade in ["E","F"]:
                    HallOfShame.objects.get_or_create(url=url.strip(), defaults={'grade': grade})
                RecentScan.objects.create(url=url.strip(), grade=grade)
                
            except Exception as db_error:
                return render(request, 'myproject/scanner/templates/scanner/index.html', {'error': f'Database error: {db_error}'})
            # try:
            #     GradeSummary.objects.all().delete()
            #     grade_counts = RecentScan.objects.values('grade').annotate(count=Count('grade'))
            #     for item in grade_counts:
            #         GradeSummary.objects.create(grade=item['grade'], count=item['count'])
            # except Exception as summary_error:
            #     return render(request, 'scanner/index.html', {'error': f'Summary update error: {summary_error}'})
            try:
    # Define all possible grades
                all_grades = ["A+", "A", "B", "C", "D", "E", "F"]

    # Get counts from RecentScan
                grade_counts_qs = RecentScan.objects.values('grade').annotate(count=Count('grade'))
                grade_counts = {item['grade']: item['count'] for item in grade_counts_qs}

    # Update or create all GradeSummary records
                for g in all_grades:
                   GradeSummary.objects.update_or_create(
                        grade=g,
                        defaults={'count': grade_counts.get(g, 0)}
        )
      
            except Exception as summary_error:
                return render(request, 'myproject/scanner/templates/scanner/index.html', {'error': f'Summary update error: {summary_error}'})

            
            context = {
                'url': url,
                'ip_address': ip_address,
                'report_time': timezone.now(),
                'header_statuses': header_statuses,
                'present_headers': present_headers,
                'grade': grade
            }
            return render(request, 'myproject/scanner/templates/scanner/grade.html', context)

        except Exception as e:
            return render(request, 'myproject/scanner/templates/scanner/index.html', {'error': str(e)})

    return render(request,"myproject/scanner/templates/scanner/index.html")    
