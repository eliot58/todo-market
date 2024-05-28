from .models import Ticker, News, Category

def ticker(_):
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