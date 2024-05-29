from .models import Ticker, News, Category
from django.utils import timezone

def ticker(_):
    today = timezone.now()

    Ticker.objects.filter(visible_date__lt=today).delete()
    
    try:
        return {"tickers": Ticker.objects.all()}
    except Ticker.DoesNotExist:
        Ticker.objects.create()
        return {"tickers": Ticker.objects.all()}
    

def news(_):
    return {"news_length": len(News.objects.all())}

def category(request):
    if request.path == "/":
        return {"categories": Category.objects.all()}
    return {}