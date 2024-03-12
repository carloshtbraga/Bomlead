# import os
# import django
# import csv
# from datetime import datetime
# from django.utils.timezone import make_aware

# # Configurar as configurações do Django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
# django.setup()

# from main.models import Person, Address, Phone, Mobile, Advertisement

# # Importar os modelos após a configuração do Django


# def import_csv(filename):
#     with open(filename, "r") as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             # Criar ou obter o endereço (Address)
#             address, _ = Address.objects.get_or_create(
#                 city=row["city"], state=row["state"], neighborhood=row["district"]
#             )

#             # Criar a pessoa (Person)
#             person, _ = Person.objects.get_or_create(
#                 name=row["name"],
#                 email=row["email"],
#                 created_at=make_aware(datetime.now()),  # Adicione a data de criação
#                 updated_at=make_aware(datetime.now()),  # Adicione a data de atualização
#             )

#             # Se houver um telefone no CSV, associá-lo à pessoa
#             if row["phone"]:
#                 phone, _ = Phone.objects.get_or_create(
#                     telefone=row["phone"], person=person
#                 )

#             # Se houver um celular no CSV, associá-lo à pessoa
#             if row["mobile"]:
#                 mobile, _ = Mobile.objects.get_or_create(
#                     celular=row["mobile"], person=person
#                 )

#             # Criar o anúncio (Advertisement) associado à pessoa e ao endereço
#             advertisement = Advertisement.objects.create(
#                 person=person,
#                 title=row["name"],
#                 fonte="webscrapping",  # Defina a fonte de acordo com os dados do CSV
#                 site="chavenamao",  # Defina o site de acordo com os dados do CSV
#                 price=0,  # Defina o preço de acordo com os dados do CSV
#                 address=address,
#             )


# # Caminho do arquivo CSV
# csv_path = "1709747996309.csv"

# # Chamar a função import_csv com o caminho do arquivo CSV
# import_csv(csv_path)
