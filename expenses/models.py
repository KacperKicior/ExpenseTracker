from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

CURRENCY_CHOICES = [
    ("PLN", "Polish Złoty"),
    ("EUR", "Euro"),
    ("USD", "US Dollar"),
    ("GBP", "British Pound"),
]

LANGUAGE_CHOICES = [
    ("pl", _("Polish")),
    ("en", _("English")),
    ("de", _("German")),
]

CURRENCY_SYMBOLS = {
    "PLN": "zł",
    "EUR": "€",
    "USD": "$",
    "GBP": "£",
}


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="PLN")
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default="pl")

    def __str__(self):
        return f"Profile of {self.user.username}"

    @property
    def currency_symbol(self):
        return CURRENCY_SYMBOLS.get(self.currency, "")


class Category(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        unique_together = ('name', 'user')
        ordering = ['name']

    def __str__(self):
        return self.name


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.amount} - {self.category} ({self.date})"
