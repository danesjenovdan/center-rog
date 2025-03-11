from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from wagtail_modeladmin.views import IndexView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.db.models import OuterRef, Subquery

from .models import Plan, Payment, PromoCode, PaymentPlanEvent
from events.export import ExportModelAdminMixin
from wagtail_rangefilter.filters import DateRangeFilter, DateTimeRangeFilter

import csv

class ExportPaymentView(IndexView):
    model_admin = None

    def export_csv(self):
        data = []
        payments = self.queryset.all()
        for payment in payments:
            data.append({
                'first_name': payment.user.first_name,
                'last_name': payment.user.last_name,
                'original_amount': str(payment.original_amount).replace('.', ','),
                'amount': str(payment.amount).replace('.', ','),
                'created_at': payment.created_at.isoformat() if payment.created_at else '',
                'successed_at': payment.successed_at.isoformat() if payment.successed_at else '',
                'transaction_successed_at': payment.transaction_success_at.isoformat() if payment.transaction_success_at else '',
                'invoice_number': payment.invoice_number,
                'ujp_id': payment.ujp_id,
                'plans': '+'.join(list(payment.payment_plans.all().values_list("plan_name", flat=True))),
                'pantheon_id': payment.pantheon_id,
            })

        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="export.csv"'},
        )
        try:
            writer = csv.DictWriter(response, fieldnames=data[0].keys(), dialect='excel-tab', delimiter='\t')
        except IndexError:
            return response
        writer.writeheader()
        writer.writerows(data)

        return response

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)
        return self.export_csv()


class PlanAdmin(ModelAdmin):
    model = Plan
    menu_icon = "pilcrow"
    menu_order = 200
    add_to_settings_menu = True
    add_to_admin_menu = False


class PaymentAdmin(ExportModelAdminMixin, ModelAdmin):
    index_template_name = "admin_export_header.html"
    export_view_class = ExportPaymentView
    model = Payment
    menu_icon = "form"
    menu_order = 201
    add_to_settings_menu = True
    add_to_admin_menu = False
    list_display=['__str__', 'plan_name', 'status', 'amount', 'successed_at', 'created_at']
    list_filter = (("created_at", DateRangeFilter),'status', 'items')
    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__email",
        "invoice_number",
        "ujp_id",
        "pantheon_id",
        "payment_plans__plan_name",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        plan_name = Subquery(PaymentPlanEvent.objects.filter(
            payment=OuterRef("id"),
        ).values("plan_name")[:1])
        qs = qs.annotate(
            plan_name=plan_name,
        )
        return qs

    def plan_name(self, obj):
        return obj.plan_name


class ExportPromoCodeView(IndexView):
    model_admin = None

    def export_csv(self):
        data = []
        promo_codes = self.queryset.all()
        for promo_code in promo_codes:
            data.append({
                'code': promo_code.code,
                'created_at': promo_code.created_at.isoformat() if promo_code.created_at else '',
                'last_entry_at': promo_code.last_entry_at.isoformat() if promo_code.last_entry_at else '',
                'number_of_uses': promo_code.number_of_uses,
                'usage_limit': 1 if promo_code.single_use else promo_code.usage_limit,
                'payment_item_type': promo_code.payment_item_type,
                'event_page': promo_code.event_page,
                'plan': promo_code.plan,
                # TODO - mail uporabnika, če je izdana na določenega uporabnika
                'percent_discount': promo_code.percent_discount,
            })

        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="export.csv"'},
        )
        try:
            writer = csv.DictWriter(response, fieldnames=data[0].keys(), dialect='excel-tab', delimiter='\t')
        except IndexError:
            return response
        writer.writeheader()
        writer.writerows(data)

        return response

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)
        return self.export_csv()


class PromoCodeAdmin(ExportModelAdminMixin, ModelAdmin):
    index_template_name = "admin_export_header.html"
    export_view_class = ExportPromoCodeView
    model = PromoCode
    menu_icon = "form"
    menu_order = 203
    add_to_settings_menu = True
    add_to_admin_menu = False
    list_display = ['__str__', 'created_at', 'last_entry_at', 'display_usage_and_limit']

    def display_usage_and_limit(self, obj):
        limit = 1 if obj.single_use else obj.usage_limit
        uses = obj.number_of_uses
        if limit > 0:
            return f"{uses}/{limit}"
        return f"{uses}/∞"


modeladmin_register(PlanAdmin)
modeladmin_register(PaymentAdmin)
modeladmin_register(PromoCodeAdmin)
