import os
import django
import pandas as pd
from django.utils.timezone import make_aware
from django.db.utils import IntegrityError
from decimal import Decimal
from decimal import InvalidOperation

# Configurar as configurações do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
django.setup()

from main.models import Person, Address, Phone, Mobile, Advertisement

# Supondo que o arquivo Excel tenha o nome 'dados.xlsx' e está na mesma pasta do script
excel_file = "rj_planilha_geral.xlsx"
total_repetidos = 0
total_unicos = 0
total_telefones_repetidos = 0
# Carregando os dados do Excel em um DataFrame do pandas


def convert_to_decimal(value):
    try:
        return Decimal(value.replace('.', ''))
    except InvalidOperation:
        return Decimal('0.0')
    
    
try:
    df = pd.read_excel(excel_file)
except FileNotFoundError:
    print(f"Arquivo '{excel_file}' não encontrado.")
    exit()

# Iterando sobre as linhas do DataFrame
for index, row in df.iterrows():
    try:
        # Criando e salvando o objeto Person
        person = Person.objects.create(
            name=row["Nome"],
            person_type="corretor",  # Definindo o tipo de pessoa como corretor
        )

        # Criando e salvando o objeto Phone, se houver número de telefone fixo na planilha
        try:
            if not pd.isnull(row["Telefone Fixo"]):
                phone = Phone.objects.create(
                    person=person, telefone=row["Telefone Fixo"]
                )
        except Exception as e:
            total_telefones_repetidos += 1
            print(f"Erro ao criar ou pegar telefone fixo: {e}")
        try:
            if not pd.isnull(row["Celular"]):
                mobile = Mobile.objects.create(person=person, celular=row["Celular"])
        except Exception as e:
            total_telefones_repetidos += 1
            print(f"Erro ao criar ou pegar telefone celular: {e}")
        # Criando o endereço
        try:
            address = Address.objects.create(
                neighborhood=row["Bairro Principal"],
                city=row["Cidade"],
                state=row["Estado"],
            )
        except Exception as e:
            print(f"Erro ao criar ou pegar endereço: {e}")
        # Criando e salvando o objeto Advertisementq

        try:
            advertisement = Advertisement.objects.create(
                fonte=row["Fonte"],
                person=person,
                title=(
                    row["Título do Anúncio"]
                    if pd.notnull(row["Título do Anúncio"])
                    else "Sem Título"
                ),
                site=row["Site"],
                price=convert_to_decimal(row["Valor do Anúncio"]) if pd.notnull(row["Valor do Anúncio"]) else Decimal('0.0'),
                address=address,
                # Adicione outros campos conforme necessário
            )

            # Exibindo uma mensagem de sucesso para cada registro processado
            print(f"Registro {index + 1} importado com sucesso.")
            total_unicos += 1
        except Exception as e:
            print(f"Erro ao criar ou pegar Anúncio: {e}")
    except IntegrityError as e:
        total_repetidos += 1
        print(f"Erro de integridade ao tentar cadastrar o registro {index + 1}: {e}")
    except Exception as e:
        print(f"Erro ao processar o registro {index + 1}: {e}")

print("Importação concluída.")
print("Total de repetidos:", total_repetidos)
print("Total de registros únicos:", total_unicos)
print("Total de telefones repetidos:", total_telefones_repetidos)
