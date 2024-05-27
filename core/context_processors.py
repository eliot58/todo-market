from .models import Ticker, News, Category

def ticker(_):
    try:
        return {"ticker": Ticker.objects.get(id=1)}
    except Ticker.DoesNotExist:
        ticker = Ticker.objects.create()
        return {"ticker": ticker}
    

def news(_):
    return {"news_length": len(News.objects.all())}

def category(request):
    if request.path == "/":
        return {"categories": Category.objects.all()}
    return {}