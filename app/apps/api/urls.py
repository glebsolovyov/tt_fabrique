from django.urls import path
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

from apps.api.views import *

urlpatterns = [
    path('schema', SpectacularAPIView.as_view(), name='schema'),
    path('docs', SpectacularSwaggerView.as_view(url_name='schema')),

    path('mailing/<int:pk>', MailingAPIView.as_view(), name='mailing'),
    path('mailing/create', MailingCreateAPIView.as_view(), name='mailing_create'),
    path('mailing/statistics', MailingStatisticsAPIView.as_view(), name='mailing_statistics'),
    path('mailing/statistics/detailed', MailingDetailedStatisticsAPIView.as_view(), name='mailing_detailed_statistics'),

    path('client/<int:pk>', ClientAPIView.as_view(), name='client'),
    path('client/create', ClientCreateAPIView.as_view(), name='client_create'),

    path('message/<int:pk>', MessageAPIView.as_view(), name='message'),
    path('message/create', MessageCreateAPIView.as_view(), name='message_create'),
    path('message/send/<int:pk>', SendMessageToClientAPIView.as_view(), name='message_send'),
]
