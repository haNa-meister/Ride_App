from django import forms


class reqForm(forms.Form):
    destination_add = forms.CharField(label='destination', max_length=128,
                                      widget=forms.TextInput(attrs={'class': 'form-control'}))
    arrive_time = forms.DateTimeField(label='arrive time',
                                      widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    passenger = forms.IntegerField(label='passenger_number')
    vehicle_type = forms.CharField(label='vehicle_type', max_length=128,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    if_shared = forms.BooleanField(label='if shared', required=False)
    special_info = forms.CharField(label='special information', max_length=128,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}),
                                   required=False)


class editRideForm(forms.Form):
    destination_add = forms.CharField(label='destination', max_length=128,
                                      widget=forms.TextInput(attrs={'class': 'form-control'}),
                                      required=False)
    arrive_time = forms.DateTimeField(label='arrive time',
                                      widget=forms.DateTimeInput(attrs={'class': 'form-control'}),
                                      required=False)
    passenger = forms.IntegerField(label='passenger_number', required=False)
    vehicle_type = forms.CharField(label='vehicle_type', max_length=128,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}),
                                   required=False)
    if_shared = forms.BooleanField(label='if shared', required=False)
    special_info = forms.CharField(label='special information', max_length=128,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}),
                                   required=False)
