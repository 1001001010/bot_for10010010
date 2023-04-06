import configparser

config = configparser.ConfigParser()
config.read("config.ini")
BOT_TOKEN = config["settings"]["token"]
admin_channel_id = config["settings"]["admin_channel_id"]
admins = config["settings"]["admin_id"]

if "," in admins:
    admins = admins.split(",")
else:
    if len(admins) >= 1:
        admins = [admins]
    else:
        admins = []
        print("***** Вы не указали админ ID *****")


