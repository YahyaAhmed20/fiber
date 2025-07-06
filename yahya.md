الكود ده من غير اضافه الانميشن والايموجي   










{% extends 'base.html' %}
{% load static %}
{% block body %}

<!-- Topbar Start -->
<div class="container-fluid topbar bg-secondary d-none d-xl-block w-100">
    <div class="container">
        <div class="row gx-0 align-items-center" style="height: 45px;">
            <div class="col-lg-6 text-center text-lg-start mb-lg-0">
                <div class="d-flex flex-wrap">
                    <a href="#" class="text-muted me-4">
                        <i class="fas fa-map-marker-alt text-primary me-2"></i>Find Our Factory
                    </a>
                    <a href="tel:+01234567890" class="text-muted me-4">
                        <i class="fas fa-phone-alt text-primary me-2"></i>+01234567890
                    </a>
                    <a href="mailto:info@cablefactory.com" class="text-muted me-0">
                        <i class="fas fa-envelope text-primary me-2"></i>info@cablefactory.com
                    </a>
                </div>
            </div>
            <div class="col-lg-6 text-center text-lg-end">
                <div class="d-flex align-items-center justify-content-end">
                    <a href="#" class="btn btn-light btn-sm-square rounded-circle me-3"><i class="fab fa-facebook-f"></i></a>
                    <a href="#" class="btn btn-light btn-sm-square rounded-circle me-3"><i class="fab fa-twitter"></i></a>
                    <a href="#" class="btn btn-light btn-sm-square rounded-circle me-3"><i class="fab fa-instagram"></i></a>
                    <a href="#" class="btn btn-light btn-sm-square rounded-circle me-0"><i class="fab fa-linkedin-in"></i></a>
                </div>
            </div>
        </div>
    </div>
</div>
<!-- Topbar End -->

<!-- Carousel Start -->
<div class="header-carousel">
    <div id="carouselId" class="carousel slide" data-bs-ride="carousel" data-bs-interval="false">
        <ol class="carousel-indicators">
            <li data-bs-target="#carouselId" data-bs-slide-to="0" class="active" aria-current="true" aria-label="First slide"></li>
            <li data-bs-target="#carouselId" data-bs-slide-to="1" aria-label="Second slide"></li>
        </ol>

        <div class="carousel-inner" role="listbox">
            <!-- Slide 1 -->
            <div class="carousel-item active">
                <img src="{% static 'img/cable-carousel-1.jpeg' %}" class="img-fluid w-100" alt="First slide"/>
                <div class="carousel-caption">
                    <div class="container py-4">
                        <div class="row g-5">
                            <div class="col-lg-6 fadeInLeft animated" data-animation="fadeInLeft" data-delay="1s" style="animation-delay: 1s;">
                            <div class="bg-secondary rounded p-5">
  <h4 class="text-white mb-4">CALCULATE CABLE COST</h4>
  <form id="priceForm" method="POST">
    <div class="row g-3">
      <!-- كاتيجوري -->
      <div class="col-md-4">
        <select id="cableCategory" class="form-select" name="category" required>
          <option value="" disabled selected>Select Cable Category</option>
          <option value="ladder">Ladder</option>
          <option value="tray">Tray</option>
        </select>
      </div>

      <!-- نوع المقاس -->
      <div class="col-md-4">
        <select id="cableType" class="form-select" name="type" required>
          <option value="" disabled selected>Select Cable Type</option>
        </select>
      </div>

      <!-- السُمك -->
      <div class="col-md-4">
        <select id="cableThickness" class="form-select" name="thickness" required>
          <option value="" disabled selected>Select Thickness</option>
        </select>
      </div>

      <!-- الجانب -->
      <div class="col-md-4">
        <select id="cableSide" class="form-select" name="side" required>
          <option value="" disabled selected>Select Side</option>
        </select>
      </div>

      <!-- الأبعاد -->
      <div class="col-md-4">
        <select id="cableDim" class="form-select" name="dim" required>
          <option value="" disabled selected>Select Dimension</option>
        </select>
      </div>

      <!-- الطول -->
      <div class="col-md-4">
        <input type="number" step="0.01" min="0" id="cableLength" name="length" class="form-control" placeholder="Enter Length in meters" required>
      </div>

      <div class="col-12">
        <button class="btn btn-primary w-100 py-2" type="submit">Calculate Cost</button>
      </div>

      <div class="col-12 mt-3">
        <div id="result" class="alert alert-info d-none"></div>
      </div>
    </div>
  </form>
  <div class="col-12">
    <div id="costResult" class="text-white mt-3"></div>
  </div>
</div>
</form>


html
Copy
Edit
<script>
const ladderData = {{ options_json_ladder|safe }};
const trayData = {{ options_json_tray|safe }};

const form = document.getElementById("priceForm");
form.addEventListener("submit", function(e) {
  e.preventDefault();
  const category = document.getElementById("cableCategory").value;
  const type = document.getElementById("cableType").value;
  const thickness = document.getElementById("cableThickness").value;
  const side = document.getElementById("cableSide").value;
  const dim = document.getElementById("cableDim").value;
  const length = document.getElementById("cableLength").value;

  if (!category || !type || !thickness || !dim || !length || (category === "ladder" && !side)) {
    alert("Please fill in all fields correctly.");
    return;
  }

  const requestData = {
    category: category,
    type: type,
    thickness: thickness,
    dim: dim,
    length: length,
    side: category === "ladder" ? side : "" // send blank if tray
  };

  fetch("{% url 'home:calculate_price' %}", {
    method: "POST",
    headers: {
      "X-CSRFToken": "{{ csrf_token }}",
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: new URLSearchParams(requestData)
  })
  .then(res => res.json())
  .then(data => {
    const resultDiv = document.getElementById("costResult");
    if (data.total_price) {
      resultDiv.innerHTML = `
        ✅ <strong>Total Price:</strong> ${data.total_price} EGP<br>
        💰 <strong>Price/m:</strong> ${data.price_per_meter} EGP<br>
        📏 <strong>Length:</strong> ${data.length} m
      `;
    } else {
      resultDiv.innerHTML = `<span class="text-danger">${data.error || 'No match found.'}</span>`;
    }
  })
  .catch(err => {
    document.getElementById("costResult").innerHTML = `<span class="text-danger">Error: ${err}</span>`;
  });
});

const categorySelect = document.getElementById("cableCategory");
categorySelect.addEventListener('change', function () {
  const selectedCategory = this.value;
  const data = selectedCategory === 'ladder' ? ladderData : trayData;

  const typeSelect = document.getElementById('cableType');
  const thicknessSelect = document.getElementById('cableThickness');
  const sideSelect = document.getElementById('cableSide');
  const dimSelect = document.getElementById('cableDim');

  // 👇 reset all fields
  typeSelect.innerHTML = '<option disabled selected>Select Cable Type</option>';
  thicknessSelect.innerHTML = '<option disabled selected>Select Thickness</option>';
  sideSelect.innerHTML = '<option disabled selected>Select Side</option>';
  dimSelect.innerHTML = '<option disabled selected>Select Dimension</option>';

  // 🧠 Hide or show "side" field
  if (selectedCategory === 'tray') {
    sideSelect.parentElement.style.display = 'none';
  } else {
    sideSelect.parentElement.style.display = 'block';
  }

  for (const t in data) {
    typeSelect.innerHTML += `<option value="${t}">${t}</option>`;
  }

  typeSelect.addEventListener('change', function () {
    const selectedType = this.value;
    const options = data[selectedType] || [];

    // reset options
    thicknessSelect.innerHTML = '<option disabled selected>Select Thickness</option>';
    dimSelect.innerHTML = '<option disabled selected>Select Dimension</option>';
    sideSelect.innerHTML = '<option disabled selected>Select Side</option>';

    const addedThick = new Set(), addedSide = new Set(), addedDim = new Set();
    options.forEach(opt => {
      if (!addedThick.has(opt.thickness)) {
        addedThick.add(opt.thickness);
        thicknessSelect.innerHTML += `<option value="${opt.thickness}">${opt.thickness} mm</option>`;
      }
      if (!addedDim.has(opt.dim)) {
        addedDim.add(opt.dim);
        dimSelect.innerHTML += `<option value="${opt.dim}">${opt.dim}</option>`;
      }
      if (selectedCategory === "ladder" && opt.side && !addedSide.has(opt.side)) {
        addedSide.add(opt.side);
        sideSelect.innerHTML += `<option value="${opt.side}">${opt.side}</option>`;
      }
    });
  });
});
</script>

            <div class="col-12">
                <div id="costResult" class="text-white mt-3"></div>
            </div>
        </div>
    </form>
</div>
                           
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
<!-- Carousel End -->

<!-- JavaScript for Cost Calculation -->


<!-- Features Start -->
<div class="container-fluid feature py-5">
    <div class="container py-5">
        <div class="text-center mx-auto pb-5 wow fadeInUp" data-wow-delay="0.1s" style="max-width: 800px;">
            <h1 class="display-5 text-capitalize mb-3">Our <span class="text-primary">Features</span></h1>
            <p class="mb-0">Discover the quality and reliability of our wire and cable products, designed to meet your electrical and connectivity needs.</p>
        </div>
        <div class="row g-4 align-items-center">
            <div class="col-xl-4">
                <div class="row gy-4 gx-0">
                    <div class="col-12 wow fadeInUp" data-wow-delay="0.1s">
                        <div class="feature-item">
                            <div class="feature-icon">
                                <span class="fa fa-bolt fa-2x"></span>
                            </div>
                            <div class="ms-4">
                                <h5 class="mb-3">High Conductivity</h5>
                                <p class="mb-0">Our cables ensure efficient power transmission with minimal loss.</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-12 wow fadeInUp" data-wow-delay="0.3s">
                        <div class="feature-item">
                            <div class="feature-icon">
                                <span class="fa fa-shield-alt fa-2x"></span>
                            </div>
                            <div class="ms-4">
                                <h5 class="mb-3">Durable Insulation</h5>
                                <p class="mb-0">Built to withstand harsh environments and ensure safety.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-lg-12 col-xl-4 wow fadeInUp" data-wow-delay="0.2s">
                <img src="{% static 'img/cable-features-img.png' %}" class="img-fluid w-100" style="object-fit: cover;" alt="Img">
            </div>
            <div class="col-xl-4">
                <div class="row gy-4 gx-0">
                    <div class="col-12 wow fadeInUp" data-wow-delay="0.1s">
                        <div class="feature-item justify-content-end">
                            <div class="text-end me-4">
                                <h5 class="mb-3">Custom Lengths</h5>
                                <p class="mb-0">Order cables cut to your exact specifications.</p>
                            </div>
                            <div class="feature-icon">
                                <span class="fa fa-cut fa-2x"></span>
                            </div>
                        </div>
                    </div>
                    <div class="col-12 wow fadeInUp" data-wow-delay="0.3s">
                        <div class="feature-item justify-content-end">
                            <div class="text-end me-4">
                                <h5 class="mb-3">Fast Delivery</h5>
                                <p class="mb-0">Quick and reliable shipping to meet your project deadlines.</p>
                            </div>
                            <div class="feature-icon">
                                <span class="fa fa-truck fa-2x"></span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
<!-- Features End -->

<!-- Fact Counter -->
<div class="container-fluid counter bg-secondary py-5">
    <div class="container py-5">
        <div class="row g-5">
            <div class="col-md-6 col-lg-6 col-xl-3 wow fadeInUp" data-wow-delay="0.1s">
                <div class="counter-item text-center">
                    <div class="counter-item-icon mx-auto">
                        <i class="fas fa-users fa-2x"></i>
                    </div>
                    <div class="counter-counting my-3">
                        <span class="text-white fs-2 fw-bold" data-toggle="counter-up">1200</span>
                        <span class="h1 fw-bold text-white">+</span>
                    </div>
                    <h4 class="text-white mb-0">Satisfied Customers</h4>
                </div>
            </div>
            <div class="col-md-6 col-lg-6 col-xl-3 wow fadeInUp" data-wow-delay="0.3s">
                <div class="counter-item text-center">
                    <div class="counter-item-icon mx-auto">
                        <i class="fas fa-box fa-2x"></i>
                    </div>
                    <div class="counter-counting my-3">
                        <span class="text-white fs-2 fw-bold" data-toggle="counter-up">500</span>
                        <span class="h1 fw-bold text-white">+</span>
                    </div>
                    <h4 class="text-white mb-0">Products Sold</h4>
                </div>
            </div>
            <div class="col-md-6 col-lg-6 col-xl-3 wow fadeInUp" data-wow-delay="0.5s">
                <div class="counter-item text-center">
                    <div class="counter-item-icon mx-auto">
                        <i class="fas fa-industry fa-2x"></i>
                    </div>
                    <div class="counter-counting my-3">
                        <span class="text-white fs-2 fw-bold" data-toggle="counter-up">50</span>
                        <span class="h1 fw-bold text-white">+</span>
                    </div>
                    <h4 class="text-white mb-0">Factory Outlets</h4>
                </div>
            </div>
        </div>
    </div>
</div>
<!-- Fact Counter End -->

<!-- Banner Start -->
<div class="container-fluid banner pb-5 wow zoomInDown" data-wow-delay="0.1s">
    <div class="container pb-5">
        <div class="banner-item rounded">
            <img src="{% static 'img/cable-banner.jpg' %}" class="img-fluid rounded w-100" alt="">
            <div class="banner-content">
                <h2 class="text-primary">Order Your Cables</h2>
                <h1 class="text-white">Need Custom Cables?</h1>
                <p class="text-white">Contact us for tailored solutions.</p>
                <div class="banner-btn">
                    <a href="#" class="btn btn-secondary rounded-pill py-3 px-4 px-md-5 me-2">WhatsApp</a>
                    <a href="#" class="btn btn-primary rounded-pill py-3 px-4 px-md-5 ms-2">Contact Us</a>
                </div>
            </div>
        </div>
    </div>
</div>
<!-- Banner End -->

<hr>

<!-- Team Start -->
<div class="container-fluid team pb-5">
    <div class="container pb-5">
        <div class="text-center mx-auto pb-5 wow fadeInUp" data-wow-delay="0.1s" style="max-width: 800px;">
            <h1 class="display-5 text-capitalize mb-3">Customer <span class="text-primary">Support</span> Team</h1>
            <p class="mb-0">Our dedicated team is here to assist you with all your cable-related queries.</p>
        </div>
        <div class="row g-4">
            <div class="col-md-6 col-lg-6 col-xl-3 wow fadeInUp" data-wow-delay="0.1s">
                <div class="team-item p-4 pt-0">
                    <div class="team-img">
                        <img src="{% static 'img/team-1.jpg' %}" class="img-fluid rounded w-100" alt="Image">
                    </div>
                    <div class="team-content pt-4">
                        <h4>Ahmed Ali</h4>
                        <p>Customer Support</p>
                        <div class="team-icon d-flex justify-content-center">
                            <a class="btn btn-square btn-light rounded-circle mx-1" href=""><i class="fab fa-facebook-f"></i></a>
                            <a class="btn btn-square btn-light rounded-circle mx-1" href=""><i class="fab fa-twitter"></i></a>
                            <a class="btn btn-square btn-light rounded-circle mx-1" href=""><i class="fab fa-instagram"></i></a>
                            <a class="btn btn-square btn-light rounded-circle mx-1" href=""><i class="fab fa-linkedin-in"></i></a>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-6 col-lg-6 col-xl-3 wow fadeInUp" data-wow-delay="0.3s">
                <div class="team-item p-4 pt-0">
                    <div class="team-img">
                        <img src="{% static 'img/team-2.jpg' %}" class="img-fluid rounded w-100" alt="Image">
                    </div>
                    <div class="team-content pt-4">
                        <h4>Fatima Hassan</h4>
                        <p>Technical Advisor</p>
                        <div class="team-icon d-flex justify-content-center">
                            <a class="btn btn-square btn-light rounded-circle mx-1" href=""><i class="fab fa-facebook-f"></i></a>
                            <a class="btn btn-square btn-light rounded-circle mx-1" href=""><i class="fab fa-twitter"></i></a>
                            <a class="btn btn-square btn-light rounded-circle mx-1" href=""><i class="fab fa-instagram"></i></a>
                            <a class="btn btn-square btn-light rounded-circle mx-1" href=""><i class="fab fa-linkedin-in"></i></a>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-6 col-lg-6 col-xl-3 wow fadeInUp" data-wow-delay="0.5s">
                <div class="team-item p-4 pt-0">
                    <div class="team-img">
                        <img src="{% static 'img/team-3.jpg' %}" class="img-fluid rounded w-100" alt="Image">
                    </div>
                    <div class="team-content pt-4">
                        <h4>Khaled Omar</h4>
                        <p>Sales Manager</p>
                        <div class="team-icon d-flex justify-content-center">
                            <a class="btn btn-square btn-light rounded-circle mx-1" href=""><i class="fab fa-facebook-f"></i></a>
                            <a class="btn btn-square btn-light rounded-circle mx-1" href=""><i class="fab fa-twitter"></i></a>
                            <a class="btn btn-square btn-light rounded-circle mx-1" href=""><i class="fab fa-instagram"></i></a>
                            <a class="btn btn-square btn-light rounded-circle mx-1" href=""><i class="fab fa-linkedin-in"></i></a>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-6 col-lg-6 col-xl-3 wow fadeInUp" data-wow-delay="0.7s">
                <div class="team-item p-4 pt-0">
                    <div class="team-img">
                        <img src="{% static 'img/team-4.jpg' %}" class="img-fluid rounded w-100" alt="Image">
                    </div>
                    <div class="team-content pt-4">
                        <h4>Sara Ahmed</h4>
                        <p>Order Specialist</p>
                        <div class="team-icon d-flex justify-content-center">
                            <a class="btn btn-square btn-light rounded-circle mx-1" href=""><i class="fab fa-facebook-f"></i></a>
                            <a class="btn btn-square btn-light rounded-circle mx-1" href=""><i class="fab fa-twitter"></i></a>
                            <a class="btn btn-square btn-light rounded-circle mx-1" href=""><i class="fab fa-instagram"></i></a>
                            <a class="btn btn-square btn-light rounded-circle mx-1" href=""><i class="fab fa-linkedin-in"></i></a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
<!-- Team End -->

<!-- Testimonial Start -->
<div class="container-fluid testimonial pb-5">
    <div class="container pb-5">
        <div class="text-center mx-auto pb-5 wow fadeInUp" data-wow-delay="0.1s" style="max-width: 800px;">
            <h1 class="display-5 text-capitalize mb-3">Our Clients<span class="text-primary">Reviews</span></h1>
            <p class="mb-0">Hear from our valued customers about their experience with our cables.</p>
        </div>
        <div class="owl-carousel testimonial-carousel wow fadeInUp" data-wow-delay="0.1s">
            <div class="testimonial-item">
                <div class="testimonial-quote"><i class="fa fa-quote-right fa-2x"></i></div>
                <div class="testimonial-inner p-4">
                    <img src="{% static 'img/testimonial-1.jpg' %}" class="img-fluid rounded" alt="">
                    <div class="ms-4">
                        <h4>Mohammed Salem</h4>
                        <p>Contractor</p>
                        <div class="d-flex text-primary">
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star text-body"></i>
                        </div>
                    </div>
                </div>
                <div class="border-top rounded-bottom p-4">
                    <p class="mb-0">The cables are reliable and the cost calculator saved us time in budgeting.</p>
                </div>
            </div>
            <div class="testimonial-item">
                <div class="testimonial-quote"><i class="fa fa-quote-right fa-2x"></i></div>
                <div class="testimonial-inner p-4">
                    <img src="{% static 'img/testimonial-2.jpg' %}" class="img-fluid rounded" alt="">
                    <div class="ms-4">
                        <h4>Lina Mahmoud</h4>
                        <p>Project Manager</p>
                        <div class="d-flex text-primary">
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star text-body"></i>
                            <i class="fas fa-star text-body"></i>
                        </div>
                    </div>
                </div>
                <div class="border-top rounded-bottom p-4">
                    <p class="mb-0">Excellent customer service and high-quality products.</p>
                </div>
            </div>
            <div class="testimonial-item">
                <div class="testimonial-quote"><i class="fa fa-quote-right fa-2x"></i></div>
                <div class="testimonial-inner p-4">
                    <img src="{% static 'img/testimonial-3.jpg' %}" class="img-fluid rounded" alt="">
                    <div class="ms-4">
                        <h4>Hassan Ibrahim</h4>
                        <p>Electrician</p>
                        <div class="d-flex text-primary">
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                        </div>
                    </div>
                </div>
                <div class="border-top rounded-bottom p-4">
                    <p class="mb-0">The fiber optic cables exceeded our performance expectations.</p>
                </div>
            </div>
        </div>
    </div>
</div>
<!-- Testimonial End -->

{% endblock %}