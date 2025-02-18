from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Rating, Professor, Module
from .forms import RatingForm
import json
from django.views.decorators.csrf import csrf_exempt

@login_required
def professor_list(request):
    professors = Professor.objects.all()  # Get professors from the database
    modules = Module.objects.all()        # Get all modules

    # Prepare JSON data for professors
    professor_list_data = []
    for professor in professors:
        ratings = Rating.objects.filter(professor=professor)
        if ratings:
            avg_rating = sum(r.score for r in ratings) / len(ratings)
        else:
            avg_rating = 0
        professor_list_data.append({
            'id': professor.id,
            'name': professor.name,
            'department': professor.department,
            'average_rating': avg_rating,
        })

    # Prepare JSON data for modules and include professor details.
    # Since Module doesn't have its own department field, we use professor.department.
    modules_list_data = []
    for module in modules:
        modules_list_data.append({
            'module_code': module.module_code,
            # Use the department from the associated professor
            'department': module.professor.department,
            'year': module.year,
            'semester': module.semester,
            'average_rating': module.average_rating,
            'professor_id': module.professor.id,
            'professor_name': module.professor.name,
        })

    return JsonResponse({'professors': professor_list_data, 'modules': modules_list_data})


@csrf_exempt
@login_required
def rate_professor(request, professor_id, module_code):
    professor = get_object_or_404(Professor, id=professor_id)
    module = get_object_or_404(Module, module_code=module_code)

    # Get or create the Rating object for this professor-user-module combination
    rating, created = Rating.objects.get_or_create(
        professor=professor,
        user=request.user,
        module=module,
        defaults={'score': 0}
    )

    if request.method == "POST":
        # Try to get the rating from a JSON payload first, fallback to POST data
        try:
            data = json.loads(request.body)
            new_score = data.get('score')
        except (json.JSONDecodeError, TypeError):
            new_score = request.POST.get('score')

        if new_score is None:
            return JsonResponse({'error': 'Rating score not provided'}, status=400)
        try:
            new_score = int(new_score)
        except ValueError:
            return JsonResponse({'error': 'Invalid rating score'}, status=400)

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
    else:
        # For GET, return the current rating details
        return JsonResponse({
            'professor': {
                'id': professor.id,
                'name': professor.name,
                'department': professor.department
            },
            'module': {
                'module_code': module.module_code,
                # Retrieve department from professor since Module doesn't have its own department field
                'department': module.professor.department,
                'year': module.year,
                'semester': module.semester
            },
            'rating': rating.score
        })


@login_required
def view_ratings(request):
    ratings = Rating.objects.all().values(
        'professor__name', 'user__username', 'score',
        # Use the professor's department for the module
        'module__professor__department', 'module__year', 'module__semester', 'created_at'
    )
    return JsonResponse({'ratings': list(ratings)})


@login_required
def average_rating(request, professor_id, module_code):
    professor = get_object_or_404(Professor, id=professor_id)
    module = get_object_or_404(Module, module_code=module_code)
    ratings = Rating.objects.filter(professor=professor, module=module)

    if not ratings:
        return JsonResponse({'error': 'No ratings found for this professor in the given module'}, status=404)

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

            try:
                rating_value = int(rating_value)
                if rating_value < 1 or rating_value > 5:
                    return JsonResponse({'error': 'Rating must be between 1 and 5'}, status=400)
            except ValueError:
                return JsonResponse({'error': 'Invalid rating value'}, status=400)

            professor = get_object_or_404(Professor, id=professor_id)
            module = get_object_or_404(Module, module_code=module_code)

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

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)



def home(request):
    return JsonResponse({'message': 'Please login to access the service', 'redirect': '/accounts/login/'})
