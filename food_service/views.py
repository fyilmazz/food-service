from django.shortcuts import render
import food_service.database as db
import logging

logger = logging.getLogger(__name__)


def index(request):
    logger.info("test")
    print(db.get_reviews_with_usernames())
    context = {
        'foods': db.get_foods()
    }

    return render(request, 'index.html', context)