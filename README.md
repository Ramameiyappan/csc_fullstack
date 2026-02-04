# CSC e-Governance Portal 🚀

A full-stack **CSC e-Governance Portal** built using **Django REST Framework** (Backend) and **React.js** (Frontend).

🌐 **Live Website:**  
https://csc-fullstack.vercel.app/

In this system, an **operator** can create an account using a username and password and log in using those credentials.  
If the operator logs in using **Google OAuth**, then the operator will always authenticate using Google login.

After successful login, the operator can register daily CSC works such as **electricity, mobile recharge, PAN, insurance, travel, e-Sevai, and other online services**, and maintain proper service records.

To access the **manager role**, an operator must send a role upgrade request.  
Once the **admin approves** the request, the user becomes a manager.

The **manager** can access all ledger details and user details.

---

## 📌 Project Overview

The **CSC e-Governance Portal** digitalizes Common Service Center operations by providing a role-based system with secure authentication and real-time service tracking.

---

## 🛠️ Tech Stack

### Backend
- Python
- Django
- Django REST Framework
- Simple JWT
- Google OAuth
- Postgres

### Frontend
- React.js
- Axios
- HTML
- CSS

---

## 🔐 Authentication & Roles

### Authentication Methods
- JWT Authentication
- Google OAuth Login

### User Roles
Operator - Registers daily CSC services
Manager - Views all records and operators

---

## 📂 Project Structure

### Backend (Django)

django_project/
- backend/
- login/
- work/
- manage.py
- requirements.txt

### Frontend (React)

react_project/
- src/
  - components/
  - pages/
  - api/
  - config/
  - styles/
  - utils/
  - app.css
  - app.jsx
  - index.css
  - main.jsx
- public/
- package.json
- index.httml

---

## 🧾 Services Available

- Electricity Bill
- Mobile Recharge
- PAN Card Services
- Insurance
- Travel Booking
- Top-Up
- E-Sevai
- Enrollment Services

Each service automatically updates:
- Passbook
- User Balance

---

## 📊 Dashboard Features

- Service cards (3-column layout)
- Dynamic modal forms
- Daily transaction tracking
- Excel export
- Role-based access

---

## ⚙️ Installation & Setup

### Backend Setup

1. Create virtual environment
   python -m venv venv

2. Activate virtual environment
   - Windows: venv\Scripts\activate

3. Install dependencies
   pip install -r requirements.txt

4. Run migrations
   python manage.py migrate

5. Create superuser
   python manage.py createsuperuser

6. Start backend server
   python manage.py runserver

---

### Frontend Setup

1. Move to frontend directory
   cd frontend

2. Install dependencies
   npm install

3. Start React server
   npm run dev

---

This project is developed for academic and learning purposes.  
You are free to modify and extend it.
