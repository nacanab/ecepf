from django.db import models
from accounts.models import Student

class Badge(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='badges/', blank=True, null=True)  # Pour stocker les images des badges

    def __str__(self):
        return self.nom
    
class AttributionBadge(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    date_attribution = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.badge}"