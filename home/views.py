import json
import numpy as np
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import TeamMember, Review


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

            # 🪜 حساب سعر الـ Ladder
            elif category == "ladder":
                A = float(request.POST.get("width"))
                B = float(request.POST.get("height"))
                C = float(request.POST.get("thickness_side"))
                D = float(request.POST.get("thickness_drawer"))
                manufacturing = 60  # تكلفة التصنيع للـ ladder

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

            # ❌ نوع غير معروف
            else:
                return JsonResponse({"error": "نوع غير معروف"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)





from django.http import HttpResponse

def robots_txt(request):
    content = """User-agent: *
Disallow: /admin/
Disallow: /accounts/
Disallow: /search/
Disallow: /cart/
Disallow: /checkout/

Allow: /

Sitemap: https://www.rovanatrade.com/sitemap.xml"""
    return HttpResponse(content, content_type="text/plain")



from django.http import HttpResponse
from django.urls import reverse

def sitemap_xml(request):
    # قائمة بالروابط المهمة في موقعك
    urls = [
    {"loc": "https://www.rovanatrade.com/", "changefreq": "weekly", "priority": "1.0"},
    {"loc": "https://www.rovanatrade.com/products", "changefreq": "weekly", "priority": "0.9"},
    {"loc": "https://www.rovanatrade.com/cable-tray", "changefreq": "weekly", "priority": "0.9"},
    {"loc": "https://www.rovanatrade.com/cable-ladder", "changefreq": "weekly", "priority": "0.8"},
    {"loc": "https://www.rovanatrade.com/galvanized", "changefreq": "monthly", "priority": "0.8"},
    {"loc": "https://www.rovanatrade.com/painted", "changefreq": "monthly", "priority": "0.8"},
    {"loc": "https://www.rovanatrade.com/contact-us", "changefreq": "monthly", "priority": "0.7"},]

    # بناء ملف XML
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""
    for url in urls:
        xml += f"""  <url>
    <loc>{url['loc']}</loc>
    <changefreq>{url['changefreq']}</changefreq>
    <priority>{url['priority']}</priority>
  </url>
"""

    xml += "</urlset>"

    return HttpResponse(xml, content_type="application/xml")


from django.http import HttpResponse

def google_verify(request):
    # ضع محتوى الملف اللي جوجل بعته
    content = """google-site-verification: googleb7c44eff2d1899d9.html"""
    return HttpResponse(content, content_type="text/html")



def products(request):
    return render(request, 'home/products.html')

def cable_tray(request):
    return render(request, 'home/cable_tray.html')

def cable_ladder(request):
    return render(request, 'home/cable_ladder.html')

def galvanized(request):
    return render(request, 'home/galvanized.html')

def painted(request):
    return render(request, 'home/painted.html')