from django.urls import path
from .. import views
from rest_framework_simplejwt.views import TokenRefreshView
from ..custom import views as custom_views


urlpatterns = [
    # authentication patterns
    path('register/', views.RegisterView.as_view(),),
    path('register/seller', views.RegisterSellerView.as_view(),),
    path('login/', custom_views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('enable-seller-status/', views.EnableSellerStatusView.as_view(), ),

    # change password patterns
    path('change_password/', views.ChangePasswordView.as_view(),),
    path('reset_password/send/', views.ResetPasswordSendTokenView.as_view(),),
    path('reset_password/check/<str:token>', views.ResetPasswordCheckTokenView.as_view(),),

    
]
