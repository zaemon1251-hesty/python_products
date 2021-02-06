from django import forms
from .models import Kakeibo

class KakeiboForm(forms.ModelForm):
    """
    新規データ登録画面用のフォーム定義
    """
    class Meta:
        model = Kakeibo
        fields =['date', 'category', 'money', 'memo']

    def clean(self):
        if not self.is_valid():
            return self.cleaned_data
            
        if not self.cleaned_data["momey"]:
            raise forms.ValidationError(
                "金額を入力してください")
        return self.cleaned_data