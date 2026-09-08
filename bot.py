import telebot, sqlite3
from telebot.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB, ReplyKeyboardMarkup as RKM, KeyboardButton as KB, KeyboardButtonRequestUser as RU, KeyboardButtonRequestChat as RC

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
    m.add(IKB("🔎 Check Another", url="https://t.me/HQR_ID?start=start"))
    return m

def km(i):
    k = RKM(resize_keyboard=True)
    if i == 6903972630:
        k.row("👥 Xogta", "📢 Post", "🔗 Ku xidh")
    k.row(KB("👤 User", request_user=RU(1, user_is_bot=False)), KB("⭐ Premium", request_user=RU(2, user_is_premium=True)), KB("🤖 Bot", request_user=RU(3, user_is_bot=True)))
    k.row(KB("👥 Group", request_chat=RC(4, chat_is_channel=False)), KB("📢 Channel", request_chat=RC(5, chat_is_channel=True)), KB("💬 Forum", request_chat=RC(6, chat_is_channel=False, chat_is_forum=True)))
    k.row(KB("👥 My Group", request_chat=RC(7, chat_is_channel=False)), KB("📢 My Channel", request_chat=RC(8, chat_is_channel=True)), KB("💬 My Forum", request_chat=RC(9, chat_is_channel=False, chat_is_forum=True)))
    return k

@b.message_handler(commands=["start"])
def st(m):
    au(m.from_user)
    b.send_message(m.chat.id, "🔎 Soo dhawoow! Dooro nooca xogta aad baarayso:", reply_markup=km(m.from_user.id))
    h(m)

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
            
    is_u = True; ti = None; un = "Qariyan"; nm = "Unknown"; lc = "🔒 Hidden"
    
    us = getattr(m, "user_shared", None) or getattr(m, "users_shared", None)
    cs = getattr(m, "chat_shared", None)
    
    if us:
        ti = getattr(us, "user_id", None)
        if not ti and hasattr(us, "users"): ti = us.users[0].user_id
        nm = "Shared User"
    elif cs:
        ti = cs.chat_id; nm = "Shared Chat"; is_u = False
    elif m.forward_from_chat:
        c_chat = m.forward_from_chat; ti = c_chat.id
        un = f"@{c_chat.username}" if c_chat.username else "Qariyan"; nm = c_chat.title; is_u = False
    elif getattr(m, "forward_sender_name", None):
        return b.reply_to(m, f"🔎 TELEGRAM ID CHECK\n\n👤 Name: {m.forward_sender_name}\n🆔 🔒 Hidden (Privacy)\n\n⚠️ Qofkan wuxuu qarsaday xogtiisa.")
    elif m.forward_from:
        u_fwd = m.forward_from; ti = u_fwd.id
        un = f"@{u_fwd.username}" if u_fwd.username else "Qariyan"; nm = u_fwd.first_name; lc = u_fwd.language_code or "🔒 Hidden"
    else:
        if t == "/start": return
        u_frm = m.from_user; ti = u_frm.id
        un = f"@{u_frm.username}" if u_frm.username else "Qariyan"; nm = u_frm.first_name; lc = u_frm.language_code or "🔒 Hidden"
        
    bi = bd = "🔒 Hidden"; hp = False; fi = None
    
    try:
        ci = b.get_chat(ti)
        if getattr(ci, "first_name", None): nm = ci.first_name
        elif getattr(ci, "title", None): nm = ci.title
        if getattr(ci, "username", None): un = f"@{ci.username}"
        if getattr(ci, "bio", None): bi = f"<code>{ci.bio}</code>"
        elif getattr(ci, "description", None): bi = f"<code>{ci.description[:50]}...</code>"
        if getattr(ci, "birthdate", None):
            d = ci.birthdate
            bd = f"<code>{2026-d.year} Years ({d.year})</code>" if getattr(d, "year", None) else f"<code>{d.day}/{d.month}</code>"
        if getattr(ci, "photo", None):
            fi = ci.photo.big_file_id; hp = True
    except: pass
    
    if is_u and not hp:
        try:
            p = b.get_user_profile_photos(ti, limit=1)
            if p and p.total_count > 0:
                fi = p.photos[0][-1].file_id; hp = True
        except: pass
        
    ps = "🖼️ 1 Photo" if hp else "🔒 Hidden"
    cc = lc.upper() if lc != "🔒 Hidden" else "🔒 Hidden"
    
    mt = f"""🔎 TELEGRAM ID CHECK\n\n👤 Name: {nm}\n🔗 Username: {un}\n🆔 <code>{ti}</code> | {len(str(ti))} digits\n\n 🌐 Language/Region: {cc}\n 🖼️ Profile Picture: {ps}\n 📝 Bio/Desc: {bi}\n 🎂 Birthday: {bd}\n\n<blockquote>This data helps you:\n• understand the real age of the account\n• assess profile reliability\n• avoid risks in deals and communication</blockquote>\n\nDetailed info in HQT ID"""
    
    try:
        if hp: b.send_photo(m.chat.id, fi, caption=mt, reply_markup=mk(ti), parse_mode="HTML")
        else: b.reply_to(m, mt, reply_markup=mk(ti), parse_mode="HTML")
    except: pass

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
