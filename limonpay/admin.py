from django.contrib import admin

from limonpay.models import User, Card, MerchantCategory, Merchant, PhonePaymentTransaction, CardPaymentTransaction

admin.site.register(User)
admin.site.register(Card)
admin.site.register(MerchantCategory)
admin.site.register(Merchant)
admin.site.register(CardPaymentTransaction)


@admin.register(PhonePaymentTransaction)
class PhonePaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'card', 'amount', 'created_at')

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If the object is being created, not updated
            # Select the first card associated with the user (you can customize this logic as needed)
            user_cards = Card.objects.filter(user=obj.user)
            if user_cards.exists():
                if not obj.card in user_cards:
                    raise Exception
        super().save_model(request, obj, form, change)
