from django.shortcuts import render
from django.http import JsonResponse
from .search import perform_search  # Ensure this import works

def home(request):
    return render(request, 'index.html')  # Ensure template path is correct

def search(request):
    query = request.GET.get('q', '')
    if query:
        results = perform_search(query)  # Call your search logic
        return JsonResponse(results, safe=False)
    return JsonResponse({"error": "No query parameter provided"}, status=400)
