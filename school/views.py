from django.shortcuts import render,redirect
from .models import SchoolInfo, Slider
from django.contrib.auth import logout
from .models import AboutUs
from .models import CallbackRequest
from django.views.decorators.http import require_POST
import json
from django.http import JsonResponse



def home(request):
    school_info = SchoolInfo.objects.first()  # Assuming only one school info
    main_sliders = Slider.objects.filter(category=Slider.MAIN_SLIDER)
    middle_sliders = Slider.objects.filter(category=Slider.MIDDLE_SLIDER)
    bottom_sliders = Slider.objects.filter(category=Slider.BOTTOM_SLIDER)

    context = {
        'school_info': school_info,
        'main_sliders': main_sliders,
        'middle_sliders': middle_sliders,
        'bottom_sliders': bottom_sliders,
    }
    return render(request, 'school/home.html', context)

def about_us_view(request):
    about_us_info = AboutUs.objects.first()  # Assuming only one AboutUs instance
    return render(request, 'school/about_us.html', {'about_us_info': about_us_info})

def contact_us(request):
    return render(request, 'school/contact_us.html')

def custom_logout(request):
    logout(request)
    return redirect('school:home')  # Redirect to your home page

from .models import CallbackRequest
from django.views.decorators.http import require_POST
import json

@require_POST
def request_callback(request):
    try:
        data = json.loads(request.body)
        name = data.get('name')
        phone_number = data.get('phone_number')
        message = data.get('message')

        if not name or not phone_number:
            return JsonResponse({'error': 'Name and phone number are required.'}, status=400)

        CallbackRequest.objects.create(name=name, phone_number=phone_number, message=message)
        return JsonResponse({'message': 'Callback request received successfully.'})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
