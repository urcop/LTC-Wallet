from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
SUPPORT_TOKEN = env.str("SUPPORT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("ip")
DB_USER = env.str('DB_USER')
DB_PASS = env.str('DB_PASS')
db = env.str('db')
