from django.forms import ModelForm, RadioSelect
from .models import Feedback

class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'body', 'url', 'email']
        widgets = {
            'rating': RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        del(self.fields['rating'].widget.choices[0])
