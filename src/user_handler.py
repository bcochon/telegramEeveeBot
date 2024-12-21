import time
import threading

users = {}

class CustomUserInfo:
    spamCount = 0
    step = 0
    banned = False

    def __init__(self, uid):
        self.uid = uid

    def __str__(self):
        return f"User{self.id} (Banned={self.banned})"

    def count_msg(self):
        self.spamCount += 1
        if self.spamCount > 6:
            self.ban(60)
        thread = threading.Thread(target=self.uncount_msg)
        thread.start()

    def uncount_msg(self):
        time.sleep(30)
        self.spamCount -= 1

    def ban(self, banTime):
        self.banned = True
        print(f"Baneado usuario {self.uid}")
        thread = threading.Thread(target=self.unban, args=(banTime,))
        thread.start()

    def unban(self, banTime):
        time.sleep(banTime)
        self.banned = False


def register_user(uid):
    if uid not in users :
        newUser = CustomUserInfo(uid)
        users[uid] = newUser
    return users[uid]

def check_spam(id):
    if not check_banned(id) :
        spammer = register_user(id)
        spammer.count_msg()

def check_banned(id):
    return register_user(id).banned

def get_user_step(uid):
    if uid not in users:
        register_user(uid)
        logger.debug(f"New user {uid} detected, who hasn't used \"/start\" yet")
    return users[uid].step

def set_user_step(uid, step):
    users[uid].step = step