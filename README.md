# 🔥 RideX — Bike Rental Management System

A full-stack bike rental web app built with Flask and Python. RideX allows customers to browse available bikes and submit booking requests, while admins manage everything through a custom-built dashboard.

🌐 **Live Demo:** [ride-x.up.railway.app] (https://ride-x.up.railway.app)

---

## 📸 Screenshots
<img width="2940" height="1661" alt="image" src="https://github.com/user-attachments/assets/3228552d-b939-40c5-9bb8-ccc2e2769caa" />
<img width="2931" height="1421" alt="image" src="https://github.com/user-attachments/assets/edaafcb3-1a71-4d93-8f90-e1854181dab6" />
<img width="2932" height="1659" alt="image" src="https://github.com/user-attachments/assets/bbbbc272-f98b-4a33-8e91-7202009f4c1d" />
<img width="2932" height="1659" alt="image" src="https://github.com/user-attachments/assets/2d8dbad7-5422-477d-9b1c-23e7e177b919" />
<img width="2932" height="1659" alt="image" src="https://github.com/user-attachments/assets/c4fe383b-fc54-42ec-8c45-6253881107c7" />
<img width="2932" height="1659" alt="image" src="https://github.com/user-attachments/assets/c5c71914-7a8f-44a2-9374-30a5a3a73884" />
<img width="2934" height="1661" alt="image" src="https://github.com/user-attachments/assets/b7927682-2b63-4ab1-a481-5177cb3c7a09" />
<img width="2931" height="1660" alt="image" src="https://github.com/user-attachments/assets/f98ef7b1-698e-4721-ab7c-4c9f38455a2c" />




---

## ✨ Features

**Customer Side**
- Browse available bikes with images and pricing
- Submit booking requests with date and contact info
- Booking confirmation page

**Admin Panel**
- Secure login system
- Approve or reject bookings with 5-second undo toast
- Edit and delete bookings
- Add new bikes to the fleet
- Full booking history with search and filter
- Rejected bookings log

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python, Flask |
| Database | PostgreSQL (Railway), SQLAlchemy ORM |
| Frontend | Jinja2, Bootstrap 5, AOS Animations |
| Icons | Bootstrap Icons |
| Deployment | Railway |

---

## 🚀 Run Locally

```bash
git clone https://github.com/lavanya-bhardwaj/RideX.git
cd RideX
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Create a `.env` file with:
