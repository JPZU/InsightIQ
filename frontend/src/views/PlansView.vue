<template>
  <div class="plans-container py-5">
    <div class="container">
      <!-- Header -->
      <div class="text-center mb-5">
        <h2 class="display-4 fw-bold mb-3" style="color: #0395ff">Choose Your Plan</h2>
        <p class="lead">Flexible pricing options to suit your business needs</p>
      </div>

      <!-- Pricing Cards -->
      <div class="row justify-content-center g-4">
        <!-- Base Plan -->
        <div class="col-md-5 col-lg-4">
          <div class="card shadow h-100">
            <div class="card-header bg-light py-3">
              <h3 class="text-center mb-0">Base Plan</h3>
            </div>
            <div class="card-body p-4">
              <div class="text-center mb-4">
                <span class="display-5 fw-bold">180,000 COP</span>
                <span class="text-muted">/month</span>
              </div>
              <ul class="list-unstyled mb-4">
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  <strong>500 queries</strong> per month
                </li>
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  Up to <strong>5 users</strong>
                </li>
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  CSV/Excel file support
                </li>
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  AI-generated reports
                </li>
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  Up to <strong>50 alarms</strong>
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
                <span class="display-5 fw-bold">300,000 COP</span>
                <span class="text-muted">/month</span>
              </div>
              <ul class="list-unstyled mb-4">
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  <strong>1000 queries</strong> per month
                </li>
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  Up to <strong>15 users</strong>
                </li>
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  CSV/Excel/Google Sheets support
                </li>
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  Advanced AI reports
                </li>
                <li class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>
                  <strong>Unlimited alarms</strong>
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
              
              <p>Our pricing is based on the computational resources required to process your queries and maintain your data. The Base Plan covers essential business needs, while the Premium Plan offers enhanced capabilities for growing teams.</p>
              
              <p>All plans include secure data storage, regular backups, and our standard service level agreement.</p>
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
                  Can I add more users to my plan?
                </button>
              </h2>
              <div id="faq2" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                <div class="accordion-body">
                  Yes! You can add additional users to any plan for a small monthly fee per user. Contact our sales team for enterprise pricing if you need more than 15 users.
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
                  If you exceed your monthly query limit, you'll have the option to purchase additional query packs or upgrade your plan. We'll notify you when you're approaching your limit so you can make adjustments.
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
  border: 1px solid rgba(0,0,0,0.1);
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
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
  border-bottom: 1px solid rgba(0,0,0,0.05);
}

.display-4 {
  color: #0395ff;
}
</style>