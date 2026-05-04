from tiktok_dmm import CONFIG, TikTokDMSender


def input_data():
        username = input("enter your email: ")
        password = input("enter your TikTok password: ")
        message = input("enter the message you want to send: ")
        target_usernames = []
        while True:
           nama_akun = input("enter the username you want to send a message to (without @): ")
           if nama_akun:
               target_usernames.append(nama_akun)
           else:
               print("Username cannot be empty. Please try again.")
           continue_input = input("do you want to add another user? (y/n): ")
           if continue_input.lower() != 'y':
               break

        return username, password, message, target_usernames

username, password, message, target_usernames = input_data()
CONFIG["email"]            = username
CONFIG["password"]         = password
CONFIG["message"]          = message
CONFIG["target_usernames"] = target_usernames

sender = TikTokDMSender()
sender.run()
 