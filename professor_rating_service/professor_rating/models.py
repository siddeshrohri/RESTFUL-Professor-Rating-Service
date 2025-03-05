from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User

class Professor(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)

    def average_rating_prof(self):
        """
        This function calculates the overall rating per professor by averaging the related modules
        of the professor by rounding to the nearest inter within the range of 1 to 5
        """
        module_ratings = (
            self.modules
            .annotate(avg_module_rating=Avg('ratings__score'))
            .values_list('avg_module_rating', flat=True)
        )
        valid_ratings = [rating for rating in module_ratings if rating is not None]
        if valid_ratings:
            return round(sum(valid_ratings) / len(valid_ratings))
        return 0

    def __str__(self):
        return f"{self.name} - Avg Rating: {self.average_rating_prof()}"


class Module(models.Model):
    module_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    professors = models.ManyToManyField(Professor, related_name='modules')
    department = models.CharField(max_length=255, default="")
    year = models.IntegerField()
    semester = models.CharField(max_length=10, default="")
    average_rating = models.FloatField(default=0.0)

    def update_average_rating_module(self):
        """
        This function calculates the overall rating of the module, rounding it to the
        nearest integer within the range of 1 to 5
        """
        avg_rating_module = self.ratings.aggregate(avg=Avg('score'))['avg'] or 0.0
        self.average_rating = round(avg_rating_module)
        self.save()

    def __str__(self):
        return f"{self.name} ({self.year} - {self.semester}) - Avg Rating: {round(self.average_rating)}"


class Rating(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='ratings')

    class Meta:
        unique_together = ('professor', 'user', 'module')

    def save(self, *args, **kwargs):
        """ Saves the rating first of the module and then calculates the average rating of the 
        module
        """
        super().save(*args, **kwargs)
        self.module.update_average_rating_module()

    def __str__(self):
        return (f"Rating: {self.score} for {self.professor.name} in "
                f"{self.module.name} by {self.user.username}")
