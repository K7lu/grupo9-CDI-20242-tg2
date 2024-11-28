from .models import Client

def create_client(name, cnpj, address, phone):
    client = Client(
        name=name,
        cnpj=cnpj,
        address=address,
        phone=phone
    )
    client.save()
    return client

def get_client_by_cnpj(cnpj):
    try:
        client = Client.objects.get(cnpj=cnpj)
        return client
    except Client.DoesNotExist:
        return None

def get_all_clients():
    return Client.objects.all()
