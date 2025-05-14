<template>
  <div class="landing-container">
    <!-- Hero Section -->
    <section class="hero-section text-center">
      <div class="container py-5">
        <h1 class="display-4 fw-bold mb-3" style="color: #0395ff">
          Transform Your Data into Insights
        </h1>
        <p class="lead mb-4">
          AI-powered data analytics that saves you time and unveils hidden opportunities
        </p>
        <div class="d-flex justify-content-center gap-3 mb-5">
          <button @click="$router.push('/chat')" class="btn btn-primary btn-lg px-4">
            Chat with Demo
          </button>
          <button @click="$router.push('/plans')" class="btn btn-outline-secondary btn-lg px-4">
            See Plans
          </button>
        </div>
        <img
          src="/dashboard.png"
          alt="InsightIQ Dashboard"
          class="img-fluid rounded shadow hero-image"
        />
      </div>
    </section>

    <section class="value-prop py-5 bg-light">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-lg-6">
            <h2 class="fw-bold mb-4" style="color: #0395ff">
              Focus on Strategy, Let AI Handle the Analysis
            </h2>
            <p class="mb-4">
              InsightIQ is a powerful data analytics automation tool that transforms how you
              interact with your business data. Upload Excel files, CSV documents, or sync directly
              with Google Sheets – then let our AI do the work.
            </p>
            <div class="d-flex align-items-center mb-3">
              <div class="feature-icon bg-primary rounded-circle p-3 me-3">
                <i class="fa-solid fa-clock text-white fs-4"></i>
              </div>
              <div>
                <h5 class="mb-1">Save Valuable Time</h5>
                <p class="text-muted mb-0">Automate repetitive data analysis tasks</p>
              </div>
            </div>
            <div class="d-flex align-items-center mb-3">
              <div class="feature-icon bg-primary rounded-circle p-3 me-3">
                <i class="fa-solid fa-lightbulb text-white fs-4"></i>
              </div>
              <div>
                <h5 class="mb-1">Discover Key Insights</h5>
                <p class="text-muted mb-0">AI finds patterns and opportunities you might miss</p>
              </div>
            </div>
            <div class="d-flex align-items-center">
              <div class="feature-icon bg-primary rounded-circle p-3 me-3">
                <i class="fa-solid fa-chart-line text-white fs-4"></i>
              </div>
              <div>
                <h5 class="mb-1">Make Data-Driven Decisions</h5>
                <p class="text-muted mb-0">Turn complex data into actionable strategies</p>
              </div>
            </div>
          </div>
          <div class="col-lg-6 mt-4 mt-lg-0">
            <img src="/data.jpg" alt="Data Analysis" class="img-fluid" />
          </div>
        </div>
      </div>
    </section>

    <!-- Data Sources -->
    <section class="data-sources py-5 bg-light">
      <div class="container">
        <h2 class="text-center fw-bold mb-5" style="color: #0395ff">Connect Your Data Sources</h2>
        <div class="row justify-content-center">
          <div class="col-lg-8">
            <div class="data-sources-container d-flex flex-wrap justify-content-center gap-4 mb-4">
              <div class="data-source-item text-center">
                <div class="icon-container mb-2">
                  <i class="fa-solid fa-file-excel fs-1" style="color: #217346"></i>
                </div>
                <p>Excel Files</p>
              </div>
              <div class="data-source-item text-center">
                <div class="icon-container mb-2">
                  <i class="fa-solid fa-file-csv fs-1" style="color: #f88379"></i>
                </div>
                <p>CSV Files</p>
              </div>
              <div class="data-source-item text-center">
                <div class="icon-container mb-2">
                  <i class="fa-brands fa-google-drive fs-1" style="color: #4285f4"></i>
                </div>
                <p>Google Sheets</p>
              </div>
              <div class="data-source-item text-center">
                <div class="icon-container mb-2">
                  <i class="fa-solid fa-database fs-1" style="color: #6c757d"></i>
                </div>
                <p>SQL Databases</p>
              </div>
            </div>
            <p class="text-center">
              Easily import data from multiple sources or connect directly to your existing
              platforms.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Key Features -->
    <section class="features py-5">
      <div class="container">
        <h2 class="text-center fw-bold mb-5" style="color: #0395ff">
          Powerful Features at Your Fingertips
        </h2>

        <div class="row g-4">
          <div class="col-md-4" @click="$router.push('/chat')">
            <div class="card shadow h-100 feature-card">
              <div class="card-body text-center p-4">
                <div class="feature-icon-wrapper mb-3">
                  <i class="fa-solid fa-comments fs-1" style="color: #00a6a6"></i>
                </div>
                <h4 class="card-title">Ask Your Data</h4>
                <p class="card-text">
                  Interact naturally with your data through our AI assistant. Ask questions in plain
                  language and get instant insights.
                </p>
                <img src="/nlp.jpg" alt="Chat Interface" class="img-fluid mt-3 rounded" />
              </div>
            </div>
          </div>

          <div class="col-md-4" @click="$router.push('/dashboard')">
            <div class="card shadow h-100 feature-card">
              <div class="card-body text-center p-4">
                <div class="feature-icon-wrapper mb-3">
                  <i class="fa-solid fa-chart-bar fs-1" style="color: #00a6a6"></i>
                </div>
                <h4 class="card-title">Smart Reports</h4>
                <p class="card-text">
                  Access beautiful, automatically generated reports and visualizations that
                  highlight key metrics and trends.
                </p>
                <img src="/reports.png" alt="Reports Dashboard" class="img-fluid mt-3 rounded" />
              </div>
            </div>
          </div>

          <div class="col-md-4" @click="$router.push('/alerts')">
            <div class="card shadow h-100 feature-card">
              <div class="card-body text-center p-4">
                <div class="feature-icon-wrapper mb-3">
                  <i class="fa-solid fa-bell fs-1" style="color: #00a6a6"></i>
                </div>
                <h4 class="card-title">Intelligent Alerts</h4>
                <p class="card-text">
                  Set up customized alerts to notify you of important changes or anomalies in your
                  business data.
                </p>
                <img src="/alerts.jpg" alt="Alert System" class="img-fluid mt-3 rounded" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Call to Action -->
    <section class="cta py-5 bg-primary text-white text-center">
      <div class="container py-3">
        <h2 class="fw-bold mb-4">Ready to Transform Your Data Strategy?</h2>
        <p class="lead mb-4">
          Join thousands of businesses using InsightIQ to make smarter, data-driven decisions
        </p>
        <div class="d-flex justify-content-center gap-3">
          <button @click="$router.push('/chat')" class="btn btn-light btn-lg px-4">
            Chat with Demo
          </button>
          <button @click="$router.push('/plans')" class="btn btn-light btn-lg px-4">
            See Plans
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.landing-container {
  overflow-x: hidden;
}

.hero-section {
  background: linear-gradient(to bottom, #f8f9fa, #ffffff);
  padding: 2rem 0;
}

.hero-image {
  max-width: 900px;
  margin: 0 auto;
}

.feature-icon {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.feature-card {
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
  cursor: pointer;
  border: none;
  border-radius: 10px;
  overflow: hidden;
}

.btn-primary {
  background-color: #0395ff !important;
  color: white !important;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1) !important;
}

.feature-icon-wrapper {
  height: 80px;
  width: 80px;
  background-color: rgba(0, 166, 166, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

.data-source-item {
  width: 120px;
}

.icon-container {
  height: 80px;
  width: 80px;
  background-color: rgba(108, 117, 125, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

.testimonial-card {
  border: none;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.testimonial-avatar {
  width: 50px;
  height: 50px;
}

.avatar-placeholder {
  width: 50px;
  height: 50px;
  background-color: #0395ff;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.cta {
  background: linear-gradient(135deg, #0395ff, #0380da);
}
</style>
