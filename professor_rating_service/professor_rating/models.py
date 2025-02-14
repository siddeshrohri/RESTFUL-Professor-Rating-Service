from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User  # Import Django's User model

class Professor(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)

    def get_average_rating(self):
        """Dynamically calculate the professor's average rating based on module ratings."""
        module_ratings = self.modules.annotate(avg_module_rating=Avg('ratings__score')).values_list('avg_module_rating', flat=True)
        valid_ratings = [rating for rating in module_ratings if rating is not None]
        return sum(valid_ratings) / len(valid_ratings) if valid_ratings else 0.0

    def __str__(self):
        return f"{self.name} - Avg Rating: {self.get_average_rating():.2f}"

class Module(models.Model):
    module_code = models.CharField(max_length=20)  # Renamed to match the view reference
    name = models.CharField(max_length=255)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='modules')
    year = models.IntegerField()
    semester = models.CharField(max_length=10)
    average_rating = models.FloatField(default=0.0)  # Store module-wise average

    def update_average_rating(self):
        """Calculate and update the module's average rating dynamically."""
        avg_rating = self.ratings.aggregate(Avg('score'))['score__avg'] or 0.0
        self.average_rating = avg_rating
        self.save()

    def __str__(self):
        return f"{self.name} ({self.year} - {self.semester}) - Avg Rating: {self.average_rating:.2f}"

class Rating(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='ratings')

    class Meta:
        unique_together = ('professor', 'user', 'module')  # One rating per user per professor per module

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save rating first
        self.module.update_average_rating()  # Update module rating
        # No need to explicitly update the professor, as it is dynamically computed

    def __str__(self):
        return f"Rating: {self.score} for {self.professor.name} in {self.module.name} by {self.user.username}"
