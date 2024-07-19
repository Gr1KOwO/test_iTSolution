from django import forms
from .models import Video

class VideoSettingsForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = [
            'title', 'text', 'duration', 'resolution', 'background_color', 
            'font_color', 'font_scale', 'thickness', 'include_stripe', 'stripe_color'
        ]
        widgets = {
            'background_color': forms.TextInput(attrs={'type': 'color'}),
            'font_color': forms.TextInput(attrs={'type': 'color'}),
            'stripe_color': forms.TextInput(attrs={'type': 'color'}),
            'text': forms.Textarea(),
        }
        labels = {
            'title': 'Название файла',
            'text': 'Текст видео',
            'duration': 'Время (в секундах)',
            'resolution': 'Разрешение (1920x1080)',
            'background_color': 'Цвет фона',
            'font_color': 'Цвет для текста',
            'font_scale': 'Размер шрифта для текста',
            'thickness': 'Толщина текста',
            'include_stripe': 'Фон для текста',
            'stripe_color': 'Цвет фона для текста',
        }

    def clean_duration(self):
        duration = self.cleaned_data.get('duration')
        if duration > 10:  # Ограничение на продолжительность видео в 10 секунд
            raise forms.ValidationError("Продолжительность видео не может превышать 10 секунд.")
        return duration

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.title:
            instance.title = instance.text[:25]
        if commit:
            instance.save()
        return instance