import telebot, sqlite3, json
from telebot.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB

b = telebot.TeleBot("8770255847:AAFzI_4wLNTmJ5Mzbk7J12qhW55MhYgQ-Dk")
c = sqlite3.connect("u.db", check_same_thread=False)
x = c.cursor()
x.execute("CREATE TABLE IF NOT EXISTS u(id INTEGER PRIMARY KEY, un TEXT, fn TEXT)")

def au(u):
    try:
        x.execute("INSERT OR IGNORE INTO u VALUES(?,?,?)", (u.id, u.username, u.first_name))
        c.commit()
    except: pass

def mk(i):
    m = IKM()
    m.add(IKB(f"📋 Copy ID {i}", callback_data=f"c_{i}"))
    m.add(IKB("🔎 Check Another", url="https://t.me/HQR_ID?gited=gited"))
    return m

# Nidaamka Custom JSON ee Xallinaya Cillad kasta oo Badhamada ah
def km(i):
    kbd = []
    if i == 6903972630: # Admin
        kbd.append([{"text": "👥 Xogta"}, {"text": "📢 Post"}, {"text": "☢️ Raadi"}, {"text": "🔗 Ku xidh"}])
    
    kbd.append([
        {"text": "👤 User", "request_users": {"request_id": 1, "user_is_bot": False, "request_photo": True, "request_name": True, "request_username": True, "max_quantity": 1}},
        {"text": "⭐ Premium", "request_users": {"request_id": 2, "user_is_premium": True, "request_photo": True, "request_name": True, "request_username": True, "max_quantity": 1}},
        {"text": "🤖 Bot", "request_users": {"request_id": 3, "user_is_bot": True, "request_photo": True, "request_name": True, "request_username": True, "max_quantity": 1}}
    ])
    
    kbd.append([
        {"text": "👥 Group", "request_chat": {"request_id": 4, "chat_is_channel": False, "request_title": True, "request_username": True, "request_photo": True}},
        {"text": "📢 Channel", "request_chat": {"request_id": 5, "chat_is_channel": True, "request_title": True, "request_username": True, "request_photo": True}},
        {"text": "💬 Forum", "request_chat": {"request_id": 6, "chat_is_channel": False, "chat_is_forum": True, "request_title": True, "request_username": True, "request_photo": True}}
        
    ])
    
    kbd.append([
    {"text": "👥 My Group", "request_chat": {"request_id": 7, "chat_is_channel": False, "chat_is_created": True, "request_title": True, "request_username": True, "request_photo": True}},
    {"text": "📢 My Channel", "request_chat": {"request_id": 8, "chat_is_channel": True, "chat_is_created": True, "request_title": True, "request_username": True, "request_photo": True}},
    {"text": "💬 My Forum", "request_chat": {"request_id": 9, "chat_is_channel": False, "chat_is_forum": True, "chat_is_created": True, "request_title": True, "request_username": True, "request_photo": True}},

])

    
    return json.dumps({"keyboard": kbd, "resize_keyboard": True})

@b.message_handler(commands=["start"])
def st(m):
    au(m.from_user)
    b.send_message(m.chat.id, "🔎 Welcome to HQR ID!Choose the buttons below to search for information, or forward me a message/profile.:", reply_markup=km(m.from_user.id))
    process_info(m)

@b.message_handler(content_types=["text", "photo", "video", "document", "audio", "voice", "sticker", "animation", "user_shared", "chat_shared", "users_shared"])
def h(m):
    au(m.from_user)
    t = m.text
    i = m.from_user.id
    
    if i == 6903972630 and t:
        if t == "👥 Xogta":
            x.execute("SELECT * FROM u")
            r = x.fetchall()
            o = "👥 Xogta:\n"
            for j in r: o += f"<code>{j[0]}</code> | @{j[1]}\n"
            return b.reply_to(m, o[:4000], parse_mode="HTML")
        if t == "📢 Post":
            return b.register_next_step_handler(b.reply_to(m, "Soo dir fariinta:"), br)
        if t == "🔗 Ku xidh":
            return b.reply_to(m, "⚠️ Kuma shaqeeyo Termux (Pyrogram baa loo baahanyahay).")
            
    if t == "/start": return
    process_info(m)

def process_info(m):
    is_u = True; ti = None; un = "Qariyan"; nm = "Unknown"; lc = "🔒 Hidden"
    bi = "🔒 Hidden"; photo_file = None; hp = False; photo_status = "🔒 Hidden"
    
    # Nidaamkan wuxuu si toos ah fariinta JSON uga dhuuqayaa sawirada lasoo wadaagay
    msg_json = getattr(m, "json", {})
    us_data = msg_json.get("users_shared") or msg_json.get("user_shared")
    cs_data = msg_json.get("chat_shared")
    
    if us_data:
        is_u = True
        if "users" in us_data:
            user_info = us_data["users"][0]
            ti = user_info.get("user_id")
            nm = user_info.get("first_name", "Shared User")
            if "username" in user_info: un = f"@{user_info['username']}"
            if "photo" in user_info and user_info["photo"]:
                photo_file = user_info["photo"][-1]["file_id"]
                hp = True; photo_status = "🖼️ 1 Photo"
        else:
            ti = us_data.get("user_id")
    elif cs_data:
        is_u = False
        ti = cs_data.get("chat_id")
        nm = cs_data.get("title", "Shared Chat")
        if "username" in cs_data: un = f"@{cs_data['username']}"
        if "photo" in cs_data and cs_data["photo"]:
            photo_file = cs_data["photo"][-1]["file_id"]
            hp = True; photo_status = "🖼️ 1 Photo"
    elif m.forward_from_chat: 
        c_chat = m.forward_from_chat; ti = c_chat.id
        un = f"@{c_chat.username}" if c_chat.username else "Qariyan"; nm = c_chat.title; is_u = False
    elif getattr(m, "forward_sender_name", None): 
        return b.reply_to(m, f"🔎 TELEGRAM ID CHECK\n\n👤 Name: {m.forward_sender_name}\n🆔 🔒 Hidden (Privacy)\n\n⚠️ This person has hidden their information, so neither their ID nor their profile picture can be retrieved.")
    elif m.forward_from: 
        u_fwd = m.forward_from; ti = u_fwd.id
        un = f"@{u_fwd.username}" if u_fwd.username else "Qariyan"; nm = u_fwd.first_name; lc = u_fwd.language_code or "🔒 Hidden"
    else: 
        u_frm = m.from_user; ti = u_frm.id
        un = f"@{u_frm.username}" if u_frm.username else "Qariyan"; nm = u_frm.first_name; lc = u_frm.language_code or "🔒 Hidden"

    if not ti: return

    ci = None
    try:
        ci = b.get_chat(ti)
        if getattr(ci, "first_name", None) and not hp: nm = ci.first_name
        elif getattr(ci, "title", None) and not hp: nm = ci.title
        if getattr(ci, "username", None) and un == "Qariyan": un = f"@{ci.username}"
        if getattr(ci, "type", None) and ci.type in ["channel", "group", "supergroup"]: is_u = False
        
        if getattr(ci, "bio", None): 
            sb = str(ci.bio).replace('<', '&lt;').replace('>', '&gt;')
            bi = f"<code>{sb}</code>"
        elif getattr(ci, "description", None): 
            sd = str(ci.description[:50]).replace('<', '&lt;').replace('>', '&gt;')
            bi = f"<code>{sd}...</code>"
    except: pass
    
    # Qofka sawirkiisa haddii laga waayo JSON
    if is_u and not hp:
        try:
            p = b.get_user_profile_photos(ti, limit=1)
            if p and p.total_count > 0:
                photo_file = p.photos[0][-1].file_id
                hp = True
                photo_status = f"🖼️ {p.total_count} Photo(s)"
        except: pass

    # Channel/Group sawirkiisa soo dejin (Download) haddii JSON laga waayo
    if not hp and ci and getattr(ci, "photo", None):
        try:
            file_info = b.get_file(ci.photo.big_file_id)
            photo_file = b.download_file(file_info.file_path)
            hp = True
            photo_status = "🖼️ 1 Photo"
        except: pass

    cc = lc.upper() if lc != "🔒 Hidden" else "🔒 Hidden"
    nm = str(nm).replace('<', '&lt;').replace('>', '&gt;')
    
    caption = f"""🔎 TELEGRAM ID CHECK

👤 Name: {nm}
🔗 Username: {un}
🆔 <code>{ti}</code> | {len(str(ti))} digits

🌐 Language/Region: {cc}
🖼️ Profile Picture: {photo_status}
📝 Bio/Desc: {bi}
🎂 Birthday: 10/8

<blockquote>This data helps you:
• understand the real age of the account
• assess profile reliability
• avoid risks in deals and communication</blockquote>"""

    if hp and photo_file:
        try:
            b.send_photo(m.chat.id, photo_file, caption=caption, reply_markup=mk(ti), parse_mode="HTML")
            return
        except: pass
            
    b.reply_to(m, caption, reply_markup=mk(ti), parse_mode="HTML")

def br(m):
    x.execute("SELECT id FROM u")
    s = 0
    for r in x.fetchall():
        try:
            b.copy_message(r[0], m.chat.id, m.message_id)
            s += 1
        except: pass
    b.reply_to(m, f"✅ Loo diray {s} qof.")

@b.callback_query_handler(func=lambda c: True)
def ans(cq):
    if cq.data.startswith("c_"):
        b.answer_callback_query(cq.id, text=cq.data.split("_")[1], show_alert=True)

b.polling()
