import logging
import speedtest
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Logging setup (Error බලාගැනීමට)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Speed Test Bot එකට සාදරයෙන් පිළිගනිමු! /test ලෙස type කර වේගය පරීක්ෂා කරන්න.")

async def run_speedtest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_message = await update.message.reply_text("⚡ Speed test එක ආරම්භ කළා... මොහොතක් රැඳී සිටින්න.")
    
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        
        # Download සහ Upload speed මැනීම
        download_speed = st.download() / 1_000_000  # Mbps වලට හැරවීම
        upload_speed = st.upload() / 1_000_000
        ping = st.results.ping
        
        report = (
            "📊 **Render Server Speed Report (Ookla)**\n\n"
            f"📥 **Download:** {download_speed:.2f} Mbps\n"
            f"📤 **Upload:** {upload_speed:.2f} Mbps\n"
            f"📡 **Ping:** {ping} ms\n\n"
            "📍 *Location:* Render Cloud Server"
        )
        
        await status_message.edit_text(report, parse_mode='Markdown')
        
    except Exception as e:
        await status_message.edit_text(f"❌ Error එකක් සිදුවුණා: {str(e)}")

if __name__ == '__main__':
    # BOT_TOKEN එක මෙතනට ලබා දෙන්න
    application = ApplicationBuilder().token('8028678734:AAGJxsL-tljE0FWa3MihPQoa7SzUXmhjhPk').build()
    
    start_handler = CommandHandler('start', start)
    test_handler = CommandHandler('test', run_speedtest)
    
    application.add_handler(start_handler)
    application.add_handler(test_handler)
    
    application.run_polling()
  
