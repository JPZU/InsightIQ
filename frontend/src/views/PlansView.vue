<template>
  <div class="plans-container py-5">
    <div class="container">
      <!-- Header -->
      <div class="text-center mb-5">
        <h1 class="display-4 fw-bold mb-3" style="color: #0395ff">Choose Your Plan</h1>
        <p class="lead">Flexible pricing options to suit your data analysis needs</p>
      </div>

      <!-- Pricing Cards -->
      <div class="row justify-content-center g-4">
        <!-- Basic Plan -->
        <div class="col-md-5 col-lg-4">
          <div class="card shadow h-100">
            <div class="card-header bg-light py-3">
              <h3 class="text-center mb-0">Basic Plan</h3>
            </div>
            <div class="card-body p-4">
              <div class="text-center mb-4">
                <span class="display-4 fw-bold">18,000 COP</span>
                <span class="text-muted">/month</span>
              </div>
              <ul class="list-unstyled mb-4">
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  <strong>50 queries</strong> per month
                </li>
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  Standard response speed
                </li>
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  Basic data visualization
                </li>
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  Email support
                </li>
              </ul>
              <button class="btn btn-primary w-100 py-2">Get Started</button>
            </div>
          </div>
        </div>

        <!-- Premium Plan -->
        <div class="col-md-5 col-lg-4">
          <div class="card border-primary shadow h-100">
            <div class="card-header bg-primary text-white py-3">
              <h3 class="text-center mb-0">Premium Plan</h3>
            </div>
            <div class="card-body p-4">
              <div class="text-center mb-4">
                <span class="display-4 fw-bold">30,000 COP</span>
                <span class="text-muted">/month</span>
              </div>
              <ul class="list-unstyled mb-4">
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  <strong>100 queries</strong> per month
                </li>
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  Priority response speed
                </li>
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  Advanced data visualization
                </li>
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  Priority email & chat support
                </li>
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  Early access to new features
                </li>
              </ul>
              <button class="btn btn-primary w-100 py-2">Start Free Trial</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Pricing Explanation -->
      <div class="row justify-content-center mt-5">
        <div class="col-lg-8">
          <div class="card shadow-sm">
            <div class="card-body">
              <h3 class="mb-4" style="color: #0395ff">How we calculate our pricing</h3>
              
              <h5 class="mt-4">Basic Plan Calculation</h5>
              <ul class="list-unstyled">
                <li class="mb-2">50 queries × 1,000 tokens = 50,000 tokens</li>
                <li class="mb-2">50,000 tokens × $0.0015 USD = $0.075 USD</li>
                <li class="mb-2">$0.075 USD × ~4,000 COP/USD ≈ 300 COP</li>
              </ul>
              <p>We apply a 60x multiplier to account for:</p>
              <ul>
                <li>Longer or more complex responses (e.g., with tables or charts)</li>
                <li>Retry attempts due to failed requests</li>
                <li>Infrastructure, file storage, backups</li>
                <li>Overhead (monitoring, alerting, platform logs)</li>
              </ul>
              <p class="fw-bold">Final estimated cost: ~18,000 COP per client/month</p>

              <h5 class="mt-4">Premium Plan Calculation</h5>
              <ul class="list-unstyled">
                <li class="mb-2">100 queries × 1,000 tokens = 100,000 tokens</li>
                <li class="mb-2">100,000 tokens × $0.0015 USD = $0.15 USD</li>
                <li class="mb-2">$0.15 USD × ~4,000 COP/USD ≈ 600 COP</li>
              </ul>
              <p>Applying the same 60x margin for usage and operations:</p>
              <p class="fw-bold">Final estimated cost: ~30,000 COP per client/month</p>
            </div>
          </div>
        </div>
      </div>

      <!-- FAQ Section -->
      <div class="row justify-content-center mt-5">
        <div class="col-lg-8">
          <h3 class="text-center mb-4" style="color: #0395ff">Frequently Asked Questions</h3>
          
          <div class="accordion" id="faqAccordion">
            <div class="accordion-item">
              <h2 class="accordion-header">
                <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#faq1">
                  What counts as a query?
                </button>
              </h2>
              <div id="faq1" class="accordion-collapse collapse show" data-bs-parent="#faqAccordion">
                <div class="accordion-body">
                  A query is counted each time you interact with our AI assistant, whether you're asking a question about your data, requesting a visualization, or generating a report. Each conversation turn counts as one query.
                </div>
              </div>
            </div>
            
            <div class="accordion-item">
              <h2 class="accordion-header">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#faq2">
                  Can I upgrade or downgrade my plan?
                </button>
              </h2>
              <div id="faq2" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                <div class="accordion-body">
                  Yes, you can change your plan at any time. When you upgrade, you'll get immediate access to the higher limits. Downgrades will take effect at the start of your next billing cycle.
                </div>
              </div>
            </div>
            
            <div class="accordion-item">
              <h2 class="accordion-header">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#faq3">
                  What happens if I exceed my query limit?
                </button>
              </h2>
              <div id="faq3" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                <div class="accordion-body">
                  If you exceed your monthly query limit, you'll have the option to purchase additional queries or wait until your quota refreshes at the start of your next billing cycle. We'll notify you when you're approaching your limit.
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
  name: 'PlansView'
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
}

.card:hover {
  transform: translateY(-5px);
}

.card-header {
  border-radius: 10px 10px 0 0 !important;
}

.btn-primary {
  background-color: #0395ff;
  border-color: #0395ff;
}

.accordion-button:not(.collapsed) {
  background-color: rgba(3, 149, 255, 0.1);
  color: #0395ff;
}

.accordion-button:focus {
  box-shadow: none;
  border-color: rgba(3, 149, 255, 0.25);
}
</style>