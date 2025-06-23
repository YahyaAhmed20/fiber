import pandas as pd
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from project.settings import BASE_DIR
import numpy as np
import json

# ❗ استخدم الملف الجديد
EXCEL_PATH = os.path.join(BASE_DIR, 'static', 'calculated_prices.xlsx')
df = pd.read_excel(EXCEL_PATH)

# نتاكد الأعمدة مكتوبة صح
df.columns = df.columns.str.strip().str.lower()

# نفصل ladder فقط
df_ladder = df[df['type'].astype(str).str.contains(r"\*", na=False)]

grouped_data = df_ladder.groupby('type').apply(
    lambda x: x[['thickness', 'side', 'dim']].drop_duplicates().to_dict(orient='records')
).to_dict()
types = sorted(df_ladder['type'].astype(str).unique())
thicknesses = sorted(df_ladder['thickness'].astype(str).unique())
sides = sorted(df_ladder['side'].astype(str).unique())
dims = sorted(df_ladder['dim'].astype(str).unique())

@csrf_exempt
def home(request):
    ...
    options_json = json.dumps(grouped_data)  # ⬅️ لازم تكون محضر grouped_data زي ما عملنا

    return render(request, 'home/home.html', {
        'types': types,
        'thicknesses': thicknesses,
        'sides': sides,
        'dims': dims,
        'options_json': options_json,  # ⬅️ مهم للـ JS
    })

@csrf_exempt
def calculate_price(request):
    if request.method == "POST":
        type_ = request.POST.get("type")
        thickness = float(request.POST.get("thickness"))
        side = float(request.POST.get("side"))
        dim = float(request.POST.get("dim"))
        length = float(request.POST.get("length", 0))

        result = df_ladder[
            (df_ladder['type'].astype(str) == type_) &
            (np.isclose(df_ladder['thickness'].astype(float), thickness)) &
            (np.isclose(df_ladder['side'].astype(float), side)) &
            (np.isclose(df_ladder['dim'].astype(float), dim))
        ]

        if not result.empty:
            row = result.iloc[0]
            price_per_meter = float(row['price_final'])  # بناخد السعر النهائي من الجدول
            total_price = round(price_per_meter * length, 2)

            return JsonResponse({
                "total_price": total_price,
                "price_per_meter": price_per_meter,
                "length": length
            })

        return JsonResponse({"error": "No match found"}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=400)
