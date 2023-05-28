from celery import shared_task

from apps.payments.models import ServicePlanPayment


@shared_task
def update_all_service_plan_status():
    spp = ServicePlanPayment.objects.all()

    for obj in spp:
        obj.update_service_plan_status()

    return ServicePlanPayment.objects.bulk_update(spp, ['service_plan_status'])
