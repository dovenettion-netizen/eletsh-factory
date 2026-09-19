import os
import threading
import sqlite3
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("8808691912:AAEw85JKQ0D32TJK60o27SdGBBce5oB_MRQ")
FORCE = "@ElETSH"  # غيره بقناتك انت

# --- سيرفر عشان يفضل شغال 24 ساعة ---
flask_app = Flask(__name__)
@flask_app.route('/')
def home(): return "El ETSH Factory 24/7 👑"
def run_flask(): flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

# --- قاعدة بيانات ---
con = sqlite3.connect("factory.db", check_same_thread=False)
con.execute("CREATE TABLE IF NOT EXISTS bots (user_id INTEGER, token TEXT)")
con.commit()

async def check_join(user_id, context):
    try:
        m = await context.bot.get_chat_member(FORCE, user_id)
        return m.status not in ['left','kicked']
    except:
        return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not await check_join(uid, context):
        kb = [[InlineKeyboardButton(f"اشترك في {FORCE}", url=f"https://t.me/{FORCE[1:]}")],
              [InlineKeyboardButton("✅ تحققت", callback_data="check")]]
        await update.message.reply_text(f"👑 عشان تستخدم مصنع El ETSH\nلازم تشترك في {FORCE} الاول", reply_markup=InlineKeyboardMarkup(kb))
        return
    kb = [[InlineKeyboardButton("➕ انشاء بوت جديد", callback_data="create")],
          [InlineKeyboardButton("🤖 بوتاتي", callback_data="mybots")]]
    await update.message.reply_text("👑 **مصنع El ETSH لصناعة بوتات الازرار**\n\nارسل توكن البوت اللي جبته من @BotFather", reply_markup=InlineKeyboardMarkup(kb))

async def on_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "check":
        if await check_join(q.from_user.id, context):
            await q.message.delete()
            await start(update, context)
        else:
            await q.answer("❌ لسه مشتركتش", show_alert=True)
    elif q.data == "create":
        await q.message.reply_text("📤 ابعت توكن البوت من @BotFather")
    elif q.data == "mybots":
        cur = con.execute("SELECT token FROM bots WHERE user_id=?", (q.from_user.id,)).fetchall()
        if not cur: await q.message.reply_text("❌ معندكش بوتات")
        else: await q.message.reply_text(f"🤖 عندك {len(cur)} بوت")

async def on_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    token = update.message.text.strip()
    if ":" not in token or len(token) < 20:
        await update.message.reply_text("❌ التوكن غلط")
        return
    con.execute("INSERT INTO bots VALUES (?,?)", (update.effective_user.id, token))
    con.commit()
    await update.message.reply_text(f"🎉 تم انشاء بوتك بنجاح!\nتوكنه: `{token}`\n\nالمصنع شغال 24/7 👑", parse_mode="Markdown")

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(on_cb))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_token))
    print("El ETSH Factory is running... 24/7")
    app.run_polling()

if __name__ == "__main__":
    main()
