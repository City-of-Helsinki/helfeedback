from django.contrib import admin

# Register your models here.
from .models import Feedback, SlackNotifier


class FeedbackAdmin(admin.ModelAdmin):
    pass


class SlackNotifierAdmin(admin.ModelAdmin):
    pass


admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(SlackNotifier, SlackNotifierAdmin)
