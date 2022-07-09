from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class DateTimeForm(forms.Form):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )

class DateForm(forms.Form):
    from_date = forms.DateField(widget=DateInput)
    to_date = forms.DateField(widget=DateInput)


#(input_formats=['%d/%m/%Y'])('%d-%b-%Y')