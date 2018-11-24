from django import forms

class UploadData(forms.Form):
    namafile = forms.CharField(max_length=200)
    url_file = forms.FileField()
    datalatih = forms.BooleanField(required=False)
    datauji =  forms.BooleanField(required=False)
    is_dataset =  forms.BooleanField(required=False)
