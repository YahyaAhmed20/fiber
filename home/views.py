import json
import numpy as np
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import *
# 📄 عرض الصفحة الرئيسية
@csrf_exempt
def home(request):
    team_members = TeamMember.objects.all()
    reviews = Review.objects.all()

    return render(request, 'home/home.html', {
        'active_page': 'home',
        'team_members': team_members,
        'reviews': reviews,

    })


# 🔢 حساب السعر


@csrf_exempt
def calculate_manual_combined(request):
    if request.method == "POST":
        try:
            category = request.POST.get("category")

            steel = 37
            galvanize = 24
            percentage = 1

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
                    "details": f"📏 سعر المتر: {round(price_per_meter, 2)}<br>🪵 سعر العود: {round(stick_price, 2)}<br>👥 عدد الأفراد: {round(individuals, 2)}"
                })

            elif category == "ladder":
                A = float(request.POST.get("width"))
                B = float(request.POST.get("height"))
                C = float(request.POST.get("thickness_side"))
                D = float(request.POST.get("thickness_drawer"))
                labor = 200

                E = ((B / 100) + 0.03) * 2
                F = (E * 3 * C * 8) + (steel + galvanize)
                G = (A / 100) * 10
                H = (G * 0.1 * D * 8) * (steel + galvanize)

                total_price = (F + H + labor) * percentage

                return JsonResponse({
                    "total_price": round(total_price, 2),
                    "details": f"👥 الأفراد: {round(E, 3)}<br>📐 جانب الأدراج: {round(F, 2)}<br>🪵 العارض: {round(H, 2)}"
                })

            else:
                return JsonResponse({"error": "نوع غير معروف"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)