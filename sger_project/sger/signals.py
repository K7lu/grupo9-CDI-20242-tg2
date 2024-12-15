from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.apps import apps

@receiver(post_migrate)
def create_default_groups(sender, **kwargs): 
    """
    Cria os grupos padrão 'Master', 'Cliente', 'Funcionario' e 'Administradores'
    automaticamente após a migração e atribui permissões específicas.
    """
    # Grupos padrão
    grupos = ["Master", "Cliente", "Funcionario", "Administradores"]

    # Permissões específicas para cada grupo
    permissoes_grupos = {
        "Master": Permission.objects.all(),  # Master tem todas as permissões
        "Cliente": [],  # Adicione permissões específicas para Clientes
        "Funcionario": [],  # Adicione permissões específicas para Funcionários
        "Administradores": [],
    }

    # Atribui permissões de gerenciamento de usuários ao grupo Administradores
    try:
        user_model = apps.get_model("auth", "User")
        content_type = ContentType.objects.get_for_model(user_model)
        permissoes_grupos["Administradores"] = Permission.objects.filter(
            content_type=content_type,
            codename__in=["add_user", "change_user", "delete_user", "view_user"]
        )
    except Exception as e:
        print(f"Erro ao buscar permissões para Administradores: {e}")

    # Cria os grupos e atribui as permissões
    for grupo in grupos:
        group, created = Group.objects.get_or_create(name=grupo)
        if created:
            print(f"Grupo '{grupo}' criado com sucesso!")
        else:
            print(f"Grupo '{grupo}' já existia.")

        # Atribuição de permissões ao grupo
        if permissoes_grupos.get(grupo):
            try:
                group.permissions.set(permissoes_grupos[grupo])
                group.save()
                print(f"Permissões atribuídas ao grupo '{grupo}'.")
            except Exception as e:
                print(f"Erro ao atribuir permissões ao grupo '{grupo}': {e}")
