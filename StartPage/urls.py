from django.urls import path
from . import views

urlpatterns = [
    path('', views.RegisterPage, name='home'),
    path('add_new/<str:book>/', views.add),
    path("send/<str:w>/", views.SendForm),
    path("test_all/<str:book>/", views.TestPage),
    path("give_word/<str:book>/", views.SendWord),
    path("check/<str:string>/", views.CheckTranslation),
    path("delete_from_db/<str:string>/", views.DeleteFromDB),
    path("library/", views.library, name='library'),
    path("library_add/<str:book>/", views.AddNewToLibrary),
    path("delete_book/<str:cur_id>/", views.DeleteBook),
    path("accounts/", views.RegisterPage),
    path("login/", views.LoginPage, name='Login'),
    path("register/", views.RegisterPage, name='register'),
    path("logout_here/", views.LogoutPage),
    path("add_error_reminder/", views.add_error_reminder),

    # path("test_all/", views.Test),
    # path("change_status/<str:status>/", views.ChangeStatus)

]

