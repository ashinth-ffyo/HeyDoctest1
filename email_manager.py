import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
import os
from dotenv import load_dotenv
import uuid
import datetime
import pytz
import logging
import json

logging.basicConfig(level=logging.INFO, filename='email.log', format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

def send_diagnosis_email(recipient_email, username, disease, symptoms, treatment_pdf_data, illness_pdf_data):
    try:
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", 587))
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        logo_path = os.getenv("LOGO_PATH", "heydoc-high-resolution-logo.png")

        if not sender_email or not sender_password:
            logging.error("Missing SMTP credentials")
            return False, "Email configuration is missing."

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = f"HeyDoc Diagnosis: {disease}"

        symptoms_list = "</li><li>".join(symptoms) if symptoms else "None reported"
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; color: #0f172a; background-color: #f8fafc; padding: 20px; }}
                .container {{ max-width: 600px; margin: auto; background: #ffffff; border-radius: 12px; padding: 20px; }}
                .header {{ background-color: #3b82f6; color: #ffffff; padding: 15px; text-align: center; border-radius: 12px 12px 0 0; }}
                .header img {{ max-width: 150px; }}
                .content {{ padding: 20px; }}
                h2 {{ color: #1e293b; }}
                ul {{ list-style-type: none; padding: 0; }}
                li {{ padding: 5px 0; }}
                .footer {{ text-align: center; color: #94a3b8; font-size: 0.85rem; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <img src="cid:logo" alt="HeyDoc Logo">
                    <h2>Diagnosis Report</h2>
                </div>
                <div class="content">
                    <p>Dear {username},</p>
                    <p>Your recent HeyDoc assessment results:</p>
                    <h3>Condition: {disease}</h3>
                    <p>Symptoms:</p>
                    <ul><li>{symptoms_list}</li></ul>
                    <p>Attached: Treatment Plan and Illness Info PDFs.</p>
                    <p><em>Consult a healthcare provider for medical advice.</em></p>
                </div>
                <div class="footer">
                    © 2023 HeyDoc™. All rights reserved.
                </div>
            </div>
        </body>
        </html>
        """
        msg.attach(MIMEText(html_body, "html"))

        if os.path.exists(logo_path):
            with open(logo_path, 'rb') as img:
                logo = MIMEImage(img.read())
                logo.add_header('Content-ID', '<logo>')
                msg.attach(logo)
        else:
            logging.warning(f"Logo not found at {logo_path}")

        for pdf_data, name in [
            (treatment_pdf_data, f"HeyDoc_Treatment_Plan_{disease}.pdf"),
            (illness_pdf_data, f"HeyDoc_Illness_Info_{disease}.pdf")
        ]:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(pdf_data.getvalue())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={name}")
            msg.attach(part)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        logging.info(f"Diagnosis email sent to {recipient_email}")
        return True, "Email sent successfully!"
    except Exception as e:
        logging.error(f"Failed to send diagnosis email to {recipient_email}: {str(e)}")
        return False, f"Failed to send email: {str(e)}"

def send_confirmation_email(recipient_email, username, token):
    try:
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", 587))
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        logo_path = os.getenv("LOGO_PATH", "heydoc-high-resolution-logo.png")

        if not sender_email or not sender_password:
            logging.error("Missing SMTP credentials")
            return False, "Email configuration is missing."

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = "HeyDoc Account Confirmation"

        confirmation_url = f"http://localhost:8501/?confirm=true&username={username}&token={token}"
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; color: #0f172a; background-color: #f8fafc; padding: 20px; }}
                .container {{ max-width: 600px; margin: auto; background: #ffffff; border-radius: 12px; padding: 20px; }}
                .header {{ background-color: #3b82f6; color: #ffffff; padding: 15px; text-align: center; border-radius: 12px 12px 0 0; }}
                .header img {{ max-width: 150px; }}
                .content {{ padding: 20px; }}
                a.button {{ display: inline-block; padding: 10px 20px; background-color: #3b82f6; color: #ffffff; text-decoration: none; border-radius: 8px; }}
                .footer {{ text-align: center; color: #94a3b8; font-size: 0.85rem; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <img src="cid:logo" alt="HeyDoc Logo">
                    <h2>Confirm Your Account</h2>
                </div>
                <div class="content">
                    <p>Dear {username},</p>
                    <p>Please confirm your HeyDoc account:</p>
                    <a href="{confirmation_url}" class="button">Confirm Account</a>
                    <p>Or use this link: <a href="{confirmation_url}">{confirmation_url}</a></p>
                    <p>Token: {token}</p>
                    <p>Expires in 24 hours.</p>
                </div>
                <div class="footer">
                    © 2023 HeyDoc™. All rights reserved.
                </div>
            </div>
        </body>
        </html>
        """
        msg.attach(MIMEText(html_body, "html"))

        if os.path.exists(logo_path):
            with open(logo_path, 'rb') as img:
                logo = MIMEImage(img.read())
                logo.add_header('Content-ID', '<logo>')
                msg.attach(logo)
        else:
            logging.warning(f"Logo not found at {logo_path}")

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        logging.info(f"Confirmation email sent to {recipient_email}")
        return True, "Confirmation email sent!"
    except Exception as e:
        logging.error(f"Failed to send confirmation email to {recipient_email}: {str(e)}")
        return False, f"Failed to send confirmation email: {str(e)}"

def generate_confirmation_token():
    return str(uuid.uuid4())

def store_pending_user(username, password, email, token):
    try:
        try:
            with open('pending_users.json', 'r') as file:
                data = json.load(file)
                pending_users = data.get('pending_users', [])
        except (FileNotFoundError, json.JSONDecodeError):
            pending_users = []

        if any(u['username'].lower() == username.lower() or u['email'] == email for u in pending_users):
            return False, "Username or email already pending confirmation!"
        
        timestamp = datetime.datetime.now(pytz.timezone('Asia/Colombo')).strftime("%Y-%m-%d %H:%M:%S")
        pending_users.append({
            "username": username,
            "password": password,  # Store plain text password
            "email": email,
            "token": token,
            "timestamp": timestamp
        })

        with open('pending_users.json', 'w') as file:
            json.dump({"pending_users": pending_users}, file, indent=2)
        
        logging.info(f"Stored pending user: {username}")
        return True, "Pending user stored!"
    except Exception as e:
        logging.error(f"Failed to store pending user {username}: {str(e)}")
        return False, f"Failed to store pending user: {str(e)}"

def confirm_user(username, token):
    try:
        with open('pending_users.json', 'r') as file:
            data = json.load(file)
            pending_users = data.get('pending_users', [])

        for user in pending_users:
            if user['username'].lower() == username.lower() and user['token'] == token:
                user_time = datetime.datetime.strptime(user['timestamp'], "%Y-%m-%d %H:%M:%S")
                user_time = pytz.timezone('Asia/Colombo').localize(user_time)
                current_time = datetime.datetime.now(pytz.timezone('Asia/Colombo'))
                if (current_time - user_time).total_seconds() > 24 * 3600:
                    logging.warning(f"Expired token for {username}")
                    return False, "Confirmation token expired."
                
                from user_manager import load_users, save_users
                users = load_users()
                if any(u['username'].lower() == username.lower() or u['email'] == user['email'] for u in users):
                    logging.warning(f"Username {username} or email already exists")
                    return False, "Username or email already exists!"
                
                users.append({
                    "username": user['username'],
                    "password": user['password'],  # Store plain text password
                    "email": user['email'],
                    "is_admin": False,
                    "usage_count": 0
                })
                save_users(users)
                
                pending_users.remove(user)
                with open('pending_users.json', 'w') as file:
                    json.dump({"pending_users": pending_users}, file, indent=2)
                
                logging.info(f"Confirmed user: {username}")
                return True, "Account confirmed!"
        
        logging.warning(f"Invalid confirmation for {username}")
        return False, "Invalid username or token."
    except Exception as e:
        logging.error(f"Failed to confirm user {username}: {str(e)}")
        return False, f"Failed to confirm user: {str(e)}"