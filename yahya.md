دي views بس مش مضافه عليها security 




import json
import numpy as np
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import  Review


# 📄 عرض الصفحة الرئيسية
@csrf_exempt
def home(request):
    reviews = Review.objects.all()

    return render(request, 'home/home.html', {
        'active_page': 'home',
        'reviews': reviews,
    })


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






@csrf_exempt
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



# home/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UserData

@csrf_exempt
def save_user_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_data = UserData.objects.create(
            name=data.get('name'),
            company=data.get('company'),
            phone=data.get('phone'),
            email=data.get('email')
        )
        return JsonResponse({'status': 'success', 'id': user_data.id})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)



from django.http import HttpResponse

def robots_txt(request):
    content = [
        "User-agent: *",
        "Allow: /",
        "Sitemap: https://www.rovanatrade.com/sitemap.xml"
    ]
    return HttpResponse("\n".join(content), content_type="text/plain")



# home/views.py
from django.http import HttpResponse

def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
     
        "Sitemap: https://www.rovanatrade.com/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")







Script in home page  



<script>

let pendingForm = null; 
let skipCheck = false; 

function checkUserData(formId) {
  if (!localStorage.getItem("userData") && !skipCheck) {
    pendingForm = formId;
    document.getElementById("userDataFormWrapper").classList.remove("d-none");
    window.scrollTo({ top: 0, behavior: 'smooth' });
    return false;
  }
  return true;
}

document.getElementById("userDataForm").addEventListener("submit", function (e) {
  e.preventDefault();
  
  const formData = {
    name: this.name.value,
    company: this.company.value,
    phone: this.phone.value,
    email: this.email.value
  };

  // حفظ في قاعدة البيانات عبر AJAX
  fetch("/save-user-data/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken") // لو الفورم محمي
    },
    body: JSON.stringify(formData)
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === "success") {
      localStorage.setItem("userData", JSON.stringify(formData));
      document.getElementById("userDataFormWrapper").classList.add("d-none");

      if (pendingForm) {
        skipCheck = true;
        document.getElementById(pendingForm).dispatchEvent(new Event("submit"));
        skipCheck = false;
        pendingForm = null;
      }
    }
  });

});

// دالة للحصول على CSRF
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
  // Toggle between Tray and Ladder fields
  document.getElementById("category").addEventListener("change", function() {
    const isLadder = this.value === "ladder";
    const isTrayType = this.value === "tray" || this.value === "cold_tray";

    document.querySelectorAll(".ladder-inputs").forEach(el => el.classList.toggle("d-none", !isLadder));
    document.querySelectorAll(".tray-inputs").forEach(el => el.classList.toggle("d-none", !isTrayType));
  });

  // Manual Calculation Form Submission
  document.getElementById("manualTrayForm").addEventListener("submit", function(e) {
  e.preventDefault();

  if (!checkUserData("manualTrayForm")) return; // 🚀 هنا بيجبر على التسجيل الأول

  const formData = new FormData(this);


    fetch("/calculate_manual_combined/", {
      method: "POST",
      headers: {
        "X-CSRFToken": "{{ csrf_token }}"
      },
      body: formData
    })
    .then(res => res.json())
    .then(data => {
      const resultDiv = document.getElementById("manualResult");
      resultDiv.classList.remove("d-none");
      if (data.total_price) {
        resultDiv.innerHTML = `✅ <strong>الإجمالي للمتر:</strong> ${data.total_price} جنيه`;
      } else {
        resultDiv.innerHTML = `<span class="text-danger">${data.error || 'حدث خطأ أثناء الحساب.'}</span>`;
      }
    })
    .catch(error => {
      const resultDiv = document.getElementById("manualResult");
      resultDiv.classList.remove("d-none");
      resultDiv.innerHTML = `<span class="text-danger">Error: ${error}</span>`;
    });
  });



  {% comment %} Cover {% endcomment %}


  
// عند تغيير نوع الغطا نمسح القيم المدخلة فقط
// عند تغيير نوع الغطا نمسح القيم المدخلة فقط
document.querySelector('select[name="cover_type"]').addEventListener("change", function () {
  // مسح عرض الغطا
  document.querySelector('input[name="cover_width"]').value = "";
  // مسح التخانة
  document.querySelector('input[name="thickness"]').value = "";
  // مسح النتيجة
  const resultDiv = document.getElementById("coverResult");
  resultDiv.classList.add("d-none");
  resultDiv.innerHTML = "";
});


document.getElementById("coverCostForm").addEventListener("submit", function(e) {
  e.preventDefault();

  if (!checkUserData("coverCostForm")) return; // 🚀 برضو يجبر على التسجيل

  const formData = new FormData(this);


  fetch("/calculate_cover_cost/", {
    method: "POST",
    headers: {
      "X-CSRFToken": "{{ csrf_token }}"
    },
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    const resultDiv = document.getElementById("coverResult");
    resultDiv.classList.remove("d-none");
    if (data.total_price) {
      resultDiv.innerHTML = `✅ <strong>الإجمالي للمتر:</strong> ${data.total_price} جنيه`;
    } else {
      resultDiv.innerHTML = `<span class="text-danger">${data.error || 'حدث خطأ أثناء الحساب.'}</span>`;
    }
  })
  .catch(error => {
    const resultDiv = document.getElementById("coverResult");
    resultDiv.classList.remove("d-none");
    resultDiv.innerHTML = `<span class="text-danger">Error: ${error}</span>`;
  });
});

</script>


السلام عليكم ي ععالمي problem solving and security and python and django and programmer