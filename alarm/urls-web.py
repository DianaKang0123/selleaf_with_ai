from django.urls import path

from alarm.views import AlarmView, AlarmAPI

app_name = 'alarm'

urlpatterns = [
    # 알람 목록 뷰 및 API
    path('main/', AlarmView.as_view()),
    path('show/main/<int:page>', AlarmAPI.as_view()),  # 특정 페이지의 알람을 보여주는 API
    path('update/', AlarmAPI.as_view()),  # 알람을 읽은 상태로 업데이트하는 API
    path('remove/', AlarmAPI.as_view())   # 모든 알람을 읽은 상태로 변경하는 API
]
