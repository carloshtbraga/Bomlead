from .models import Person, Address, Advertisement, Sales, Phone, Mobile
from .forms import (
    PersonForm,
    AddressForm,
    AdvertisementForm,
    PersonUpdateForm,
    SaleForm,
    CustomAuthenticationForm,
    CustomUserCreationForm,
    MobileForm,
    PhoneForm,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

# import matplotlib.pyplot as plt
# from django.http import HttpResponse
from django.db.models import Count
from django.http import JsonResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required, user_passes_test


def is_comercial_group(user):
    return user.groups.filter(name="Comercial").exists()


# @user_passes_test(is_comercial_group)
# @login_required
def index(request):
    total_sales = Sales.objects.count()
    total_advertisements = Advertisement.objects.count()
    total_person = Person.objects.count()
    total_arquiteto = Person.objects.filter(person_type="arquiteto").count()
    total_corretor = Person.objects.filter(person_type="corretor").count()
    return render(
        request,
        "index.html",
        {
            "total_sales": total_sales,
            "total_advertisements": total_advertisements,
            "total_person": total_person,
            "total_arquiteto": total_arquiteto,
            "total_corretor": total_corretor,
        },
    )


def create_person(request):
    if request.method == "POST":
        person_form = PersonForm(request.POST)
        phone_form = PhoneForm(request.POST)
        mobile_form = MobileForm(request.POST)

        if person_form.is_valid() and phone_form.is_valid() and mobile_form.is_valid():
            person = person_form.save()
            phone = phone_form.save(commit=False)
            phone.person = person
            phone.save()
            mobile = mobile_form.save(commit=False)
            mobile.person = person
            mobile.save()
            return redirect(
                "index"
            )  # Redirecionar para a página inicial após a criação do Person
    else:
        person_form = PersonForm()
        phone_form = PhoneForm()
        mobile_form = MobileForm()

    return render(
        request,
        "create_person.html",
        {
            "person_form": person_form,
            "phone_form": phone_form,
            "mobile_form": mobile_form,
        },
    )


def create_advertisement(request):
    if request.method == "POST":
        advertisement_form = AdvertisementForm(request.POST)
        address_form = AddressForm(request.POST)
        if advertisement_form.is_valid() and address_form.is_valid():
            address = address_form.save()  # Salve primeiro o endereço
            advertisement = advertisement_form.save(commit=False)
            advertisement.address = address  # Associe o endereço ao anúncio
            advertisement.save()  # Salve o anúncio
            return redirect("index")
    else:
        advertisement_form = AdvertisementForm()
        address_form = AddressForm()
    return render(
        request,
        "create_advertisement.html",
        {"advertisement_form": advertisement_form, "address_form": address_form},
    )


def list_persons(request):
    query = request.GET.get("q")

    if query:
        persons = (
            Person.objects.filter(
                Q(name__icontains=query)
                | Q(email__icontains=query)
                | Q(person_type__icontains=query)
                | Q(phones__telefone__icontains=query)
                | Q(mobiles__celular__icontains=query)
            )
            .distinct()
            .order_by("name")
        )  # Ordenar os resultados pelo nome
        person_count = persons.count()
    else:
        persons = Person.objects.all().order_by(
            "name"
        )  # Ordenar todos os resultados pelo nome
        person_count = persons.count()

    return render(
        request,
        "list_persons.html",
        {
            "persons": persons,
            "person_count": person_count,
        },
    )


def person_advertisements(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    advertisements = person.advertisement_set.all()

    if request.method == "POST":
        person_form = PersonUpdateForm(request.POST, instance=person)
        phone_form = PhoneForm(request.POST)
        mobile_form = MobileForm(request.POST)

        if person_form.is_valid() and phone_form.is_valid() and mobile_form.is_valid():
            person = person_form.save()
            telefone = phone_form.cleaned_data.get("telefone")
            celular = mobile_form.cleaned_data.get("celular")

            if telefone:  # Verifica se um telefone foi fornecido
                Phone.objects.create(person=person, telefone=telefone)

            if celular:  # Verifica se um celular foi fornecido
                Mobile.objects.create(person=person, celular=celular)

            return redirect("person_advertisements", person_id=person_id)
    else:
        person_form = PersonUpdateForm(instance=person)
        phone_form = PhoneForm()
        mobile_form = MobileForm()

    return render(
        request,
        "person_advertisements.html",
        {
            "person": person,
            "advertisements": advertisements,
            "person_form": person_form,
            "phone_form": phone_form,
            "mobile_form": mobile_form,
        },
    )


def delete_person(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    if request.method == "POST":
        person.delete()
    return redirect("list_persons")


def update_advertisement(request, advertisement_id):
    advertisement = get_object_or_404(Advertisement, pk=advertisement_id)
    if request.method == "POST":
        form = AdvertisementForm(request.POST, instance=advertisement)
        if form.is_valid():
            form.save()
            return redirect(
                "index"
            )  # Redirecione para onde desejar após a atualização do anúncio
    else:
        form = AdvertisementForm(instance=advertisement)
    return render(
        request,
        "update_advertisement.html",
        {"form": form, "advertisement": advertisement},
    )


def delete_advertisement(request, advertisement_id):
    advertisement = get_object_or_404(Advertisement, pk=advertisement_id)
    if request.method == "POST":
        advertisement.delete()
        return redirect(
            "index"
        )  # Redirecione para onde desejar após a exclusão do anúncio
    return render(
        request, "delete_advertisement.html", {"advertisement": advertisement}
    )


def all_sales(request):
    # Obtenha o usuário logado
    user = request.user

    # Filtrar as vendas para mostrar apenas as vendas do usuário logado
    sales = Sales.objects.filter(user=user)

    # Crie o formulário de venda
    form = SaleForm()

    # Calcule o valor total de leads
    total_lead_value = sum(sale.quantity * sale.lead_value for sale in sales)

    # Adicione o total de cada venda
    for sale in sales:
        sale.total = sale.quantity * sale.lead_value

    return render(
        request,
        "all_sales.html",
        {"sales": sales, "form": form, "total_lead_value": total_lead_value},
    )


def create_sale(request):
    if request.method == "POST":
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)  # Não salva no banco de dados ainda
            person = form.cleaned_data["person"]
            person.number_of_sales += 1
            person.save()  # Salva a atualização do número de vendas da pessoa
            sale.save()  # Salva a venda no banco de dados
            return redirect("all_sales")
    else:
        form = SaleForm()
    return render(request, "create_sale.html", {"form": form})


def grafico_person_type(request):
    return render(request, "grafico_person_type.html")


def grafico_person_type_data(request):
    # Consulta para contar o número de pessoas para cada tipo de person_type
    person_types_count = Person.objects.values("person_type").annotate(
        total=Count("id")
    )

    # Extrair dados para o gráfico
    person_types = [entry["person_type"] for entry in person_types_count]
    counts = [entry["total"] for entry in person_types_count]

    # Formatar os dados para Plotly
    data = {"person_types": person_types, "counts": counts}

    # Retornar os dados como uma resposta JSON
    return JsonResponse(data)


def grafico_status_person(request):
    # Consulta para contar o número de pessoas para cada status
    status_count = Person.objects.values("status").annotate(total=Count("id"))

    # Extrair dados para o gráfico
    status_labels = [entry["status"] for entry in status_count]
    counts = [entry["total"] for entry in status_count]

    # Passar os dados para o template
    return render(
        request,
        "grafico_status_person.html",
        {
            "status_labels": status_labels,
            "counts": counts,
        },
    )


def grafico_advertisement_from_where(request):
    # Consulta para contar o número de anúncios para cada local de origem
    from_where_count = Advertisement.objects.values("fonte").annotate(total=Count("id"))

    # Extrair dados para o gráfico
    from_where_labels = [entry["fonte"] for entry in from_where_count]
    counts = [entry["total"] for entry in from_where_count]

    # Passar os dados para o template
    return render(
        request,
        "grafico_advertisement_from_where.html",
        {
            "from_where_labels": from_where_labels,
            "counts": counts,
        },
    )


class CustomLoginView(LoginView):
    template_name = "login.html"
    authentication_form = CustomAuthenticationForm


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("index")


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"


def all_company_sales(request):
    sales = Sales.objects.all()
    form = SaleForm()
    total_lead_value = sum(sale.quantity * sale.lead_value for sale in sales)
    for sale in sales:
        sale.total = (
            sale.quantity * sale.lead_value
        )  # Adicionando a criação do formulário aqui
    return render(
        request,
        "all_company_sales.html",
        {"sales": sales, "form": form, "total_lead_value": total_lead_value},
    )
