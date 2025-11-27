import csv  # to read the contacts file
import smtplib  # to send emails via SMTP
import ssl  # to secure the connection
import json  # to read configuration from a JSON file
from email.message import EmailMessage  # to build the email object
from datetime import datetime, timezone  # to timestamp the log in UTC
from pathlib import Path  # to handle paths safely


def load_config(config_path: str = "config.json") -> dict:
    """
    Load SMTP and template configuration from a JSON file.
    Falls back to 'config_example.json' if 'config.json' does not exist.
    """
    config_file = Path(config_path)

    if not config_file.exists():
        # if real config is missing, use the example (for demo / testing)
        print(f"[INFO] {config_path} not found, using config_example.json instead.")
        config_file = Path("config_example.json")

    with config_file.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_contacts(csv_path: str) -> list[dict]:
    """
    Load contacts from a CSV file and return a list of dictionaries, 
    where each dict represents one row (one contact).
    """
    contacts = []
    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            contacts.append(row)
    return contacts


def build_message(config: dict, contact: dict) -> EmailMessage:
    """
    Build a personalized email message for a single contact
    using templates from the config and fields from the contact row.
    """
    msg = EmailMessage()

    # fill subject and body templates with the contact info
    subject = config["SUBJECT_TEMPLATE"].format(**contact)
    body = config["BODY_TEMPLATE"].format(**contact)

    from_name = config.get("FROM_NAME", config["SMTP_USER"])
    from_email = config["SMTP_USER"]
    to_email = contact["email"]

    # 'From' field with name + email
    msg["From"] = f"{from_name} <{from_email}>"
    msg["To"] = to_email
    msg["Subject"] = subject

    # set the email body as plain text
    msg.set_content(body)

    return msg


def send_all_emails(config_path: str, contacts_path: str, log_path: str = "logs/send_log.csv") -> None:
    """
    Main function:
    - loads config and contacts
    - connects to SMTP server
    - sends all emails one by one
    - writes a log file with results
    """
    config = load_config(config_path)
    contacts = load_contacts(contacts_path)

    # make sure logs directory exists
    log_file = Path(log_path)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # prepare secure SMTP connection
    context = ssl.create_default_context()

    smtp_host = config["SMTP_HOST"]
    smtp_port = int(config["SMTP_PORT"])
    smtp_user = config["SMTP_USER"]
    smtp_password = config["SMTP_PASSWORD"]

    print(f"[INFO] Connecting to SMTP server {smtp_host}:{smtp_port} ...")

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls(context=context)  # upgrade connection to TLS
        server.login(smtp_user, smtp_password)
        print("[INFO] Logged in successfully.")

        # open log file for writing
        with log_file.open("w", newline="", encoding="utf-8") as logfile:
            log_writer = csv.writer(logfile)
            # write header row for the log
            log_writer.writerow(["timestamp", "email", "status", "error"])

            # send email to each contact
            for contact in contacts:
                email_address = contact.get("email", "").strip()
                if not email_address:
                    print("[WARN] Skipping contact with missing email:", contact)
                    log_writer.writerow([datetime.now(timezone.utc).isoformat(), "", "skipped", "missing email"])
                    continue

                msg = build_message(config, contact)

                try:
                    server.send_message(msg)
                    print(f"[OK] Sent email to {email_address}")
                    log_writer.writerow([datetime.now(timezone.utc).isoformat()
, email_address, "sent", ""])
                except Exception as e:
                    print(f"[ERROR] Failed to send to {email_address}: {e}")
                    log_writer.writerow([datetime.now(timezone.utc).isoformat(), email_address, "failed", str(e)])

# Configuration paths:
# - 'config.json' must be created by the user by copying 'config_example.json'
# - This file contains private SMTP credentials and SHOULD NOT be committed to GitHub
# - 'contacts_example.csv' is an example file safe to include in public repositories
# - The script will auto-create the 'logs' directory if it does not exist

if __name__ == "__main__":
    CONFIG_PATH = "config.json"              # User-provided config file
    CONTACTS_PATH = "contacts_example.csv"   # Example contacts file
    LOG_PATH = "logs/send_log.csv"           # Log file path

    send_all_emails(CONFIG_PATH, CONTACTS_PATH, LOG_PATH)
    
