<template>
  <div class="plans-container py-5">
    <div class="container">
      <!-- Header -->
      <div class="text-center mb-5">
        <h2 class="display-4 fw-bold mb-3" style="color: #0395ff">{{ $t('plans.choose_plan') }}</h2>
        <p class="lead">{{ $t('plans.pricing_subtitle') }}</p>
      </div>

      <!-- Pricing Cards -->
      <div class="row justify-content-center g-4">
        <!-- Base Plan -->
        <div class="col-md-5 col-lg-4">
          <div class="card shadow h-100">
            <div class="card-header bg-light py-3">
              <h3 class="text-center mb-0">{{ $t('plans.base_plan') }}</h3>
            </div>
            <div class="card-body p-4">
              <div class="text-center mb-4">
                <span class="display-5 fw-bold">180,000 COP</span>
                <span class="text-muted">{{ $t('plans.per_month') }}</span>
              </div>
              <ul class="list-unstyled mb-4">
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  <strong>500</strong> {{ $t('plans.queries_per_month') }}
                </li>
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  {{ $t('plans.up_to_users', { count: 5 }) }}
                </li>
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  {{ $t('plans.csv_excel_support') }}
                </li>
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  {{ $t('plans.ai_reports') }}
                </li>
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  {{ $t('plans.up_to_alarms', { count: 50 }) }}
                </li>
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  {{ $t('plans.email_support') }}
                </li>
              </ul>
              <button class="btn btn-primary w-100 py-2">{{ $t('plans.get_started') }}</button>
            </div>
          </div>
        </div>

        <!-- Premium Plan -->
        <div class="col-md-5 col-lg-4">
          <div class="card border-primary shadow h-100">
            <div class="card-header bg-primary text-white py-3">
              <h3 class="text-center mb-0">{{ $t('plans.premium_plan') }}</h3>
            </div>
            <div class="card-body p-4">
              <div class="text-center mb-4">
                <span class="display-5 fw-bold">300,000 COP</span>
                <span class="text-muted">{{ $t('plans.per_month') }}</span>
              </div>
              <ul class="list-unstyled mb-4">
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  <strong>1000</strong> {{ $t('plans.queries_per_month') }}
                </li>
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  {{ $t('plans.up_to_users', { count: 15 }) }}
                </li>
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  {{ $t('plans.csv_excel_sheets_support') }}
                </li>
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  {{ $t('plans.advanced_ai_reports') }}
                </li>
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  {{ $t('plans.unlimited_alarms') }}
                </li>
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  {{ $t('plans.priority_support') }}
                </li>
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  {{ $t('plans.early_access') }}
                </li>
              </ul>
              <button class="btn btn-primary w-100 py-2">{{ $t('plans.start_trial') }}</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Pricing Explanation -->
      <div class="row justify-content-center mt-5">
        <div class="col-lg-8">
          <div class="card shadow-sm">
            <div class="card-body">
              <h3 class="mb-4" style="color: #0395ff">{{ $t('plans.pricing_calculation_title') }}</h3>

              <p>
                {{ $t('plans.pricing_calculation_text') }}
              </p>

              <p>
                {{ $t('plans.pricing_includes') }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- FAQ Section -->
      <div class="row justify-content-center mt-5">
        <div class="col-lg-8">
          <h3 class="text-center mb-4" style="color: #0395ff">{{ $t('plans.faq_title') }}</h3>

          <div class="accordion" id="faqAccordion">
            <div class="accordion-item">
              <h2 class="accordion-header">
                <button
                  class="accordion-button"
                  type="button"
                  data-bs-toggle="collapse"
                  data-bs-target="#faq1"
                >
                  {{ $t('plans.faq_query_title') }}
                </button>
              </h2>
              <div
                id="faq1"
                class="accordion-collapse collapse show"
                data-bs-parent="#faqAccordion"
              >
                <div class="accordion-body">
                  {{ $t('plans.faq_query_answer') }}
                </div>
              </div>
            </div>

            <div class="accordion-item">
              <h2 class="accordion-header">
                <button
                  class="accordion-button collapsed"
                  type="button"
                  data-bs-toggle="collapse"
                  data-bs-target="#faq2"
                >
                  {{ $t('plans.faq_users_title') }}
                </button>
              </h2>
              <div id="faq2" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                <div class="accordion-body">
                  {{ $t('plans.faq_users_answer') }}
                </div>
              </div>
            </div>

            <div class="accordion-item">
              <h2 class="accordion-header">
                <button
                  class="accordion-button collapsed"
                  type="button"
                  data-bs-toggle="collapse"
                  data-bs-target="#faq3"
                >
                  {{ $t('plans.faq_limit_title') }}
                </button>
              </h2>
              <div id="faq3" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                <div class="accordion-body">
                  {{ $t('plans.faq_limit_answer') }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PlansView',
}
</script>

<style scoped>
.plans-container {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.card {
  border-radius: 10px;
  transition: transform 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.card-header {
  border-radius: 10px 10px 0 0 !important;
}

.btn-primary {
  background-color: #0395ff;
  border-color: #0395ff;
  font-weight: 600;
}

.accordion-button:not(.collapsed) {
  background-color: rgba(3, 149, 255, 0.1);
  color: #0395ff;
}

.accordion-button:focus {
  box-shadow: none;
  border-color: rgba(3, 149, 255, 0.25);
}

.list-unstyled li {
  padding: 8px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.display-4 {
  color: #0395ff;
}
</style>
