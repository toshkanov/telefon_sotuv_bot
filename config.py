from environs import Env

env = Env()
env.read_env()

TOKEN = env.str("BOT_TOKEN") # .env faylida token turibdi
ADMINS = env.list("ADMINS") # .env da admin ID lari

# KANAL SOZLAMALARI (O'zingiznikiga almashtiring)
CHANNEL_ID = "@toshkanov_bozor"  # Kanalingiz userneymi (@ bilan)
CHANNEL_URL = "https://t.me/toshkanov_bozor" # Kanal havolasi
ADMIN_USERNAME = "@jav0hir_iq" # Sizning lichkangiz