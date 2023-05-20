from django.urls import path

from django.contrib.auth import views as auth_views
from .views import loginPage, asset_update
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('registerassets/', views.registerassets, name="registerassets"),

    path('asset/<int:pk>/update/', views.asset_update, name='asset_update'),
   
    #path('updateAsset/<str:pk>/', views.updateAsset, name="updateAsset"),
    #path('updateVendor/<int:pk>/', views.updateVendor, name="updateVendor"),
    path('deleteAsset/<str:pk>/', views.deleteAsset, name="deleteAsset"),
    
    path('account/', views.accountSettings, name="account"),
    path('superprofile/', views.accountSuperSettings, name="superprofile"),

    path('users/', views.userPage, name="user-page"),
    path('table/', views.table, name="table"),
   
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    path('userdetails/', views.userDetails, name="userdetails"),
    path('userdetails/<int:employee_id>', views.userDetails, name="userdetails"),
    
    #### Reports #####
    path('employeereport/', views.employeeReport, name="employee-report"),
    path('vendorreport/', views.vendorReport, name="vendor-report"),
    path('assetreport/', views.assetReport, name="asset-report"),

    
]