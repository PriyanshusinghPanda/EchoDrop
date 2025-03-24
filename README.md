# **EchoDrop - Anonymous Messaging App**

**EchoDrop** is a secure and anonymous messaging app that allows users to receive messages without revealing their identity. Users can share a unique link to receive messages privately, with a dashboard to manage and view them.

---

## **🚀 Features**
- **User Authentication:** Secure registration and login system.
- **Anonymous Messaging:** Users can send and receive messages without revealing their identity.
- **Unique Shareable Link:** Each user gets a unique link to receive anonymous messages.
- **Dashboard:** View received messages and track unread ones.
- **Regenerate Link:** Refresh your anonymous message link anytime for security.
- **Secure & Encrypted:** Uses password hashing and SSL for secure communication.

---

## **🛠 Tech Stack**
- **Backend:** Flask, Flask-Login, SQLAlchemy
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite (Can be switched to PostgreSQL or MongoDB)
- **Security:** Password hashing, authentication, SSL encryption

---

## **📌 Installation & Setup**

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/PriyanshusinghPanda/EchoDrop.git
cd EchoDrop
```

### **2️⃣ Create a Virtual Environment & Install Dependencies**
```sh
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate  # For Windows
pip install -r requirements.txt
```

### **3️⃣ Set Up the Database**
```sh
python
>>> from app import db
>>> db.create_all()
>>> exit()
```

### **4️⃣ Run the Application**
```sh
python app.py
```
Visit **http://127.0.0.1:5000/** in your browser.

---

## **🌍 Deployment**

### **Deploy Using Gunicorn (Production Server)**
```sh
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### **Deploy on Heroku/Render/AWS (Modify Database Settings)**
- Replace `SQLALCHEMY_DATABASE_URI` with a cloud database (PostgreSQL, MongoDB).
- Use `gunicorn` instead of Flask’s built-in server.

---

## **📸 Screenshots**
🚀 *Coming Soon*

---

## **🤝 Contributing**
Want to improve EchoDrop? Feel free to **fork** the repo and submit a pull request!

```sh
git clone https://github.com/PriyanshusinghPanda/EchoDrop.git
cd EchoDrop
git checkout -b feature-branch
# Make changes & commit
```

---

## **📄 License**
This project is licensed under the MIT License.

---

## **🔗 Connect With Me**
📧 Email: *your.email@example.com*  
💻 LinkedIn: [Your LinkedIn](https://linkedin.com/in/your-profile)  
🔗 GitHub: [PriyanshusinghPanda](https://github.com/PriyanshusinghPanda)

---

### ⭐ If you find this project useful, don’t forget to **star** this repository! 🚀
