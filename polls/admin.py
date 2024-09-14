"""Admin class."""
from django.contrib import admin
from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    """Inline admin descriptor for Choice model."""
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Admin interface for the Question model."""
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date', 'end_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently', 'end_date', 'can_vote')
    list_filter = ['pub_date', 'end_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
