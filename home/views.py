from django.shortcuts import render
import pandas as pd
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from project.settings import BASE_DIR

# تحميل الملف مرة واحدة
EXCEL_PATH = os.path.join(BASE_DIR, 'static', 'New Microsoft Excel Worksheet.xlsx')
df = pd.read_excel(EXCEL_PATH, skiprows=2)

df.columns = [
    'type', 'thickness', 'side', 'dim',
    'metal_price', 'galv_price',
    'manuf_price', 'price_plain', 'price_with_cover',
    'price_with_joints', 'price_final'
]
df = df[df['type'] != 'type']

df = df.dropna(subset=['type', 'thickness', 'side', 'dim', 'price_final'])
types = sorted(df['type'].astype(str).unique())
thicknesses = sorted(df['thickness'].astype(str).unique())
sides = sorted(df['side'].astype(str).unique())
dims = sorted(df['dim'].astype(str).unique())
df_ladder = df[df['type'].astype(str).str.contains(r"\*", na=False)]

# تبعتهم للتمبلت زي كده
# تمريرهم للتمبلت
context = {
    'types': types,
    'thicknesses': thicknesses,
    'sides': sides,
    'dims': dims,
}
# نفلتر ladder بس

@csrf_exempt
def home(request):
    # نعرض فقط البيانات اللي فيها *
    types = sorted(df_ladder['type'].astype(str).unique())
    thicknesses = sorted(df_ladder['thickness'].astype(str).unique())
    dims = sorted(df_ladder['dim'].astype(str).unique())

    return render(request, 'home/home.html', {
        'types': types,
        'thicknesses': thicknesses,
        'dims': dims,
        'sides': sides,
    })
@csrf_exempt
def calculate_price(request):
    if request.method == "POST":
        type_ = request.POST.get("type")
        thickness = request.POST.get("thickness")
        length = float(request.POST.get("length", 0))

        result = df_ladder[
            (df_ladder['type'].astype(str) == type_) &
            (df_ladder['thickness'].astype(str) == thickness)
        ]

        if not result.empty:
            price_per_meter = float(result.iloc[0]['price_final'])
            total_price = round(price_per_meter * length, 2)

            return JsonResponse({
                "total_price": total_price,
                "price_per_meter": price_per_meter,
                "length": length
            })

        return JsonResponse({"error": "No match found"}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=400)