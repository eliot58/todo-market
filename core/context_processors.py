from .models import Ads

def ads(_):
    try:
        return {"ads": Ads.objects.get(id=1)}
    except Ads.DoesNotExist:
        ads = Ads.objects.create()
        return {"ads": ads}