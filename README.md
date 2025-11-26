# SmartMail Automation Tool

A professional Python-based email automation system that sends personalized emails to multiple recipients using a CSV contact list.

Perfect for:

- Payment reminders  
- Marketing campaigns  
- Customer updates  
- Notifications  
- Bulk personalized messages  

SmartMail Automation Tool is designed for small businesses, freelancers, and teams who need fast, reliable email automation without expensive software.

---

## 🚀 Features

- Bulk email sending from a CSV file  
- Personalized messages using dynamic fields (e.g., `{name}`, `{amount}`, `{due_date}`)  
- SMTP support (Gmail, Outlook, business email)  
- Secure login with App Passwords  
- Automatic logging of all sent, skipped, and failed emails  
- Simple configuration via `config.json`  
- Clean folder structure + easy to extend  
- Runs on Linux, macOS, and Windows  

---

## 📂 Project Structure

```plaintext
email_sender_tool/
├─ send_emails.py
├─ config.json                # Your private settings (not included in repo)
├─ config_example.json        # Public safe version
├─ contacts_example.csv       # Example input file
├─ logs/
│  └─ send_log.csv            # Generated after running the script
└─ README.md
```

---

## 🛠️ Requirements 

- Python 3.10+  
- Internet connection  
- Valid SMTP email account (Gmail, Outlook, etc.)  
- Gmail users must use App Passwords  

No external Python libraries required — everything is built using the standard library.

---

## 📥 Preparing Your CSV File

Example:

```csv
name,email,amount,due_date
Alice Smith,alice@example.com,120.50,2025-12-01
Bob Johnson,bob@example.com,89.99,2025-12-05
Charlie Brown,charlie@example.com,200,2025-12-10
```
Each column becomes available inside your email templates.

---

## ✅ Configuration



Copy `config_example.json` → rename to `config.json`, then edit:

```json
{
  "SMTP_HOST": "smtp.gmail.com",
  "SMTP_PORT": 587,
  "SMTP_USER": "your_email@gmail.com",
  "SMTP_PASSWORD": "YOUR_APP_PASSWORD",
  "FROM_NAME": "Your Business Name",
  "SUBJECT_TEMPLATE": "Payment reminder for {name}",
  "BODY_TEMPLATE": "Hello {name},\n\nThis is a friendly reminder that your payment of {amount} is due on {due_date}.\n\nBest regards,\nYour Company"
}
```

---

# 🔐 Gmail Security Notice

Gmail requires:

- 2-Step Verification enabled  
- App Password (Do NOT use your real password)

---

## ▶️ How to Run

Open a terminal in the folder and run:

```bash
python3 send_emails.py
```

Emails will be sent to every contact in your CSV.
```bash
A log file will be created at:
  logs/send_log.csv
Containing:
  timestamp,email,status,error
```

---

## 🧪 Testing

Before sending real emails:

1. Add only your own email(s) to `contacts_example.csv`  
2. Run the tool  
3. Confirm that everything looks correct in your inbox  

---

## 🔧 Future Enhancements (Optional)

These can be added for clients who want more advanced features:

- HTML email support  
- Attachments  
- Scheduling (daily/weekly sends)  
- GUI version  
- API version  
- Excel (.xlsx) support  
- Multi-template system  
- Integration with payment systems  

---

## 💼 Perfect For

- Small businesses  
- Freelancers  
- Accountants  
- Marketing teams  
- Customer support  
- Automated notifications  
- Anyone who needs fast, personalized bulk emailing  

---

## 🧑‍💻 Author

This tool was developed as part of a professional automation portfolio focused on Python, data workflows, and backend logic.
