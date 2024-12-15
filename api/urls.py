from django.urls import path
from .views import (ProcessDataAPIView, ProcessFilterAPIView, ProcessDurationAPIView)

urlpatterns = [
    path('process-data/', ProcessDataAPIView.as_view(), name='process-data'),
    path('filter-processes/', ProcessFilterAPIView.as_view(), name='filter-processes'),
    path('process-duration/', ProcessDurationAPIView.as_view(), name='process-duration'),
]
