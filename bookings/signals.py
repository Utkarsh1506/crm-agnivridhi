from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Booking


# DISABLED: Booking revenue aggregation is disabled for now
# Revenue tracking uses Client-level fields which are updated via:
# 1. Client creation/edit forms
# 2. Payment records (which update client.received_amount)
# 
# This ensures existing clients with manual revenue entries are not affected

# @receiver(post_save, sender=Booking)
# def update_client_revenue_on_booking_save(sender, instance, created, **kwargs):
#     """
#     Update client's aggregated revenue whenever a booking is created or updated.
#     Only updates if the booking has revenue data (pitched_amount > 0).
#     """
#     if instance.client and instance.pitched_amount > 0:
#         # Recalculate and update client revenue from all bookings
#         instance.client.calculate_aggregated_revenue()
#         # Save without triggering the client's save() method's own calculations
#         # to avoid recursion
#         from clients.models import Client
#         Client.objects.filter(pk=instance.client.pk).update(
#             total_pitched_amount=instance.client.total_pitched_amount,
#             gst_amount=instance.client.gst_amount,
#             gst_percentage=instance.client.gst_percentage,
#             total_with_gst=instance.client.total_with_gst,
#             received_amount=instance.client.received_amount,
#             pending_amount=instance.client.pending_amount
#         )
#
#
# @receiver(post_delete, sender=Booking)
# def update_client_revenue_on_booking_delete(sender, instance, **kwargs):
#     """
#     Update client's aggregated revenue when a booking is deleted.
#     """
#     if instance.client:
#         # Recalculate and update client revenue from remaining bookings
#         instance.client.calculate_aggregated_revenue()
#         from clients.models import Client
#         Client.objects.filter(pk=instance.client.pk).update(
#             total_pitched_amount=instance.client.total_pitched_amount,
#             gst_amount=instance.client.gst_amount,
#             gst_percentage=instance.client.gst_percentage,
#             total_with_gst=instance.client.total_with_gst,
#             received_amount=instance.client.received_amount,
#             pending_amount=instance.client.pending_amount
#         )
