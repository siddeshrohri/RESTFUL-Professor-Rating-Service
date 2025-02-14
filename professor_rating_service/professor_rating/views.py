from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.http import JsonResponse
from .models import Rating, Professor, Module
from .forms import RatingForm
import json
from django.views.decorators.csrf import csrf_exempt


# 🎯 List all professors and modules (Updated to work with models)
@login_required
def professor_list(request):
    professors = Professor.objects.all()  # Get professors from the database
    modules = Module.objects.all()  # Get all modules

    # Calculate average rating for each professor dynamically
    for professor in professors:
        ratings = Rating.objects.filter(professor=professor)  # Get all ratings for the professor
        if ratings:
            avg_rating = sum(rating.score for rating in ratings) / len(ratings)  # Calculate average
            professor.average_rating = avg_rating  # Set the professor's average rating
        else:
            professor.average_rating = 0  # Set to 0 if no ratings exist

    return render(request, 'professor_rating/professor_list.html', {'professors': professors, 'modules': modules})


# 🎯 Rate a professor for a module (Updated to use the existing form and model)
@login_required
def rate_professor(request, professor_id, module_code):
    professor = get_object_or_404(Professor, id=professor_id)
    module = get_object_or_404(Module, module_code=module_code)

    # Create or fetch the Rating object, ensuring it’s specific to the professor and module
    rating, created = Rating.objects.get_or_create(professor=professor, user=request.user, module=module, defaults={'score': 0})

    if request.method == "POST":
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            form.save()  # Save rating for this specific professor-module pair
            return redirect('professor_list')  # Redirect to the professor list after submission
    else:
        form = RatingForm(instance=rating)

    return render(request, 'professor_rating/rate_professor.html', {'form': form, 'professor': professor, 'module': module})



@login_required
def view_ratings(request):
    ratings = Rating.objects.all().values('professor__name', 'user__username', 'score', 'module__name', 'module__year', 'module__semester', 'created_at')
    return JsonResponse({'ratings': list(ratings)})

# 🎯 View average rating for a professor and module
@login_required
def average_rating(request, professor_id, module_code):
    professor = get_object_or_404(Professor, id=professor_id)
    module = get_object_or_404(Module, code=module_code)
    ratings = Rating.objects.filter(professor=professor, module=module)

    if not ratings:
        return JsonResponse({'error': 'No ratings found for this professor in the given module'}, status=404)

    avg_rating = sum(rating.score for rating in ratings) / len(ratings)
    return JsonResponse({
        'professor_id': professor.id,
        'module_code': module.code,
        'average_rating': avg_rating
    })

# 🎯 Submit a rating for a professor (API Route)
@csrf_exempt
@login_required
def api_rate_professor(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            professor_id = data['professor_id']
            module_code = data['module_code']
            rating = data['rating']

            if rating < 1 or rating > 5:
                return JsonResponse({'error': 'Rating must be between 1 and 5'}, status=400)

            professor = get_object_or_404(Professor, id=professor_id)
            module = get_object_or_404(Module, code=module_code)
            rating_obj = Rating.objects.create(
                professor=professor,
                user=request.user,
                module=module,
                score=rating
            )

            return JsonResponse({'message': 'Rating submitted successfully'})

        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid request format'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

# 🎯 Home redirect (Kept as is)
def home(request):
    return redirect('/accounts/login/')
