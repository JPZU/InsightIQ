<template>
  <div class="d-flex flex-column min-vh-100">
    <section class="text-center pb-1 d-flex flex-column align-items-center justify-content-center">
      <h1 class="display-6 fw-bold mt-4 mb-3" style="color: #183446">Welcome to InsightIQ</h1>
      <p class="text-muted mt-2 mb-4">Empowering businesses with intelligent data insights.</p>
      <div class="row g-3 justify-content-center">
        <div class="col-md-4" @click="$router.push('/chat')">
          <div class="card shadow-sm p-3 card-hover h-100 text-center">
            <i class="bi bi-chat-left-text h2" style="color: #00a6a6"></i>
            <h5>Natural Language Queries</h5>
            <p class="text-muted">Interact with data using simple language, no SQL required.</p>
            <img src="/nlp.jpg" alt="Chat Icon" class="img-fluid" style="max-height: 220px;">
          </div>
        </div>
        <div class="col-md-4" @click="$router.push('/dashboard')">
          <div class="card shadow-sm p-3 card-hover h-100 text-center">
            <i class="bi bi-bar-chart h2" style="color: #00a6a6"></i>
            <h5>Automated Reports</h5>
            <p class="text-muted">Generate insights instantly with AI-powered reporting.</p>
            <img src="/reports.png" alt="Dashboard Icon" class="img-fluid" style="max-height: 220px;">
          </div>
        </div>
      </div>
    </section>
  </div>
</template>