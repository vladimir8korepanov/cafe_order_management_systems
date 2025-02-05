from django.db import models 
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.utils.timezone import now
import json

class Order(models.Model):
    """
    Модель заказа.
    Содержит информацию о номере стола, составе заказа, общей стоимости и статусе.
    """
    STATUS_CHOICE = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]
    
    id = models.AutoField(primary_key=True) # Уникальный ID заказа
    table_number = models.IntegerField(verbose_name='Номер стола') # Номер стола клиента
    items = models.JSONField(verbose_name='Заказанные блюда', default=list) # Список блюд в формате JSON
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Общая стоимость', default=0.00    
    ) # Общая стоимость заказа
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICE, default='pending', verbose_name='Статус'
    ) # Текущий статус заказа
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан') # Дата и время создания заказа
    
    class Meta: 
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
    
    def save(self, *args, **kwargs):
        """Пересчитываем общую соимость перед сохранением"""
        
        if isinstance(self.items, str): # Если items — строка JSON
            try:
                self.items = json.loads(self.items) # Преобразуем строку в Python-объект
            except json.JSONDecodeError:
                raise ValidationError('Некорректный формат данных в items')
        
        if not isinstance(self.items, list): # Проверяем, что items — список
            raise ValidationError('Поле "items" должно содержать список блюд.')
    
        if not self.items: # Если список пустой
            self.total_price = 0.00
        else:
    
            try:
                # Считаем сумму цен всех блюд
                self.total_price = sum(float(item.get('price', 0)) for item in self.items)
            except (TypeError, ValueError):
                raise ValidationError('Ошибка в данных "items": цена должна быть числом')
        
        super().save(*args, **kwargs) # Вызываем родительский метод 
        
    def __str__(self):
        return f"Заказ {self.id} (Стол {self.table_number})" 
    
    def revenue_today(cls):
        """Выручка за день"""
        return cls.objects.filter(
            status='paid',
            created_at__date=now().date()
        ).aggregate(Sum('total_price'))['total_price_sum'] or 0
        
    def get_items_display(self):
        """Возвращаем список блюд в читаемом формате"""
        return ", ".join(f"{item.get('name', 'Неизвестное блюдо')} x{item.get('quantity', 1)}" for item in self.items)
    
    def is_paid(self):
        return self.status == 'paid'