from django.shortcuts import render, redirect
from food_service.forms import SignUpForm
from django.contrib.auth import login, authenticate

import food_service.database as db
import logging

logger = logging.getLogger('django')


def index(request):
    context = {
        'foods': db.get_foods()
    }

    if request.user.is_authenticated:
        username = request.user.username
        if request.method == 'POST':
            if 'food_id' in request.POST:
                food_id = request.POST['food_id']
                logger.info(food_id)
                db.add_to_cart(username, int(food_id))
            elif 'reset_cart' in request.POST:
                db.reset_cart(username)
            elif 'give_order' in request.POST:
                db.give_order(username, 'Kapıda Ödeme')
            elif 'comment' in request.POST:
                db.add_review(int(request.POST['order_id']), request.POST['comment'], request.POST['rating'])
                return redirect('/')

        cart_total = db.get_cart_total(username)
        context['cart_total'] = cart_total[0] if cart_total else 0
        orders = db.get_all_orders_of_user(username)
        orders_dict = {}
        for food_order in orders:
            if food_order[0] not in orders_dict:
                orders_dict[food_order[0]] = {
                    'total_price': food_order[1],
                    'order_date': food_order[2],
                    'review_comment': food_order[4],
                    'review_rating': food_order[5],
                    'foods': []
                }
            orders_dict[food_order[0]]['foods'].append(food_order[3])
        context['orders_dict'] = orders_dict
        total_spend = db.get_users_with_total_spendings(username)
        context['total_spend'] = total_spend[0] if total_spend else 0

    return render(request, 'index.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            address = form.cleaned_data.get('address')
            phone_number = form.cleaned_data.get('phone_number')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            db.create_user(user.id, username, address, phone_number)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})