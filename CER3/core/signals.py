from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from core.models import RegistroProduccion, RegistroAuditoria  # Ajusta esto a tu estructura de proyecto

@receiver(pre_delete, sender=RegistroProduccion)
def log_delete_action(sender, instance, **kwargs):
    # Obtener el usuario que está realizando la eliminación
    user_id = None
    try:
        session = Session.objects.latest('expire_date')
        user_id = session.get_decoded().get('_auth_user_id')
    except Session.DoesNotExist:
        pass

    if user_id:
        user = User.objects.get(id=user_id)
        detalle = (f"Eliminación del registro de producción: "
                   f"Combustible: {instance.combustible.nombre}, "
                   f"Operador: {instance.operador.username}, "
                   f"Litros producidos: {instance.litros_producidos}.")
        RegistroAuditoria.objects.create(
            usuario=user,
            registro_produccion_id=instance.id,
            detalle=detalle
        )

