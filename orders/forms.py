from django import forms
import json
from .models import Order

class OrderForm(forms.ModelForm):
    """
    Форма для создания и редактирования заказа. Включает поля: номер стола, состав заказа, общая стоимость, статус. 
    """
    class Meta:
        model = Order
        fields = ['table_number', 'items', 'status']
        widgets = {
            'status': forms.Select(choices=Order.STATUS_CHOICE)
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk:
            # Загружаем существующий список блюд в читаемом формате
            try:
                self.fields['items'].initial = json.dumps(self.instance.items, ensure_ascii=False)
            except json.JSONDecodeError:
                self.fields['items'].initial = "[]"
        
        # Если это новый заказ (то есть его ещё нет в БД), устанавливаем 'pending'
        else:
            # Для нового заказа – устанавливаем значения по умолчанию
            self.fields['status'].initial = 'pending'

    def clean_items(self):
        data = self.cleaned_data.get('items', '[]')
        
       
        # Если данные уже список (при редактировании)
        if isinstance(data, list):
            return json.dumps(data)
        
        try:
        # Если данные в виде строки JSON 
            items = json.loads(data)
            return self.validate_items(items)
        except json.JSONDecodeError:
            raise forms.ValidationError("Некорректный JSON-формат")
    
    def validate_items(self, items):
        """Валидация списка блюд"""
        if not isinstance(items, list):
            raise forms.ValidationError("Должен быть список блюд")
            
        for index, item in enumerate(items, 1):
            if not isinstance(item, dict):
                raise forms.ValidationError(f"Блюдо #{index} должно быть объектом")
                
            if 'name' not in item or 'price' not in item:
                raise forms.ValidationError(f"Блюдо #{index} должно содержать 'name' и 'price'")
                
            try:
                price = float(item['price'])
                if price <= 0:
                    raise forms.ValidationError(f"Цена в блюде #{index} должна быть больше нуля")
            except (TypeError, ValueError):
                raise forms.ValidationError(f"Некорректная цена в блюде #{index}")
    
        return items
