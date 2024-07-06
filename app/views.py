from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from app.models import Report, Visitor
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import qrcode
from io import BytesIO
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json


BASE_URL = "Add the ngrok url here"

def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('userid')  # Use get to avoid MultiValueDictKeyError
        password = request.POST.get('password')  # Use get to avoid MultiValueDictKeyError
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')
            else:
                 
                return render(request, 'login.html', {'error_message': "Invalid User ID or Password. Please try again."})
        else:
            
            return render(request, 'login.html', {'error_message': 'Please enter both User ID and Password.'})
    return render(request, 'login.html')

@csrf_exempt
def share_location(request, id):
    print(id)
    print(request.method)
    if request.method == 'POST':
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if latitude and longitude:
            # Process the location data (e.g., save it to the database)
            # Here we are just printing it for demonstration purposes
            visitor = Visitor.objects.get(id=id)
            visitor.latitude = latitude
            visitor.longitude = longitude
            visitor.save()
            return JsonResponse({'success': True, 'message': 'Location shared successfully.'})
        else:
            visitor = Visitor.objects.get(id=id)
            visitor.latitude = None
            visitor.longitude = None
            visitor.save()
            return JsonResponse({'success': False, 'message': 'Location sharing stopped'})

    else:
        # Handle GET request and render the share_location.html template
        visitor = get_object_or_404(Visitor, id=id)
        return render(request, 'share_location.html', {'visitor': visitor})

def track_visitor(request, visitor_id):
    visitors = get_object_or_404(Visitor, id=visitor_id)
    
    location_data = [{
        'name': visitor.visitor_name,
        'latitude': visitor.latitude,
        'longitude': visitor.longitude
    } for visitor in visitors]
    return JsonResponse({'success': True, 'locations': location_data})

def check_transactions(request, visitor_id):
    visitors = get_object_or_404(Visitor, id=visitor_id)
    transaction_data = [{
        'name': visitor.visitor_name,
        'time': visitor.created_at,
    } for visitor in visitors]
    return JsonResponse({'success': True, 'transactions': transaction_data})

@csrf_exempt
def create_report(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        visitor_name = request.POST.get('visitor-name')
        user = request.user if request.user.is_authenticated else None

        if title and content:
            if user:
                # Authenticated user
                report = Report(title=title, content=content, creator_type='user', creator_id=str(user.id))
            else:
                # Visitor
                report = Report(title=title, content=content, creator_type='visitor', creator_id=visitor_name)

            report.save()
            return JsonResponse({'success': True, 'message': 'Report submitted successfully!'})
        else:
            return JsonResponse({'success': False, 'message': 'Title and content are required.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
    
def visitor_view(request):
    return render(request, 'visitor.html')

def visitor_view(request):
    return render(request, 'visitor.html')


def visitor_dashboard(request):
    context = {}

    if request.method == 'POST':
        visitor_name = request.POST.get('name')
        visitor_email = request.POST.get('email')
        visitor_phone = request.POST.get('phone')
        purpose = request.POST.get('purpose')

        # Create a new visitor object
        visitor = Visitor.objects.create(
            visitor_name=visitor_name,
            visitor_email=visitor_email,
            visitor_phone=visitor_phone,
            purpose=purpose
        )

        # Generate QR code
        print(BASE_URL)
        qr_data = f"{BASE_URL}/share_location/{visitor.id}/"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        buffer = BytesIO()
        img.save(buffer)
        buffer.seek(0)

        # Save QR code image
        file_name = f"qr_codes/{visitor.id}.png"
        file_path = default_storage.save(file_name, ContentFile(buffer.read()))
        buffer.close()

        # Prepare context with a success message
        context = {
            'visitor_name': visitor_name,
            'success_message': 'Visitor registered successfully!',
            'qr_code_url': default_storage.url(file_path),
        }

    return render(request, 'visitor_dashboard.html', context)

def dashboard(request):
    user = request.user
    context = {
        'phone_number': user.phone_number,
        'email': user.email,
    }
    return render(request, 'dashboard.html', context)

@csrf_exempt
@require_POST
@login_required
def update_profile(request):
    user = request.user
    phone_number = request.POST.get('phone_number')
    email = request.POST.get('email')

    if phone_number and email:
        user.phone_number = phone_number
        user.email = email
        user.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid data'})
    
def get_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    return JsonResponse({'success': True, 'title': report.title, 'content': report.content})

def logout(request):
    auth_logout(request)
    return redirect('login')

def security_dashboard(request):
    reports = Report.objects.all()
    visitors = Visitor.objects.all()
    context = {
        'reports': reports,
        'visitors': visitors,
    }
    return render(request, 'security_dashboard.html', context)

def security_login(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        password = request.POST.get('password')
        
        user = authenticate(request, username=userid, password=password)
        
        if user is not None:
            login(request)
            # Redirect to dashboard or success page
            return redirect('dashboard')
        else:
            error_message = "Invalid User ID or Password. Please try again."
            return render(request, 'security_login.html', {'error_message': error_message})
    
    return render(request, 'security_login.html')