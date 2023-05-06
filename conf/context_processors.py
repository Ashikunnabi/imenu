from django.conf import settings
from django.contrib.auth.models import Permission
# from apps.core.rbac.models import Permission

# from apps.main.user_panel.models import DealerSalesReps


def application_information(request):
    variables = {
        "APPLICATION_NAME": settings.APPLICATION_NAME,
        "COMPANY_NAME": settings.COMPANY_NAME,
        "COMPANY_EMAIL": settings.COMPANY_EMAIL,
        "COMPANY_PHONE": settings.COMPANY_PHONE,
        "FAVICON_URL": settings.FAVICON_URL,
        "COMPANY_NAME_ICON_URL": settings.COMPANY_NAME_ICON_URL,
        "JS_VERSION": "1.00",
    }
    return variables


def sales_reps_information(request):
    variables = {
        "SALES_REPS_NAME": "",
        "SALES_REPS_TITLE": "",
        "SALES_REPS_IMAGE": "",
        "SALES_REPS_EMAIL": "",
        "SALES_REPS_PHONE": "",
    }

    # if hasattr(request, "user"):
    #     if request.user.is_authenticated:
    #         sales_reps = DealerSalesReps.objects.filter(dealer=request.user)
    #         if sales_reps.exists():
    #             if sales_reps.first().sales_reps.count():
    #                 sales_rep = sales_reps.first()
    #                 variables = {
    #                     "SALES_REPS_NAME": sales_rep.sales_reps.first().name,
    #                     "SALES_REPS_TITLE": sales_rep.sales_reps.first().title,
    #                     "SALES_REPS_IMAGE": sales_rep.sales_reps.first().image,
    #                     "SALES_REPS_EMAIL": sales_rep.sales_reps.first().email,
    #                     "SALES_REPS_PHONE": sales_rep.sales_reps.first().phone,
    #                 }
    return variables


def current_user_permissions(request):
    permissions = []
    if not request.user.is_anonymous:
        permission_set = request.user.get_all_permissions()
        permissions = [permission for permission in permission_set]

    variables = {"CURRENT_USER_PERMISSIONS": set(permissions)}
    return variables
