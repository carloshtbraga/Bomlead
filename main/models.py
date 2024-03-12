from django.db import models
from .helpers import BR_STATES
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class Address(models.Model):
    city = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    state = models.CharField(max_length=2, choices=BR_STATES)

    def __str__(self):
        return f"{self.city}, {self.neighborhood}, {self.state}"


class Advertisement(models.Model):
    SITE_TYPES = (
        ("chavenamao", "Chave na Mão"),
        ("googlemaps", "Google Maps"),
    )
    FONTE_TYPES = (
        ("webscrapping", "Web Scrapping"),
        ("fake_lead", "Fake Lead"),
    )

    fonte = models.CharField(max_length=20, choices=FONTE_TYPES)
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    site = models.CharField(max_length=20, choices=SITE_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Person(models.Model):
    PERSON_TYPES = (
        ("corretor", "Corretor"),
        ("arquiteto", "Arquiteto"),
    )
    STATUS_CHOICES = (
        ("nao_responde", "Não Responde"),
        ("em_contato", "Em Contato"),
        ("pedido_espera", "Pedido em Espera"),
        ("nada_feito", "Nada Feito"),
    )
    FUNNEL_STAGES = (
        ("nao_qualificado", "Não Qualificado"),
        ("qualificado", "Qualificado"),
        ("conversa", "Conversa"),
        ("conversa_vendas", "Conversa de Vendas"),
        ("negociacao", "Negociação"),
        ("comprou", "Comprou"),
        ("nada_feito", "Nada Feito"),
    )
    email = models.EmailField(max_length=100, blank=True, null=True, unique=True)
    name = models.CharField(max_length=100, unique=True)
    person_type = models.CharField(
        max_length=20, choices=PERSON_TYPES, blank=True, null=True
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="nada_feito"
    )
    funnel_stage = models.CharField(
        max_length=20, choices=FUNNEL_STAGES, default="nada_feito"
    )
    number_of_sales = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Phone(models.Model):
    person = models.ForeignKey(
        "Person", on_delete=models.CASCADE, related_name="phones", blank=True, null=True
    )
    telefone = models.CharField(
        max_length=20,
        unique=True
    )  # Você pode ajustar o tamanho conforme necessário

    def __str__(self):
        return self.telefone

    def clean(self):
        # Verifica se já existe um telefone igual associado a outra pessoa
        if Phone.objects.exclude(pk=self.pk).filter(telefone=self.telefone).exists():
            raise ValidationError(
                "Este número de telefone já está em uso por outra pessoa."
            )


class Mobile(models.Model):
    person = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
        related_name="mobiles",
    )
    celular = models.CharField(
        max_length=20,
        unique=True
    )  # Você pode ajustar o tamanho conforme necessário

    def __str__(self):
        return self.celular

    def clean(self):
        # Verifica se já existe um celular igual associado a outra pessoa
        if Mobile.objects.exclude(pk=self.pk).filter(celular=self.celular).exists():
            raise ValidationError(
                "Este número de celular já está em uso por outra pessoa."
            )


class Sales(models.Model):
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    sale_description = models.TextField(max_length=200)
    sale_date = models.DateField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)  # Quantidade de leads vendidos
    lead_value = models.DecimalField(max_digits=10, decimal_places=2)  # Valor do lead

    def __str__(self):
        return f"Venda de {self.advertisement.title} para {self.person.name}"


class CustomUser(AbstractUser):
    # Adicione campos adicionais aqui, se necessário
    pass
