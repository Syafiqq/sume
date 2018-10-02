from django import forms

class UploadDokumen(forms.Form):
    name = forms.CharField(max_length=200)
    file_upload = forms.FileField()
