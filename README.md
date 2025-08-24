# 💇‍♀️ Salon Booking & Management System  
_A Capstone Project Adapted from a Task Management API_  

## 📌 Overview  
The **Salon Booking & Management System** is a web-based **Task Management API** built using **Django** and **Django REST Framework (DRF)**.  

It is tailored for small to medium-sized beauty salons to simplify:  
- Appointment scheduling  
- Service management  
- Staff management  
- Client reminders  

This project demonstrates **backend engineering skills** such as **user authentication, CRUD operations, model relationships, API design, and deployment**.  

---

## 🎯 Core Features  
- **User Authentication**: Clients, Staff, and Admins  
- **Service Management**: Add, update, delete, and list salon services  
- **Booking Management (Tasks)**: Create, update, cancel, and track appointments  
- **Recurring Tasks**: Auto-schedule appointments every 6 weeks  
- **Reminders**: Notify clients when their appointment is near  
- **Staff Assignment**: Assign staff to specific bookings  
- **Role-Based Access Control**: Admin, Staff, and Clients have different permissions  
- **Dashboard (API-based)**: For staff and admins to view/manage services and bookings  

---

## 🛠 Tech Stack  
- **Backend**: Django, Django REST Framework (DRF)  
- **Database**: SQLite/PostgreSQL (Django ORM)  
- **Authentication**: Django Auth (JWT/Session)  
- **Deployment**: Heroku / PythonAnywhere  

---

## 🗂 Django App Structure  
- **Accounts** → Handles user registration, login, logout  
- **Services** → Manages available salon services  
- **Bookings** → Handles appointment creation, updates, cancellations  
- **Staff** → Manages staff info and authentication  

---

## 🔗 API Endpoints  
| **Endpoint**           | **Method** | **Description**                |
|-------------------------|------------|--------------------------------|
| `/api/login/`          | POST       | Log in                        |
| `/api/logout/`         | POST       | Log out                       |
| `/api/register/`       | POST       | Register new user             |
| `/api/services/`       | GET, POST  | List or add services          |
| `/api/services/<id>/`  | PUT, DELETE| Update or delete service      |
| `/api/bookings/`       | GET, POST  | List or book appointments     |
| `/api/bookings/<id>/`  | PUT, DELETE| Update or cancel booking      |
| `/api/staff/`          | GET, POST  | List or add staff             |
| `/api/staff/<id>/`     | PUT, DELETE| Update or remove staff        |

---

## 🗄 Database Schema  
### **1. CustomUser (AbstractUser)**  
- `username`: CharField  
- `email`: EmailField  
- `password`: CharField  

### **2. Service**  
- `name`: CharField  
- `description`: TextField  
- `due_date`: DateTimeField  
- `priority_level`: CharField _(choices: Low, Medium, High)_  

### **3. Staff**  
- `username`: CharField  
- `email`: EmailField  
- `password`: CharField  

### **4. Booking**  
- `client`: ForeignKey → CustomUser  
- `staff`: ForeignKey → Staff _(nullable)_  
- `service`: ForeignKey → Service  
- `appointment_time`: DateTimeField  
- `status`: CharField _(choices: pending, confirmed, completed, canceled)_  

---

## 📅 Timeline (5-Week Plan)  
- **Week 1**: Finalize idea, create virtual environment, set up Django project, configure settings, and plan schema.  
- **Week 2**: Create custom user model and implement authentication (registration, login/logout).  
- **Week 3**: Build services and booking modules (models, serializers, views, endpoints).  
- **Week 4**: Implement staff management, appointment logic, and access control.  
- **Week 5**: Write tests, documentation, and prepare for deployment.  

---

## ✅ Conclusion  
The **Salon Booking & Management System** is a **Task Management API adapted to the salon industry**.  
By managing bookings as tasks, assigning staff, sending reminders, and auto-scheduling recurring appointments, this project delivers both **academic alignment** and **real-world impact**.  

---
