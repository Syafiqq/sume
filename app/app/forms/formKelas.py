from django import forms
from django.contrib.auth.models import User


class BuatKelas(forms.Form):
    users = User.objects.filter(is_staff=False, is_superuser=False)
    staffs = User.objects.filter(is_staff=True, is_superuser=False)

    pilihan1 = []
    pilihan2 = []
    for user in users:
        new = [user.id, user.username]
        pilihan1.append(new)

    for staff in staffs:
        new = [staff.id, staff.username]
        pilihan2.append(new)

    name = forms.CharField(max_length=200)
    deskripsi = forms.CharField()
    members = forms.MultipleChoiceField(choices=pilihan1)
    staffs = forms.MultipleChoiceField(choices=pilihan2)
    startdate = forms.DateField()
    enddate = forms.DateField()
