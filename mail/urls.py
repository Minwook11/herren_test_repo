from django.urls import path

from .views import (
    SubscribeView,
    UnsubscribeView,
    SendView,
    ListView,
)

urlpatterns = [
    path('/subscribe', SubscribeView.as_view()),
    path('/unsubscribe', UnsubscribeView.as_view()),
    path('/send', SendView.as_view()),
    path('/list', ListView.as_view()),
]
