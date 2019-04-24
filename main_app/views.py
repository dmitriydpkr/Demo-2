from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import Good, Order
from django.template import loader

from .forms import OrderForm
from django.http import HttpResponseRedirect
from django.urls import reverse


def home(request):
    return render(request, 'main_app/category.html', {
        'list_goods': 0
    })


def good_detail(request, good_id):

    good = get_object_or_404(Good, id=good_id)
    list_order = Order.objects.all()[:6]

    form = OrderForm(request.POST or None, initial={  # данные, корорые будут переданы форме
        'good': good
    })

    if request.method == 'POST':

        if form.is_valid():
            form.save()
            # перезагрузка товара для очистки данных и получение подтверждения заказа
            return HttpResponseRedirect('{}?sent=True'.format(reverse('good-detail', kwargs={'good_id': good.id})))

    return render(request, 'main_app/good_detail.html', {
        'good': good,
        'form': form,
        'sent': request.GET.get('sent', False),  # передаем в шаблон false в редирект,
        'list_order': list_order

    })

