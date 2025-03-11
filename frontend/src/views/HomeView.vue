<template>
    <div class="d-flex flex-column min-vh-100">
        <!-- Navbar -->
        <nav class="navbar navbar-expand-lg navbar-dark" style="background-color: #0090C1;">
            <a class="navbar-brand px-3" href="#">InsightIQ</a>
        </nav>

        <!-- Hero Section -->
        <section class="text-center pb-1 bg-light d-flex flex-column align-items-center justify-content-center">
            <h1 class="display-6 fw-bold mt-3 mb-3" style="color: #183446;">Welcome to InsightIQ</h1>
            <p class="text-muted mt-2 mb-4">Empowering businesses with intelligent data insights.</p>
            <div class="row g-3">
                <div class="col-md-4">
                    <div class="card shadow-sm p-3 card-hover h-100 d-flex flex-column align-items-center text-center gap-3" style="min-height: 420px;" @click="$router.push('/chat')">
                        <i class="bi bi-chat-left-text h2" style="color: #00A6A6;"></i>
                        <h5 class="mt-2">Natural Language Queries</h5>
                        <p class="text-muted">Interact with data using simple language, no SQL required.</p>
                        <img src="/nlp.jpg" alt="Chat Icon" class="img-fluid" style="max-height: 220px; object-fit: contain;">
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card shadow-sm p-3 card-hover h-100 d-flex flex-column align-items-center text-center gap-3" style="min-height: 420px;" @click="$router.push('/dashboard')">
                        <i class="bi bi-bar-chart h2" style="color: #00A6A6;"></i>
                        <h5 class="mt-2">Automated Reports</h5>
                        <p class="text-muted">Generate insights instantly with AI-powered reporting.</p>
                        <img src="/reports.png" alt="Dashboard Icon" class="img-fluid" style="max-height: 220px; object-fit: contain;">
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card shadow-sm p-3 card-hover h-100 d-flex flex-column align-items-center text-center gap-3" style="min-height: 420px;" @click="$router.push('/synthetic-data')">
                        <i class="bi bi-database h2" style="color: #183446;"></i>
                        <h5 class="mt-2">Generate Synthetic Data</h5>
                        <p class="text-muted">Create custom synthetic datasets tailored to your needs.</p>
                        <img src="/synthetic-data.png" alt="Synthetic Data Icon" class="img-fluid" style="max-height: 220px; object-fit: contain;">
                    </div>
                </div>
            </div>
        </section>


        <!-- Call to Action -->
        <section class="text-center py-4 bg-light mb-4 mt-3">
            <h2 style="color: #183446;">Start Managing Your Data Smarter</h2>
            <p class="text-muted">Experience the power of AI-driven data insights today.</p>
        </section>
    </div>
</template>

<style>
.card-hover {
    transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
    cursor: pointer;
}

.card-hover:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}
</style>
