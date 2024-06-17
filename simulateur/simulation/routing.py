from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/stocks/(?P<topic>\w+)/$', consumers.StockConsumer.as_asgi()),
]
