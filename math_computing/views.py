from django.shortcuts import render
from django.http import JsonResponse
from .tasks import fibonacci
from asgiref.sync import sync_to_async

import random


# Create your views here.

def fib_test(request):
    number = random.randint(-10, 100) * 100

    result = fibonacci.apply_async([number])

    result_number = result.get(propagate=False)

    return render(request, 'test.html', {
        'number': number,
        'result_number': result_number if result.status == 'SUCCESS' else 'error'
    })
