from django.urls import path, include


app_name = "api"

urlpatterns = [
    path('v1/', include('mini_wallet.api.v1.urls'))
]
