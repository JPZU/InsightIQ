<template>
  <div class="d-flex flex-column min-vh-100">
    <section class="text-center pb-1 d-flex flex-column align-items-center justify-content-center">
      <h1 class="display-6 fw-bold mt-3 mb-3" style="color: #183446">{{ $t('app.welcome') }}</h1>
      <p class="text-muted mt-2 mb-4">{{ $t('app.description') }}</p>
      <div class="row g-3 justify-content-center">
        <div class="col-md-4" @click="$router.push('/chat')">
          <div class="card shadow-sm p-3 card-hover h-100 text-center">
            <i class="bi bi-chat-left-text h2" style="color: #00a6a6"></i>
            <h5 class="mt-2">{{ $t('app.natural_language') }}</h5>
            <p class="text-muted">{{ $t('app.natural_language_desc') }}</p>
            <img src="/nlp.jpg" alt="Chat Icon" class="img-fluid" style="max-height: 220px" />
          </div>
        </div>
        <div class="col-md-4" @click="$router.push('/dashboard')">
          <div class="card shadow-sm p-3 card-hover h-100 text-center">
            <i class="bi bi-bar-chart h2" style="color: #00a6a6"></i>
            <h5 class="mt-2">{{ $t('app.reports') }}</h5>
            <p class="text-muted">{{ $t('app.reports_desc') }}</p>
            <img
              src="/reports.png"
              alt="Dashboard Icon"
              class="img-fluid"
              style="max-height: 220px"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- Call to Action -->
    <section class="text-center py-4 bg-light mb-4 mt-3">
      <h2 style="color: #183446">{{ $t('app.smart_manage') }}</h2>
      <p class="text-muted">{{ $t('app.smart_manage_desc') }}</p>
    </section>
  </div>
</template>
