from django.urls import path
from .. import views

urlpatterns = [
    path('profile/', views.ProfileView.as_view(),),
    path('profile/<str:email>', views.ProfileView.as_view(),),
    path('user_list/', views.UserListView.as_view(),),
    path('sellers/', views.SellerListView.as_view()),
    path('products/', views.ProductListVIew.as_view(), ),
    path('product/', views.ProductDetaliView.as_view(), ),
    path('shop/', views.ShopView.as_view(), )
]
