
# @csrf_exempt
# def calculate_tray_manual(request):
#     if request.method == "POST":
#         try:
#             # 🔹 القيم المدخلة من المستخدم
#             width = float(request.POST.get("width"))
#             height = float(request.POST.get("height"))
#             thickness = float(request.POST.get("thickness"))

#             # ✅ الثوابت
#             metal_price = 35         # الصاج
#             galvanize_price = 22     # الجلفنة
#             manufacturing = 50       # مصنعيات
#             ratio = 1.01             # النسبة

#             # ✅ الحسابات
#             individuals = width + (height * 2)  # الأفراد
#             stick_price = ((individuals / 100) * thickness * 3 * 8) * (metal_price + galvanize_price)  # اجمالي سعر العود
#             price_per_meter = (stick_price / 3) + manufacturing  # اجمالي سعر المتر
#             total_price = price_per_meter * ratio  # الإجمالي للمتر

#             return JsonResponse({
#                 "individuals": round(individuals, 2),
#                 "stick_price": round(stick_price, 2),
#                 "price_per_meter": round(price_per_meter, 2),
#                 "total_price": round(total_price, 2),
#             })
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=400)

#     return JsonResponse({"error": "Invalid request"}, status=400)





# # home/views.py

# from django.shortcuts import render
# from .forms import ManualPricingForm

# def calculate_dynamic_price(request):
#     total_price = None
#     breakdown = {}

#     if request.method == 'POST':
#         form = ManualPricingForm(request.POST)
#         if form.is_valid():
#             A = form.cleaned_data['width_drawer']
#             B = form.cleaned_data['height_side']
#             C = form.cleaned_data['thickness_side']
#             D = form.cleaned_data['thickness_drawer']

#             # 🔢 القيم الثابتة
#             steel = 35        # الصاج
#             galvanize = 22    # الجلفنه
#             labor = 200       # مصنعيات
#             percentage = 1.0174   # النسبه

#             # 🔢 الحسابات بالمعادلات
#             E = ((B / 100) + 0.03) * 2                     # الافراد للجانب
#             F = (E * 3 * C * 8) + (steel + galvanize)      # جانب الادر
#             G = (A / 100) * 10                             # افراد درج
#             H = (G * 0.1 * D * 8) * (steel + galvanize)    # الدرج الإجمالي
#             K = labor                                      # مصنعيات
#             L = percentage                                 # النسبة

#             total_price = (F + H + K) * L

#             # علشان نعرض القيم لو حابب تطبعهم في القالب
#             breakdown = {
#                 'الافراد للجانب': round(E, 3),
#                 'جانب الادر': round(F, 3),
#                 'افراد درج': round(G, 3),
#                 'الدرج الإجمالي': round(H, 3),
#                 'اجمالي السعر': round(total_price, 3)
#             }

#     else:
#         form = ManualPricingForm()

#     return render(request, 'home/calculate_dynamic_price.html', {
#         'form': form,
#         'total_price': total_price,
#         'breakdown': breakdown
#     })







