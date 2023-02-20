from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.connect, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('signup', views.create_user, name="signup"),
    path('html', views.serve_msg),
    path('search', views.search, name='search_car'),
    path("add_car/<str:cid>", views.add_car, name='add_car'),
    path("edit_car/<int:cid>", views.edit_car, name='edit_car'),
    path("cars_list", views.serve_cars, name='cars_list'),
    path("car_list", views.CarsListView.as_view()),
    path("create_person", views.PersonCreationForm.as_view(),
         name="create_person"),

    path("update_person/<int:pk>", views.PersonUpdateView.as_view(),
         name="update_person"),
]
