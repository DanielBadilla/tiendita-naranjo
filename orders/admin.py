from django.contrib import admin

from .models import Order

from .models import PurchaseHistory

@admin.register(PurchaseHistory)
class PurchaseHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'total', 'purchased_at')

admin.site.register(Order)