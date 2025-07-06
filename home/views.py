import json
import numpy as np
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import LadderPrice, TrayPrice


# 📄 عرض الصفحة الرئيسية
@csrf_exempt
def home(request):
    # 🧠 جلب بيانات الـ Ladder والـ Tray وتحويلها إلى DataFrame
    df_ladder = pd.DataFrame.from_records(LadderPrice.objects.all().values())
    df_tray = pd.DataFrame.from_records(TrayPrice.objects.all().values())

    # ✅ تجهيز بيانات الـ ladder
    if not df_ladder.empty:
        grouped_data = (
            df_ladder.groupby('type')
            .apply(
                lambda x: x[['thickness', 'side', 'dim']]
                .drop_duplicates()
                .to_dict(orient='records'),
                include_groups=False
            )
            .to_dict()
        )

        types = sorted(df_ladder['type'].astype(str).unique())
        thicknesses = sorted(df_ladder['thickness'].astype(str).unique())
        sides = sorted(df_ladder['side'].astype(str).unique())
        dims = sorted(df_ladder['dim'].astype(str).unique())
    else:
        grouped_data, types, thicknesses, sides, dims = {}, [], [], [], []

    # ✅ تجهيز بيانات الـ tray
    if not df_tray.empty:
        grouped_tray = (
            df_tray.groupby('type')
            .apply(
                lambda x: x[['thickness', 'dim']]
                .drop_duplicates()
                .to_dict(orient='records'),
                include_groups=False
            )
            .to_dict()
        )

        tray_types = sorted(df_tray['type'].astype(str).unique())
        tray_thicknesses = sorted(df_tray['thickness'].astype(str).unique())
        tray_dims = sorted(df_tray['dim'].astype(str).unique())
    else:
        grouped_tray, tray_types, tray_thicknesses, tray_dims = {}, [], [], []

    return render(request, 'home/home.html', {
        'ladder_types': types,
        'ladder_thicknesses': thicknesses,
        'ladder_sides': sides,
        'ladder_dims': dims,
        'tray_types': tray_types,
        'tray_thicknesses': tray_thicknesses,
        'tray_sides': [],  # tray مفيهاش side
        'tray_dims': tray_dims,
        'options_json_ladder': json.dumps(grouped_data),
        'options_json_tray': json.dumps(grouped_tray),
        'active_page': 'home',
    })


# 🔢 حساب السعر
@csrf_exempt
def calculate_price(request):
    if request.method == "POST":
        category = request.POST.get("category")
        type_ = request.POST.get("type")
        thickness = request.POST.get("thickness")
        dim = request.POST.get("dim")
        length = request.POST.get("length")

        # ✅ التأكد من كل القيم المطلوبة موجودة
        if not all([category, type_, thickness, dim, length]):
            return JsonResponse({"error": "Missing required fields"}, status=400)

        try:
            thickness = float(thickness)
            dim = float(dim)
            length = float(length)
        except ValueError:
            return JsonResponse({"error": "Invalid number input"}, status=400)

        if category == "ladder":
            # ladder يحتاج قيمة side
            side_value = request.POST.get("side")
            if side_value in [None, '', 'undefined']:
                return JsonResponse({"error": "Side is required for ladder"}, status=400)

            try:
                side = float(side_value)
            except ValueError:
                return JsonResponse({"error": "Invalid side input"}, status=400)

            # البحث عن السعر
            result = LadderPrice.objects.filter(
                type=type_,
                thickness=thickness,
                side=side,
                dim=dim
            ).first()

            if not result:
                return JsonResponse({"error": "No match found"}, status=404)

            price_per_meter = result.price_final

        else:  # tray
            result = TrayPrice.objects.filter(
                type=type_,
                thickness=thickness,
                dim=dim
            ).first()

            if not result:
                return JsonResponse({"error": "No match found"}, status=404)

            price_per_meter = result.price_with_joints

        total_price = round(price_per_meter * length, 2)

        return JsonResponse({
            "total_price": total_price,
            "price_per_meter": price_per_meter,
            "length": length
        })

    # 🚫 لو مش POST
    return JsonResponse({"error": "Invalid request"}, status=400)
