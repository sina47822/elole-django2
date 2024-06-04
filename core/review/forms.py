from django import forms
from .models import ReviewModel
from stylist.models import Services,ServiceStatusType

class SubmitReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewModel
        fields = ['service','rate', 'description']
        error_messages = {
            'description': {
                'required': 'فیلد توضیحات اجباری است',
            },
        }
    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get('service')

        # Check if the service exists and is published
        try:
            Services.objects.get(id=service.id,status=ServiceStatusType.publish.value)
        except Services.DoesNotExist:
            raise forms.ValidationError("این محصول وجود ندارد")

        return cleaned_data