import json
import re
import streamlit as st
from history_manager import load_user_history, save_user_history

@st.cache_data(ttl=300)
def load_users():
    try:
        with open('users.json', 'r') as file:
            data = json.load(file)
            return data.get('users', [])
    except FileNotFoundError:
        save_users([])
        return []
    except json.JSONDecodeError:
        st.error("Invalid JSON format in users.json!")
        return []

def save_users(users):
    try:
        with open('users.json', 'w') as file:
            json.dump({"users": users}, file, indent=2)
        load_users.clear()
    except Exception as e:
        st.error(f"Error saving users: {str(e)}")

def validate_login(username, password):
    users = load_users()
    for user in users:
        if user['username'].lower() == username.lower():
            if user['password'] == password:  # Compare plain text password
                return True
    return False

def get_user(username):
    users = load_users()
    return next((u for u in users if u['username'].lower() == username.lower()), None)

def is_admin_user(username):
    user = get_user(username)
    return user.get('is_admin', False) if user else False

def update_user_profile(username, new_email, new_password):
    users = load_users()
    user = next((u for u in users if u['username'].lower() == username.lower()), None)
    if not user:
        return False, "User not found!"
    
    if new_email:
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, new_email):
            return False, "Invalid email format!"
        if any(u['email'] == new_email and u['username'].lower() != username.lower() for u in users):
            return False, "Email already in use!"
        user['email'] = new_email
    
    if new_password:
        user['password'] = new_password  # Store plain text password
    
    save_users(users)
    return True, "Profile updated successfully!"

def delete_user(admin_username, target_username):
    if admin_username.lower() == target_username.lower():
        return False, "Cannot delete your own account!"
    
    users = load_users()
    user = next((u for u in users if u['username'].lower() == target_username.lower()), None)
    if not user:
        return False, "User not found!"
    
    users.remove(user)
    save_users(users)
    
    history = load_user_history()
    history_entry = next((h for h in history if h['username'].lower() == target_username.lower()), None)
    if history_entry:
        history.remove(history_entry)
        save_user_history(history)
    
    return True, f"User {target_username} deleted successfully!"

def toggle_admin_status(admin_username, target_username):
    if admin_username.lower() == target_username.lower():
        return False, "Cannot change your own admin status!"
    
    users = load_users()
    user = next((u for u in users if u['username'].lower() == target_username.lower()), None)
    if not user:
        return False, "User not found!"
    
    user['is_admin'] = not user.get('is_admin', False)
    save_users(users)
    status = "promoted to admin" if user['is_admin'] else "demoted to regular user"
    return True, f"User {target_username} {status}!"

def reset_user_usage(username):
    users = load_users()
    user = next((u for u in users if u['username'].lower() == username.lower()), None)
    if not user:
        return False, "User not found!"
    user['usage_count'] = 0
    save_users(users)
    return True, f"Usage count reset for {username}"

def reset_all_usage(admin_username):
    users = load_users()
    updated = False
    for user in users:
        if not user.get('is_admin', False):
            user['usage_count'] = 0
            updated = True
    if updated:
        save_users(users)
        return True, "All non-admin usage counts reset!"
    return True, "No usage counts to reset."

def increment_usage_count(username):
    users = load_users()
    user = next((u for u in users if u['username'].lower() == username.lower()), None)
    if user and not user.get('is_admin', False):
        user['usage_count'] = user.get('usage_count', 0) + 1
        save_users(users)
    return True

def get_usage_count(username):
    user = get_user(username)
    if user:
        return "Unlimited" if user.get('is_admin', False) else user.get('usage_count', 0)
    return 0

def load_pending_users():
    try:
        with open('pending_users.json', 'r') as file:
            data = json.load(file)
            return data.get('pending_users', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def approve_pending_user(admin_username, target_username):
    pending_users = load_pending_users()
    user = next((u for u in pending_users if u['username'].lower() == target_username.lower()), None)
    if not user:
        return False, "Pending user not found!"
    
    users = load_users()
    if any(u['username'].lower() == user['username'].lower() or u['email'] == user['email'] for u in users):
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
    
    return True, f"User {target_username} approved!"

def reject_pending_user(admin_username, target_username):
    pending_users = load_pending_users()
    user = next((u for u in pending_users if u['username'].lower() == target_username.lower()), None)
    if not user:
        return False, "Pending user not found!"
    
    pending_users.remove(user)
    with open('pending_users.json', 'w') as file:
        json.dump({"pending_users": pending_users}, file, indent=2)
    
    return True, f"User {target_username} rejected!"