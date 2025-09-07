# Adaptive Question Generator

This repository contains the implementation of the **Adaptive Question Generator** for the dissertation project.  
It combines an **Angular 19 client application** with a **FastAPI backend** to deliver adaptive question generation and intelligent tutoring features.

---

## 📂 Project Structure

```
adaptive_question_generator/
│
├── client/       # Angular 19 frontend application
│   ├── src/      # Angular source code
│   ├── dist/     # Build output (ignored by Git)
│   └── ...       
│
├── fastapi/      # FastAPI backend
│   ├── app/      # Main application code
│   ├── tests/    # Unit tests
│   └── ...
│
└── README.md     # Project documentation
```

---

## 🚀 Technologies Used

### Frontend (client/)
- **Angular 19**
- TypeScript
- RxJS
- HTML / CSS / SCSS
- Angular Material

### Backend (fastapi/)
- **FastAPI**
- Python 3.11+
- SQLAlchemy / Pydantic
- Uvicorn
- REST API design

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/<USERNAME>/adaptive_question_generator.git
cd adaptive_question_generator
```

### 2. Setup the Angular client
```bash
cd client
npm install
ng serve
```
The client will be running at: `http://localhost:4200`

### 3. Setup the FastAPI backend
```bash
cd fastapi
pip install -r requirements.txt
uvicorn app.main:app --reload
```
The API will be available at: `http://localhost:8000`

---

## 🎯 Features
- Adaptive question generation
- Intelligent tutoring workflow
- Angular-based interactive UI
- REST API backend with FastAPI
- Modular structure (frontend + backend separation)

---

## 📖 Dissertation Context
This project is developed as part of a **MSc dissertation**, exploring the integration of:
- Causal AI
- Bayesian methods
- Adaptive question generation for personalized learning

---

## 👤 Author
**Mir Mohamed Ullah**  
[GitHub Profile](https://github.com/mir-dhaka)
