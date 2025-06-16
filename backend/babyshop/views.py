from django.http import JsonResponse

def root_view(request):
    return JsonResponse({"message": "Welcome to Baby Shop API! Use /api/ for endpoints."})