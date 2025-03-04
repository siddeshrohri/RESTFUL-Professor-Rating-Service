from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Rating, Professor, Module
import json
from django.views.decorators.csrf import csrf_exempt



@login_required
def professor_list(request):
    professors = Professor.objects.all()  # Get all professors
    modules = Module.objects.all()        # Get all modules

    # Prepare JSON data for professors
    professor_list_data = []
    for professor in professors:
        avg_rating = professor.get_average_rating()
        professor_list_data.append({
            'id': professor.id,
            'name': professor.name,
            'department': professor.department,
            'average_rating': avg_rating,
        })

    # Prepare JSON data for modules and include professors
    modules_list_data = []
    for module in modules:
        professors = module.professors.all()  # Get all professors for this module
        modules_list_data.append({
            'module_code': module.module_code,
            'name': module.name,  # Include module name
            'department': module.department,
            'year': module.year,
            'semester': module.semester,
            'average_rating': module.average_rating,
            'professors': [{'id': prof.id, 'name': prof.name} for prof in professors]  # List of professors teaching this module
        })

    return JsonResponse({'professors': professor_list_data, 'modules': modules_list_data})


@csrf_exempt
@login_required
def rate_professor(request, professor_id, module_code):
    professor = get_object_or_404(Professor, id=professor_id)
    module = get_object_or_404(Module, module_code=module_code)

    # Ensure professor is actually teaching this module
    if professor not in module.professors.all():
        return JsonResponse({'error': 'Professor does not teach this module'}, status=400)

    # Get or create the Rating object for this professor-user-module combination
    rating, created = Rating.objects.get_or_create(
        professor=professor,
        user=request.user,
        module=module,
        defaults={'score': 0}
    )

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_score = data.get('score')

            if new_score is None:
                return JsonResponse({'error': 'Rating score not provided'}, status=400)

            new_score = int(new_score)
            if new_score < 1 or new_score > 5:
                return JsonResponse({'error': 'Rating must be between 1 and 5'}, status=400)

            rating.score = new_score
            rating.save()

            return JsonResponse({
                'message': 'Rating updated successfully',
                'professor_id': professor.id,
                'module_code': module.module_code,
                'score': rating.score
            })

        except (json.JSONDecodeError, ValueError):
            return JsonResponse({'error': 'Invalid rating format'}, status=400)

    return JsonResponse({
        'professor': {
            'id': professor.id,
            'name': professor.name,
            'department': professor.department
        },
        'module': {
            'module_code': module.module_code,
            'name': module.name,
            'department': module.department,
            'year': module.year,
            'semester': module.semester
        },
        'rating': rating.score
    })


@login_required
def view_ratings(request):
    # Return overall professor ratings, even if no ratings exist.
    professors = Professor.objects.all()
    ratings_data = []
    for professor in professors:
        ratings_data.append({
            'professor_id': professor.id,
            'professor_name': professor.name,
            'department': professor.department,
            'average_rating': professor.get_average_rating(),  # This returns 0.0 if no ratings exist
        })
    return JsonResponse({'ratings': ratings_data})




@login_required
def average_rating(request, professor_id, module_code):
    professor = get_object_or_404(Professor, id=professor_id)
    module = get_object_or_404(Module, module_code=module_code)
    
    # Ensure professor teaches this module
    if professor not in module.professors.all():
        return JsonResponse({'error': 'Professor does not teach this module'}, status=400)
    
    ratings = Rating.objects.filter(professor=professor, module=module)
    if not ratings:
        avg_rating = 0.0  # Return 0.0 if no ratings exist
    else:
        avg_rating = sum(rating.score for rating in ratings) / len(ratings)
    
    return JsonResponse({
        'professor_id': professor.id,
        'module_code': module.module_code,
        'average_rating': avg_rating
    })



@csrf_exempt
@login_required
def api_rate_professor(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            professor_id = data.get('professor_id')
            module_code = data.get('module_code')
            rating_value = data.get('rating')

            if not all([professor_id, module_code, rating_value]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            rating_value = int(rating_value)
            if rating_value < 1 or rating_value > 5:
                return JsonResponse({'error': 'Rating must be between 1 and 5'}, status=400)

            professor = get_object_or_404(Professor, id=professor_id)
            module = get_object_or_404(Module, module_code=module_code)

            # Ensure professor teaches this module
            if professor not in module.professors.all():
                return JsonResponse({'error': 'Professor does not teach this module'}, status=400)

            rating_obj, created = Rating.objects.get_or_create(
                professor=professor,
                user=request.user,
                module=module,
                defaults={'score': rating_value}
            )

            if not created:
                rating_obj.score = rating_value
                rating_obj.save()

            return JsonResponse({
                'message': 'Rating submitted successfully',
                'professor_id': professor.id,
                'module_code': module.module_code,
                'score': rating_obj.score
            }, status=200)

        except (json.JSONDecodeError, ValueError):
            return JsonResponse({'error': 'Invalid input format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


# def home(request):
#     return JsonResponse({'message': 'Please login to access the service', 'redirect': '/admin/login/'})
