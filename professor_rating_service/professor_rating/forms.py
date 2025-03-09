# from django import forms
# from .models import Rating

# class RatingForm(forms.ModelForm):
#     class Meta:
#         model = Rating
#         fields = ['score']

#     def clean_score(self):
#         score = self.cleaned_data.get('score')
#         if score is None:
#             raise forms.ValidationError("Rating score is required.")
#         if score < 1 or score > 5:
#             raise forms.ValidationError("Rating must be between 1 and 5.")
#         return score
