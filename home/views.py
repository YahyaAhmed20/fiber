import json

from django.http import JsonResponse
from django.shortcuts import render
from .models import  Review
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_GET
import re

from .models import UserData
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import HttpResponse


# 📄 عرض الصفحة الرئيسية
@require_GET
@csrf_protect
def home(request):
    reviews = Review.objects.all()

    return render(request, 'home/home.html', {
        'active_page': 'home',
        'reviews': reviews,
    })


@require_POST
@csrf_protect
def calculate_manual_combined(request):
    if request.method == "POST":
        try:
            category = request.POST.get("category")

            steel = 37
            galvanize = 24
            percentage = 1

            # 🛠 حساب سعر الـ Tray
            if category == "tray":
                width = float(request.POST.get("width"))
                height = float(request.POST.get("height"))
                thickness = float(request.POST.get("thickness"))
                manufacturing = 15

                individuals = width + (height * 2)
                stick_price = ((individuals / 100) * thickness * 3 * 8) * (steel + galvanize)
                price_per_meter = (stick_price / 3) + manufacturing
                total_price = price_per_meter * 1.04

                return JsonResponse({
                    "total_price": round(total_price, 2),
                    "details": (
                        f"📏 سعر المتر: {round(price_per_meter, 2)}<br>"
                        f"🪵 سعر العود: {round(stick_price, 2)}<br>"
                        f"👥 عدد الأفراد: {round(individuals, 2)}"
                    )
                })

            # ❄️ حساب سعر الـ Cold Tray (بدون جلفنة)
            elif category == "cold_tray":
                steel = 45 
                galvanize = 0  # لا يوجد جلفنة
                width = float(request.POST.get("width"))
                height = float(request.POST.get("height"))
                thickness = float(request.POST.get("thickness"))
                manufacturing = 15

                individuals = width + (height * 2)
                stick_price = ((individuals / 100) * thickness * 3 * 8) * (steel + galvanize)
                price_per_meter = (stick_price / 3) + manufacturing
                total_price = price_per_meter * 1.04

                return JsonResponse({
                    "total_price": round(total_price, 2),
                    "details": (
                        f"📏 سعر المتر: {round(price_per_meter, 2)}<br>"
                        f"🪵 سعر العود: {round(stick_price, 2)}<br>"
                        f"👥 عدد الأفراد: {round(individuals, 2)}"
                    )
                })

            # 🪜 حساب سعر الـ Ladder
            elif category == "ladder":
                A = float(request.POST.get("width"))
                B = float(request.POST.get("height"))
                C = float(request.POST.get("thickness_side"))
                D = float(request.POST.get("thickness_drawer"))
                manufacturing = 60

                E = ((B / 100) + 0.03) * 2
                F = (E * 3 * C * 8) * (steel + galvanize)
                G = (A / 100) * 10
                H = (G * 0.1 * D * 8) * (steel + galvanize)

                total_price = ((F + H) / 3 * 1.04) + manufacturing

                return JsonResponse({
                    "total_price": round(total_price, 2),
                    "details": (
                        f"👥 الأفراد: {round(E, 3)}<br>"
                        f"📐 جانب الأدراج: {round(F, 2)}<br>"
                        f"🪵 العارض: {round(H, 2)}<br>"
                        f"🏭 التصنيع: {manufacturing}"
                    )
                })

            else:
                return JsonResponse({"error": "نوع غير معروف"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)






@require_POST
@csrf_protect
def calculate_cover_cost(request):
    if request.method == "POST":
        try:
            cover_type = request.POST.get("cover_type")
            cover_width = float(request.POST.get("cover_width"))
            thickness = float(request.POST.get("thickness"))  # متغير

            side_height = 1.5  # ثابت

            manufacturing = 10
            percentage = 1.03

            # تحديد القيم حسب نوع الغطا
            if cover_type == "hot_cover":
                steel = 37
                galvanize = 24
            elif cover_type == "cold_cover":
                steel = 45
                galvanize = 0
            else:
                return JsonResponse({"error": "Invalid cover type"}, status=400)

            # الأفراد (ديناميكي)
            individuals = (side_height * 2) + cover_width

            # إجمالي سعر العود
            stick_price = ((individuals / 100) * thickness * 3 * 8) * (steel + galvanize)

            # إجمالي سعر المتر
            price_per_meter = (stick_price / 3) + manufacturing

            # الإجمالي للمتر للغطا
            total_price = price_per_meter * percentage

            return JsonResponse({
                "total_price": round(total_price, 2),
                "details": (
                    f"👥 الأفراد: {round(individuals, 2)}<br>"
                    f"🪵 سعر العود: {round(stick_price, 2)}<br>"
                    f"📏 سعر المتر: {round(price_per_meter, 2)}<br>"
                    f"🏭 المصنعيات: {manufacturing}<br>"
                    f"📈 النسبة: {percentage}"
                )
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)






@require_POST
@csrf_protect
def save_user_data(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    name = data.get('name', '').strip()
    company = data.get('company', '').strip()
    phone = data.get('phone', '').strip()
    email = data.get('email', '').strip()

    # ✅ Basic validation
    if not name or not company:
        return JsonResponse({'status': 'error', 'message': 'الاسم والشركة مطلوبين'}, status=400)

    if not re.match(r"^01[0-9]{9}$", phone):
        return JsonResponse({'status': 'error', 'message': 'رقم الهاتف غير صالح'}, status=400)

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'status': 'error', 'message': 'البريد الإلكتروني غير صالح'}, status=400)

    if not email.endswith("@gmail.com"):
        return JsonResponse({'status': 'error', 'message': 'يجب استخدام Gmail فقط'}, status=400)

    user_data = UserData.objects.create(
        name=name, company=company, phone=phone, email=email
    )

    return JsonResponse({'status': 'success', 'id': user_data.id})



def robots_txt(request):
    content = [
        "User-agent: *",
        "Allow: /",
        "Sitemap: https://www.rovanatrade.com/sitemap.xml"
    ]
    return HttpResponse("\n".join(content), content_type="text/plain")



