from .models import Ads, News

def ads(_):
    try:
        return {"ads": Ads.objects.get(id=1)}
    except Ads.DoesNotExist:
        ads = Ads.objects.create()
        return {"ads": ads}
    

def news(_):
    return {"news_length": len(News.objects.all())}