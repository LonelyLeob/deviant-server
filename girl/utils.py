from django.contrib.gis.geoip2 import GeoIP2


def geo(request):
    x_forwarded_for: str = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip: str = x_forwarded_for.split(',')[0]
    else:
        ip: str = request.META.get('REMOTE_ADDR')
    if ip == "127.0.0.1":
            return "Moscow"
    geocoder = GeoIP2()
    return geocoder.city(ip)['city']

# def simple(_):
#     return "123"

func_table = {
    "geo": geo,
    # "additional": simple
}