from .models import Ads, News, Category

def ads(_):
    try:
        return {"ads": Ads.objects.get(id=1)}
    except Ads.DoesNotExist:
        ads = Ads.objects.create()
        return {"ads": ads}
    

def news(_):
    return {"news_length": len(News.objects.all())}

def category(request):
    if request.path == "/":
        return {"categories": Category.objects.all()}
    return {}