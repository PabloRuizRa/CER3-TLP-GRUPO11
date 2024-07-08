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

@receiver(pre_save, sender=RegistroProduccion)
def log_update_action(sender, instance, **kwargs):
    if instance.pk:  # Solo si el registro ya existe (es una actualización)
        original = RegistroProduccion.objects.get(pk=instance.pk)
        if original.operador == instance.operador:  # Asegurarse de que el operador que modifica es el mismo que creó el registro
            user = instance.operador  # Obtener el operador que creó el registro
            detalle = f"Modificación del registro de producción del operador {instance.operador.username} con ID {instance.id}."
            RegistroAuditoria.objects.create(
                usuario=user,
                registro_produccion=instance,
                accion='MODIFICACION',
                detalle=detalle
            )