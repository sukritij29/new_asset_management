from django.core.exceptions import ValidationError
from django.db import models
# Create your models here.
from django.utils.text import slugify

from users_module.models import User


class Proposal(models.Model):
    title = models.CharField(max_length=150, unique=True)
    proposal_slug = models.SlugField(max_length=200, primary_key=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proposals')

    description = models.TextField(blank=True)

    due_date = models.DateField(blank=True, null=True)

    delivery_date = models.DateField(blank=True, null=True)

    emails = models.URLField(blank=True)

    amount = models.CharField(max_length=150,blank=True, null=True)

    address = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=15, choices=(
        ('Proposed', 'Proposed'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    ), default='Proposed')

    approved_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='approved_proposals', null=True,
                                    blank=True)
    form_complete = models.BooleanField(default=False)

    @property
    def is_owner(self, user):
        return self.owner == user

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.project_slug = slugify(self.title)
        super(Proposal, self).save(*args, **kwargs)