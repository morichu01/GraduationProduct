import bootstrap_datepicker_plus as datetimepicker
from django import forms
from .models import *
from django.contrib.auth.models import User
import bootstrap_datepicker_plus as datetimepicker


class UserForm(forms.ModelForm):
  
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ("username", "last_name", "first_name", "email",)


class BorrowForm(forms.ModelForm):

    class Meta:
        model = Borrow
        fields = ('title','user','start', 'end')
        widgets = {
            'title': forms.HiddenInput(),

            'user': forms.HiddenInput(),

            'start': datetimepicker.DatePickerInput(
                format='%Y-%m-%d',
                options={
                    'locale': 'ja',
                    'dayViewHeaderFormat': 'YYYY年 MMMM',
                }
            ).start_of('rental_tarm'),

            'end': datetimepicker.DatePickerInput(
                format='%Y-%m-%d',
                options={
                    'locale': 'ja',
                    'dayViewHeaderFormat': 'YYYY年 MMMM',
                }
            ).end_of('rental_tarm'),
        }
