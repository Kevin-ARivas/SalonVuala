# reportes/services.py

from agenda.models import Cita
from inventario.models import Producto
from finanzas.models import Venta
from django.db import transaction


def registrar_pago_cita(cita_id, metodo_pago="efectivo"):
    """
    Cuando se paga una cita:
    ✔ Cambia estado a confirmada
    ✔ Crea una venta automática
    ✔ Registra servicio realizado
    ✔ Descuenta productos si la cita usa productos asociados
    """

    with transaction.atomic():
        cita = Cita.objects.select_related("servicio", "cliente", "estilista").get(id=cita_id)

        # Cambiar estado
        cita.estado = "confirmada"
        cita.save()

        # Crear Venta
        venta = Venta.objects.create(
            total=cita.servicio.precio,
            metodo_pago=metodo_pago
        )

        return venta



def registrar_venta_producto(producto_id, cantidad, metodo_pago="efectivo"):
    """
    Venta directa desde Inventario
    ✔ Descuenta stock
    ✔ Crea venta con monto correcto
    """

    with transaction.atomic():
        producto = Producto.objects.get(id=producto_id)

        if producto.stock < cantidad:
            raise ValueError("No hay stock suficiente")

        # Descontar stock
        producto.stock -= cantidad
        producto.save()

        total = producto.precio * cantidad

        venta = Venta.objects.create(
            total=total,
            metodo_pago=metodo_pago
        )

        return venta



def dashboard_estilista(user):
    """
    Datos dinámicos para el panel del estilista:
    ✔ Servicios realizados
    ✔ Total generado
    ✔ Clientes atendidos
    ✔ Productos vendidos
    """

    citas = Cita.objects.filter(estilista=user, estado="confirmada")

    total_servicios = citas.count()
    total_generado = sum(c.servicio.precio for c in citas)

    clientes_atendidos = citas.values("cliente").distinct().count()

    return {
        "total_servicios": total_servicios,
        "total_generado": total_generado,
        "clientes_atendidos": clientes_atendidos,
    }
