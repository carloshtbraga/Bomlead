from django.urls import path
from . import views

urlpatterns = [
    path("index/", views.index, name="index"),  # Página inicial
    path("create_person/", views.create_person, name="create_person"),
    path(
        "create_advertisement/", views.create_advertisement, name="create_advertisement"
    ),
    path("list_persons/", views.list_persons, name="list_persons"),
    path(
        "person_advertisements/<int:person_id>/",
        views.person_advertisements,
        name="person_advertisements",
    ),
    path("delete_person/<int:person_id>/", views.delete_person, name="delete_person"),
    path(
        "update_advertisement/<int:advertisement_id>/",
        views.update_advertisement,
        name="update_advertisement",
    ),
    path(
        "advertisement/<int:advertisement_id>",
        views.delete_advertisement,
        name="delete_advertisement",
    ),
    path("sales/", views.all_sales, name="all_sales"),
    path("all_company_sales/", views.all_company_sales, name="all_company_sales"),
    path("create_sale/", views.create_sale, name="create_sale"),
    path("grafico_person_type/", views.grafico_person_type, name="grafico_person_type"),
    path(
        "grafico_person_type_data/",
        views.grafico_person_type_data,
        name="grafico_person_type_data",
    ),
    path(
        "grafico-status-person/",
        views.grafico_status_person,
        name="grafico_status_person",
    ),
    path(
        "grafico_status_person/",
        views.grafico_status_person,
        name="grafico_status_person",
    ),
    path(
        "grafico_advertisement_from_where/",
        views.grafico_advertisement_from_where,
        name="grafico_advertisement_from_where",
    ),  # Você esqueceu de fechar o parêntese nesta linha
    path("", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
]
