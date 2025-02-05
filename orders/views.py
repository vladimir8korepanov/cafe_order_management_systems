from django.shortcuts import render, get_object_or_404, redirect
from .models import Order
from .forms import OrderForm
from django.db.models import Sum


def order_list(request):
    """
    Список всех заказов. Заказы отсортированы по времени создания(новые сверху)    
    """
    orders = Order.objects.all().order_by('-created_at') # Получаем все заказы, сортируя их по дате создания
    return render(request, 'orders/order_list.html', {'orders': orders})

def order_detail(request, order_id):
    """
    Отображение деталей заказа по ID. 
    Информация о столе, статусе, общей стоимости и состав заказа.
    """
    order = get_object_or_404(Order, id=order_id) # Детали конктретного заказа
    return render(request, 'orders/order_detail.html', {'order': order})

def order_create(request):
    """
    Создание нового заказа. Если форма прошла валидацию, закакз сохраняется в БД.
    При GET-запросе отображается пустая форма.
    При POST-запросе данные формы проверяются и сохраняются.
    """
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid(): # Если форма валидна
            form.save() # Сохраняем заказ в БД
            return redirect('order_list')        
    else: 
        form = OrderForm() # Если GET-запрос, создаем пустую форму
            
    return render(request, 'orders/order_form.html', {'form': form})

def order_edit(request, order_id):
    """
    Редактирование существующего заказа
    """
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order) # Создаем форму с данными из запроса и текущим заказом
        if form.is_valid():
            form.save()
            return redirect('order_list')
            
    else:
        form = OrderForm(instance=order)
    
    return render(request, 'orders/order_form.html', {'form': form, 'order': order})
    

def order_delete(request, order_id):
    """
    Удаление заказа. После удаления пользователь перенаправляется на список заказов.
    """
    order = get_object_or_404(Order, id=order_id) 
    
    if request.method == 'POST':
        order.delete() # Удаляем заказ из базы данных
        return redirect('order_list')
    
    return render(request, 'orders/order_confirm_delete.html', {'order': order})

def revenue_view(request):
    """Вычисление выручки за все оплаченные заказы. Для подсчета используется агрегация """
    total_revenue = Order.objects.filter(
        status='paid'
    ).aggregate(total=Sum('total_price'))['total'] or 0 # Фильтруем только оплаченные заказы и считаем сумму их стоимости
    
    return render(request, 'orders/revenue.html', {'total_revenue': total_revenue}) 


