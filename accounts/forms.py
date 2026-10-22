from decimal import Decimal

from django import forms


class AddMoneyForm(forms.Form):
    amount = forms.DecimalField(
        min_value=Decimal("1.00"),
        max_value=Decimal("100000.00"),
        max_digits=10,
        decimal_places=2,
    )