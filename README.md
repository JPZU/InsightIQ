# InsightIQ

This project consists of a **backend** built with FastAPI and a **frontend** built with React (using Vite). Below are the steps to install dependencies and run the project.

---

## **Prerequisites**

Before proceeding, ensure you have the following installed on your system:

- **Python 3.8+**: Required for the backend.
  - Download and install Python from [python.org](https://www.python.org/downloads/).
  - Verify installation:
    ```bash
    python --version
    ```

- **Node.js 16+**: Required for the frontend.
  - Download and install Node.js from [nodejs.org](https://nodejs.org/).
  - Verify installation:
    ```bash
    node --version
    npm --version
    ```
---

## **Install Dependencies**

### **Backend**
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

### **Frontend**
1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install the required Node.js packages:
   ```bash
   npm install
   ```

---

## **Run the Project**

### **Backend**
1. Start the FastAPI server:
   ```bash
   uvicorn backend.main:app --reload
   ```
2. The backend will be available at:
   ```
   http://localhost:8000
   ```

### **Frontend**
1. Navigate to the `frontend` directory (if not already there):
   ```bash
   cd frontend
   ```
2. Start the development server:
   ```bash
   npm run dev

   ```
3. The frontend will be available at:
   ```
   http://localhost:5173
   ```

## Database Migrations
To manage database migrations, we use Alembic. Follow these steps to create and apply migrations:

### 1. Generate a Migration
1. Navigate to the backend directory (if not already there):

   ```bash
   cd backend
   ```
2. Generate a new migration file based on the changes in your SQLAlchemy models:

   ```bash
   alembic revision --autogenerate -m "Models configured"
   ```
   This command will create a new migration file in the alembic/versions/ directory.
### 2. Apply the migration
1. Apply the migration to update the database schema:

   ```bash
   alembic upgrade head
   ```
   This command will execute the SQL commands in the migration file and update the database.