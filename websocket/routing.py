
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from .consumers import Consumer



# websocket_urlpatterns = [
#     path('ws/hello/', Consumer.as_asgi()),
# ]

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter([
#             path("/ws/hello", Consumer.as_asgi()),
#             # 添加其他 WebSocket 路由
#             # websocket_urlpatterns
#         ])
#     ),
# })

# backend/websocket/routing.py

# from django.urls import path
# from .consumers import Consumer

# websocket_urlpatterns = [
#     path('ws/hello/', Consumer.as_asgi()),
#     # 添加其他 WebSocket 路由
# ]

from django.urls import path
from .consumers import Consumer

websocket_urlpatterns = [
    path('ws/hello/', Consumer.as_asgi()),
]