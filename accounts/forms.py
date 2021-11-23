from django.contrib.auth import forms as auth_forms
from django import forms
from .models import StudentVideo

class LoginForm(auth_forms.AuthenticationForm):
    '''ログインフォーム'''
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label

class WeeklyGoalForm(forms.Form):

    time = forms.IntegerField(label='目標勉強時間（h）')

"""
class VideoForm(forms.ModelForm):
    class Meta:
        model = StudentVideo
        fields = ('video',)
"""