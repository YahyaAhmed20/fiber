import pandas as pd
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from project.settings import BASE_DIR
import numpy as np
import json

# 📊 ملفات الإكسل
EXCEL_PATH = os.path.join(BASE_DIR, 'static', 'calculated_prices.xlsx')
df = pd.read_excel(EXCEL_PATH)
df.columns = df.columns.str.strip().str.lower()



TRAY_EXCEL_PATH = os.path.join(BASE_DIR, 'static', 'tray_dataa.xlsx')
df_tray = pd.read_excel(TRAY_EXCEL_PATH)
df_tray.columns = df_tray.columns.str.strip().str.lower()

df_tray['type'] = df_tray['type'].astype(str).str.strip()
df_tray['thickness'] = pd.to_numeric(df_tray['thickness'], errors='coerce')
df_tray['dim'] = pd.to_numeric(df_tray['dim'], errors='coerce')

# ✅ عرض الأعمدة للتأكد
print("Tray Columns:", df_tray.columns)

# 📂 فصل ladder فقط
df_ladder = df[df['type'].astype(str).str.contains(r"\*", na=False)]

# 🧠 إعداد بيانات ladder و tray للتعامل مع القوائم
grouped_data = df_ladder.groupby('type').apply(
    lambda x: x[['thickness', 'side', 'dim']].drop_duplicates().to_dict(orient='records')
).to_dict()

grouped_tray = df_tray.groupby('type').apply(
    lambda x: x[['thickness', 'dim']].drop_duplicates().to_dict(orient='records')
).to_dict()

# 📋 بيانات HTML
types = sorted(df_ladder['type'].astype(str).unique())
thicknesses = sorted(df_ladder['thickness'].astype(str).unique())
sides = sorted(df_ladder['side'].astype(str).unique())
dims = sorted(df_ladder['dim'].astype(str).unique())
tray_types = sorted(df_tray['type'].astype(str).unique())
tray_thicknesses = sorted(df_tray['thickness'].astype(str).unique())
tray_dims = sorted(df_tray['dim'].astype(str).unique())

@csrf_exempt
def home(request):
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
    })

@csrf_exempt
def calculate_price(request):
    if request.method == "POST":
        category = request.POST.get("category")
        type_ = request.POST.get("type")
        thickness = request.POST.get("thickness")
        dim = request.POST.get("dim")
        length = request.POST.get("length")

        if not all([category, type_, thickness, dim, length]):
            return JsonResponse({"error": "Missing required fields"}, status=400)

        if category == "ladder":
            side_value = request.POST.get("side")
            if side_value in [None, '', 'undefined']:
                return JsonResponse({"error": "Side is required for ladder"}, status=400)
            try:
                thickness = float(thickness)
                dim = float(dim)
                length = float(length)
                side = float(side_value)
            except ValueError:
                return JsonResponse({"error": "Invalid number input"}, status=400)

            df_used = df_ladder
            result = df_used[
                (df_used['type'].astype(str) == type_) &
                (np.isclose(df_used['thickness'].astype(float), thickness)) &
                (np.isclose(df_used['side'].astype(float), side)) &
                (np.isclose(df_used['dim'].astype(float), dim))
            ]
            price_column = "price_final"

        else:  # tray
            try:
                thickness = float(thickness)
                dim = float(dim)
                length = float(length)
            except ValueError:
                return JsonResponse({"error": "Invalid number input"}, status=400)

            df_used = df_tray
            result = df_used[
                (df_used['type'].astype(str) == type_) &
                (np.isclose(df_used['thickness'].astype(float), thickness)) &
                (np.isclose(df_used['dim'].astype(float), dim))
            ]
            price_column = "price_with_joints"

        if not result.empty:
            row = result.iloc[0]
            if price_column not in row:
                return JsonResponse({"error": f"Missing price column: {price_column}"}, status=500)

            price_per_meter = float(row[price_column])
            total_price = round(price_per_meter * length, 2)

            return JsonResponse({
                "total_price": total_price,
                "price_per_meter": price_per_meter,
                "length": length
            })

        return JsonResponse({"error": "No match found"}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=400)