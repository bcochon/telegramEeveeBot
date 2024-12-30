import time
import threading

from utils import logger

users = {}
MAX_GROUP_CHAT_USES = (1, 12) # x in y hours

class CustomUserInfo:
    def __init__(self, uid):
        self.uid = uid
        self.spamCount = 0
        self.step = 0
        self.banned = False
        self.groupChatsUses = {}

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
        logger.info(f"Baneado usuario {self.uid}")
        thread = threading.Thread(target=self.unban, args=(banTime,))
        thread.start()

    def unban(self, banTime):
        time.sleep(banTime)
        self.banned = False

    def clean_groupchat_uses(self, cid, nowTime):
        if cid in self.groupChatsUses:
            uses = self.groupChatsUses[cid]
            return [u for u in uses if (nowTime - u) < 60*60*MAX_GROUP_CHAT_USES[1]]
        return []

    def groupchat_count(self, cid, time):
        uses = self.clean_groupchat_uses(cid, time)
        uses.append(time)
        self.groupChatsUses.update({cid : uses})
        logger.debug(f'User {self.uid} groupchat {cid} uses: {len(uses)}')

    def groupchat_limit_reached(self, cid):
        if cid in self.groupChatsUses:
            return (len(self.groupChatsUses[cid]) >= MAX_GROUP_CHAT_USES[0])
        return False


def register_user(uid: int) -> CustomUserInfo:
    if uid not in users :
        newUser = CustomUserInfo(uid)
        users[uid] = newUser
        logger.debug(f"New user {uid} detected, who hasn't used \"/start\" yet")
    return users[uid]

def check_spam(id):
    if not check_banned(id) :
        spammer = register_user(id)
        spammer.count_msg()

def check_banned(id):
    return register_user(id).banned

def get_user_step(uid):
    return register_user(uid).step

def set_user_step(uid, step):
     register_user(uid).step = step

def use_groupchat(uid: int, cid: int, time: int):
     register_user(uid).groupchat_count(cid, time)

def reached_limit(uid: int, cid: int) -> bool :
    return register_user(uid).groupchat_limit_reached(cid)