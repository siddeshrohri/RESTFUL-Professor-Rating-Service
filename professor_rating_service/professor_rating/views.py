from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Rating, Professor, Module
import json
from django.views.decorators.csrf import csrf_exempt

@login_required
def professor_list(request):
    """
    Returns a list of all professors and their related modules in JSON format.
    """
    try:
        professors = Professor.objects.all()
        modules = Module.objects.all()

        professor_list_data = []
        for professor in professors:
            avg_rating_profs = professor.average_rating_prof()
            professor_list_data.append({
                'id': professor.id,
                'name': professor.name,
                'department': professor.department,
                'average_rating': avg_rating_profs,
            })

        modules_list_data = []
        for module in modules:
            profs = module.professors.all()
            modules_list_data.append({
                'module_code': module.module_code,
                'name': module.name,
                'department': module.department,
                'year': module.year,
                'semester': module.semester,
                'average_rating': module.average_rating,
                'professors': [{'id': prof.id, 'name': prof.name} for prof in profs]
            })

        return JsonResponse({'professors': professor_list_data, 'modules': modules_list_data})
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)


# @csrf_exempt
# @login_required
# def rate_professor(request, professor_id, module_code):
#     try:
#         professor = get_object_or_404(Professor, id=professor_id)
#         module = get_object_or_404(Module, module_code=module_code)
#     except Exception as e:
#         return JsonResponse({'error': f'Error retrieving objects: {str(e)}'}, status=500)

#     if professor not in module.professors.all():
#         return JsonResponse({'error': 'Professor does not teach this module'}, status=400)

#     try:
#         rating, created = Rating.objects.get_or_create(
#             professor=professor,
#             user=request.user,
#             module=module,
#             defaults={'score': 0}
#         )
#     except Exception as e:
#         return JsonResponse({'error': f'Error retrieving/creating rating: {str(e)}'}, status=500)

#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             new_score = data.get('score')
#             if new_score is None:
#                 return JsonResponse({'error': 'Rating score not provided'}, status=400)
#             new_score = int(new_score)
#             if new_score < 1 or new_score > 5:
#                 return JsonResponse({'error': 'Rating must be between 1 and 5'}, status=400)

#             rating.score = new_score
#             rating.save()
#             return JsonResponse({
#                 'message': 'Rating updated successfully',
#                 'professor_id': professor.id,
#                 'module_code': module.module_code,
#                 'score': rating.score
#             })
#         except (json.JSONDecodeError, ValueError) as e:
#             return JsonResponse({'error': f'Invalid rating format: {str(e)}'}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)

#     try:
#         return JsonResponse({
#             'professor': {
#                 'id': professor.id,
#                 'name': professor.name,
#                 'department': professor.department
#             },
#             'module': {
#                 'module_code': module.module_code,
#                 'name': module.name,
#                 'department': module.department,
#                 'year': module.year,
#                 'semester': module.semester
#             },
#             'rating': rating.score
#         })
#     except Exception as e:
#         return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)


@login_required
def view_ratings(request):
    """
    Returns the overall average ratings for all professors.
    """
    try:
        professors = Professor.objects.all()
        ratings_data = []
        for professor in professors:
            ratings_data.append({
                'professor_id': professor.id,
                'professor_name': professor.name,
                'department': professor.department,
                'average_rating': professor.average_rating_prof(),
            })
        return JsonResponse({'ratings': ratings_data})
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)


@login_required
def average_rating(request, professor_id, module_code):
    """
    Returns the average rating for a module taught by a specific professor.
    """
    try:
        professor = get_object_or_404(Professor, id=professor_id)
        module = get_object_or_404(Module, module_code=module_code)
    except Exception as e:
        return JsonResponse({'error': f'Error retrieving objects: {str(e)}'}, status=500)

    if professor not in module.professors.all():
        return JsonResponse({'error': 'Professor does not teach this module'}, status=400)

    try:
        ratings = Rating.objects.filter(professor=professor, module=module)
        if not ratings:
            avg_rating = 0.0
        else:
            avg_rating = sum(rating.score for rating in ratings) / len(ratings)
        return JsonResponse({
            'professor_id': professor.id,
            'module_code': module.module_code,
            'average_rating': avg_rating
        })
    except Exception as e:
        return JsonResponse({'error': f'Error calculating average: {str(e)}'}, status=500)


@csrf_exempt
@login_required
def api_rate_professor(request):
    """
    API endpoint to rate a professor for a specific module instance.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            professor_id = data.get('professor_id')
            module_code = data.get('module_code')
            year = data.get('year')
            semester = data.get('semester')
            rating_value = data.get('rating')

            if not all([professor_id, module_code, year, semester, rating_value]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            try:
                rating_value = int(rating_value)
            except ValueError:
                return JsonResponse({'error': 'Rating must be an integer'}, status=400)
            if rating_value < 1 or rating_value > 5:
                return JsonResponse({'error': 'Rating must be between 1 and 5'}, status=400)

            try:
                year = int(year)
            except ValueError:
                return JsonResponse({'error': 'Year must be an integer'}, status=400)

            try:
                semester = int(semester)
            except ValueError:
                return JsonResponse({'error': 'Semester must be an integer'}, status=400)
            if semester not in [1, 2]:
                return JsonResponse({'error': 'Semester must be either 1 or 2'}, status=400)

            professor = get_object_or_404(Professor, id=professor_id)

            module_qs = Module.objects.filter(module_code=module_code)
            if not module_qs.exists():
                return JsonResponse({
                    'error': f'No module found with module code {module_code}'
                }, status=400)

            module_year_qs = module_qs.filter(year=year)
            if not module_year_qs.exists():
                return JsonResponse({
                    'error': f'No module instance found for module code {module_code} in year {year}'
                }, status=400)

            module_instance_qs = module_year_qs.filter(semester=semester)
            if not module_instance_qs.exists():
                return JsonResponse({
                    'error': f'No module instance found for module code {module_code} in year {year} for semester {semester}'
                }, status=400)

            module = module_instance_qs.first()

            if professor not in module.professors.all():
                return JsonResponse({
                    'error': 'Professor does not teach this module instance for the specified year and semester'
                }, status=400)

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
                'year': module.year,
                'semester': module.semester,
                'score': rating_obj.score
            }, status=200)
        except (json.JSONDecodeError, ValueError) as e:
            return JsonResponse({'error': f'Invalid input format: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
