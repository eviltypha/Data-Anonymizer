from django import forms
from .models import Upload


class FileForm(forms.ModelForm):
    # disabled_fields = ('temp_id',)

    class Meta:
        model = Upload
        # disabled_fields = ('temp_id',)
        fields = ('temp_id', 'doc')
        widgets = {'temp_id': forms.HiddenInput()}
        # def __init__(self, *args, **kwargs):
        #     super(FileForm, self).__init__(*args, **kwargs)
        #     for field in self.disabled_fields:
        #         self.fields[field].disabled = True
