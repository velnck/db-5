from django.forms import ModelForm
from .models import Reviews


class NewReviewForm(ModelForm):
    class Meta:
        model = Reviews
        fields = '__all__'
        exclude = ['id', 'book', 'review_author']

    def __init__(self, *args, **kwargs):
        super(NewReviewForm, self).__init__(*args, **kwargs)
        self.fields['review_text'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Add a comment...'
        })