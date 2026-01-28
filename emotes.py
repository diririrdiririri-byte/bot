from highrise import BaseBot, User, Position, AnchorPosition
from highrise.models import SessionMetadata
from highrise.__main__ import *
import asyncio
import json
import os
import random
import time

# =============================================
# BOT AYARLARI - BURADAN DOLDURUN
# =============================================
BOT_OWNER_ID = "673a417cb7f0ffc582a43435"
ROOM_ID = "6942f77823105f519fc7e44a"
BOT_TOKEN = "ac81cb41a1d1e036bbf8292af0d75ec213d55862abb257ba4fdbafab4ebd1b6b"

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.prefix = "!"
        
        # Roller
        self.owners = [BOT_OWNER_ID]
        self.coowners = []
        self.senioradmins = []
        self.moderators = []
        self.designers = []
        self.vips = {}
        self.blocked_users = []
        self.subscribers = []
        
        # Teleport
        self.teleport_points = {}
        self.teleport_roles = {}
        
        # Emote
        self.active_emote_loops = {}
        self.custom_emotes = {}
        
        # Follow
        self.follow_mode = {}
        self.follow_tasks = {}
        
        # Flash
        self.flash_users = []
        
        # Freeze
        self.frozen_users = []
        self.freeze_positions = {}
        
        # Messages
        self.join_messages = {}
        self.leave_messages = {}
        self.loop_messages = {}
        self.loop_cooldown = 60
        self.loop_task = None
        self.loop_running = False
        
        # VIP
        self.vip_cost = 0
        self.vip_duration = "permanent"
        self.vip_join_messages = {}
        self.vip_leave_messages = {}
        
        # Warnings
        self.warnings = {}
        self.moderation_history = []
        
        # Broadcast
        self.invite_room_id = None
        
        # Bot Settings
        self.saved_position = None
        self.autotele_enabled = False
        self.command_aliases = {}
        
        # Emote listesi (224 emote)
        self.emotes = {
            "0": "idle_zombie", "zombie": "idle_zombie",
            "1": "emote-looping", "fairytwirl": "emote-looping",
            "2": "idle-floating", "fairyfloat": "idle-floating",
            "3": "emote-launch", "launch": "emote-launch",
            "4": "emote-cutesalute", "cutesalute": "emote-cutesalute",
            "5": "emote-salute", "atattention": "emote-salute",
            "6": "dance-tiktok11", "tiktok": "dance-tiktok11",
            "7": "emote-kissing-bound", "smooch": "emote-kissing-bound",
            "8": "dance-employee", "pushit": "dance-employee",
            "9": "emote-gift", "foryou": "emote-gift",
            "10": "dance-touch", "touch": "dance-touch",
            "11": "dance-kawai", "kawaii": "dance-kawai",
            "12": "emote-repose", "repose": "emote-repose",
            "13": "emote-sleigh", "sleigh": "emote-sleigh",
            "14": "emote-hyped", "hyped": "emote-hyped",
            "15": "dance-jinglebell", "jingle": "dance-jinglebell",
            "16": "idle-toilet", "gottago": "idle-toilet",
            "17": "emote-timejump", "timejump": "emote-timejump",
            "18": "idle-wild", "scritchy": "idle-wild",
            "19": "idle-nervous", "bitnervous": "idle-nervous",
            "20": "emote-iceskating", "iceskating": "emote-iceskating",
            "21": "emote-celebrate", "partytime": "emote-celebrate",
            "22": "emote-pose10", "arabesque": "emote-pose10",
            "23": "emote-shy2", "bashful": "emote-shy2",
            "24": "emote-headblowup", "revelations": "emote-headblowup",
            "25": "emote-creepycute", "watchyourback": "emote-creepycute",
            "26": "dance-creepypuppet", "creepypuppet": "dance-creepypuppet",
            "27": "dance-anime", "saunter": "dance-anime",
            "28": "emote-pose6", "surprise": "emote-pose6",
            "29": "emote-celebrationstep", "celebration": "emote-celebrationstep",
            "30": "dance-pinguin", "penguin": "dance-pinguin",
            "31": "emote-boxer", "boxer": "emote-boxer",
            "32": "idle-guitar", "airguitar": "idle-guitar",
            "33": "emote-stargaze", "stargaze": "emote-stargaze",
            "34": "emote-pose9", "ditzy": "emote-pose9",
            "35": "idle-uwu", "uwu": "idle-uwu",
            "36": "dance-wrong", "wrong": "dance-wrong",
            "37": "emote-fashionista", "fashion": "emote-fashionista",
            "38": "dance-icecream", "icecream": "dance-icecream",
            "39": "idle-dance-tiktok4", "sayso": "idle-dance-tiktok4",
            "40": "idle_zombie", "zombie2": "idle_zombie",
            "41": "emote-astronaut", "astronaut": "emote-astronaut",
            "42": "emote-punkguitar", "punk": "emote-punkguitar",
            "43": "emote-gravity", "zerogravity": "emote-gravity",
            "44": "emote-pose5", "beautiful": "emote-pose5",
            "45": "emote-pose8", "omg": "emote-pose8",
            "46": "idle-dance-casual", "casual": "idle-dance-casual",
            "47": "emote-pose1", "wink": "emote-pose1",
            "48": "emote-pose3", "fightme": "emote-pose3",
            "49": "emote-pose5", "icon": "emote-pose5",
            "50": "emote-cute", "cute": "emote-cute",
            "51": "emote-cutey", "cutey": "emote-cutey",
            "52": "emote-greedy", "greedy": "emote-greedy",
            "53": "dance-tiktok9", "viralgroove": "dance-tiktok9",
            "54": "dance-weird", "weird": "dance-weird",
            "55": "emote-tiktok10", "shuffle": "emote-tiktok10",
            "56": "emoji-gagging", "tummyache": "emoji-gagging",
            "57": "emoji-celebrate", "raise": "emoji-celebrate",
            "58": "dance-tiktok8", "savage": "dance-tiktok8",
            "59": "dance-blackpink", "blackpink": "dance-blackpink",
            "60": "emote-model", "model": "emote-model",
            "61": "dance-tiktok2", "dontstartnow": "dance-tiktok2",
            "62": "dance-pennywise", "pennywise": "dance-pennywise",
            "63": "emote-bow", "bow": "emote-bow",
            "64": "dance-russian", "russian": "dance-russian",
            "65": "emote-curtsy", "curtsy": "emote-curtsy",
            "66": "emote-snowball", "snowball": "emote-snowball",
            "67": "emote-hot", "hot": "emote-hot",
            "68": "emote-snowangel", "snowangel": "emote-snowangel",
            "69": "emote-charging", "charging": "emote-charging",
            "70": "dance-shoppingcart", "letsgoshopping": "dance-shoppingcart",
            "71": "emote-confused", "confusion": "emote-confused",
            "72": "idle-enthusiastic", "enthused": "idle-enthusiastic",
            "73": "emote-telekinesis", "telekinesis": "emote-telekinesis",
            "74": "emote-float", "float": "emote-float",
            "75": "emote-teleporting", "teleporting": "emote-teleporting",
            "76": "emote-swordfight", "swordfight": "emote-swordfight",
            "77": "emote-maniac", "maniac": "emote-maniac",
            "78": "emote-energyball", "energyball": "emote-energyball",
            "79": "emote-snake", "worm": "emote-snake",
            "80": "idle_singing", "singalong": "idle_singing",
            "81": "emote-frog", "frog": "emote-frog",
            "82": "dance-macarena", "macarena": "dance-macarena",
            "83": "emoji-kiss", "kiss": "emoji-kiss",
            "84": "emote-no", "shakehead": "emote-no",
            "85": "emote-sad", "sad": "emote-sad",
            "86": "emote-yes", "nod": "emote-yes",
            "87": "emote-laughing", "laugh": "emote-laughing",
            "88": "emote-hello", "hello": "emote-hello",
            "89": "emote-thumbsup", "thumbsup": "emote-thumbsup",
            "90": "mining-success", "miningfail": "mining-success",
            "91": "idle-loop-shy", "shy": "idle-loop-shy",
            "92": "fishing-pull", "fishingpull": "fishing-pull",
            "93": "emote-wave", "thewave": "emote-wave",
            "94": "emoji-angry", "angry": "emoji-angry",
            "95": "", "rough": "",
            "96": "fishing-idle", "fishingidle": "fishing-idle",
            "97": "", "dropped": "",
            "98": "mining-success", "miningsuccess": "mining-success",
            "99": "", "receivehappy": "",
            "100": "emote-cold", "cold": "emote-cold",
            "101": "fishing-cast", "fishingcast": "fishing-cast",
            "102": "idle-loop-sitfloor", "sit": "idle-loop-sitfloor",
            "103": "emote-tiktok10", "shuffledance": "emote-tiktok10",
            "104": "", "receivesad": "",
            "105": "emote-tired", "tired": "emote-tired",
            "106": "dance-hipshake", "hipshake": "dance-hipshake",
            "107": "dance-fruity", "fruity": "dance-fruity",
            "108": "dance-cheerleader", "cheer": "dance-cheerleader",
            "109": "dance-tiktok14", "magnetic": "dance-tiktok14",
            "110": "idle-howl", "nocturnal": "idle-howl",
            "111": "emote-howl", "moonlit": "emote-howl",
            "112": "emote-trampoline", "trampoline": "emote-trampoline",
            "113": "emote-attention", "attention": "emote-attention",
            "114": "sit-open", "laidback": "sit-open",
            "115": "emote-shrink", "shrink": "emote-shrink",
            "116": "emote-puppet", "puppet": "emote-puppet",
            "117": "dancee-aerobics", "pushups": "dancee-aerobics",
            "118": "dance-duckwalk", "duckwalk": "dance-duckwalk",
            "119": "dance-handsup", "handsup": "dance-handsup",
            "120": "dance-metal", "rockout": "dance-metal",
            "121": "dance-orangejuice", "orangejuice": "dance-orangejuice",
            "122": "dance-singleladies", "ringonit": "dance-singleladies",
            "123": "dance-smoothwalk", "smoothwalk": "dance-smoothwalk",
            "124": "dance-voguehands", "voguehands": "dance-voguehands",
            "125": "emoji-arrogance", "arrogance": "emoji-arrogance",
            "126": "emoji-give-up", "giveup": "emoji-give-up",
            "127": "emoji-hadoken", "fireball": "emoji-hadoken",
            "128": "emoji-halo", "levitate": "emoji-halo",
            "129": "emoji-lying", "lying": "emoji-lying",
            "130": "emoji-naughty", "naughty": "emoji-naughty",
            "131": "emoji-poop", "stinky": "emoji-poop",
            "132": "emoji-pray", "pray": "emoji-pray",
            "133": "emoji-punch", "punch": "emoji-punch",
            "134": "emoji-sick", "sick": "emoji-sick",
            "135": "emoji-smirking", "smirk": "emoji-smirking",
            "136": "emoji-sneeze", "sneeze": "emoji-sneeze",
            "137": "emoji-there", "point": "emoji-there",
            "138": "emote-death2", "collapse": "emote-death2",
            "139": "emote-disco", "disco": "emote-disco",
            "140": "emote-ghost-idle", "ghostfloat": "emote-ghost-idle",
            "141": "emote-handstand", "handstand": "emote-handstand",
            "142": "emote-kicking", "superkick": "emote-kicking",
            "143": "emote-panic", "panic": "emote-panic",
            "144": "emote-splitsdrop", "splits": "emote-splitsdrop",
            "145": "idle_layingdown", "attentive": "idle_layingdown",
            "146": "idle_layingdown2", "relaxed": "idle_layingdown2",
            "147": "emote-apart", "fallingapart": "emote-apart",
            "148": "emote-baseball", "homerun": "emote-baseball",
            "149": "emote-boo", "boo": "emote-boo",
            "150": "emote-bunnyhop", "bunnyhop": "emote-bunnyhop",
            "151": "emote-death", "revival": "emote-death",
            "152": "emote-deathdrop", "faintdrop": "emote-deathdrop",
            "153": "emote-elbowbump", "elbowbump": "emote-elbowbump",
            "154": "emote-fail1", "fall": "emote-fail1",
            "155": "emote-fail2", "clumsy": "emote-fail2",
            "156": "emote-fainting", "faint": "emote-fainting",
            "157": "emote-hugyourself", "hugyourself": "emote-hugyourself",
            "158": "emote-jetpack", "jetpack": "emote-jetpack",
            "159": "emote-judochop", "judochop": "emote-judochop",
            "160": "emote-jumpb", "jump": "emote-jumpb",
            "161": "emote-laughing2", "amused": "emote-laughing2",
            "162": "emote-levelup", "levelup": "emote-levelup",
            "163": "emote-monster_fail", "monsterfail": "emote-monster_fail",
            "164": "emote-nightfever", "nightfever": "emote-nightfever",
            "165": "emote-ninjarun", "ninjarun": "emote-ninjarun",
            "166": "emote-peace", "peace": "emote-peace",
            "167": "emote-peekaboo", "peekaboo": "emote-peekaboo",
            "168": "emote-proposing", "proposing": "emote-proposing",
            "169": "emote-rainbow", "rainbow": "emote-rainbow",
            "170": "emote-robot", "robot": "emote-robot",
            "171": "emote-rofl", "rofl": "emote-rofl",
            "172": "emote-roll", "roll": "emote-roll",
            "173": "emote-ropepull", "ropepull": "emote-ropepull",
            "174": "emote-secrethandshake", "secrethandshake": "emote-secrethandshake",
            "175": "emote-sumo", "sumofight": "emote-sumo",
            "176": "emote-kicking", "superpunch": "emote-kicking",
            "177": "emote-superrun", "superrun": "emote-superrun",
            "178": "emote-theatrical", "theatrical": "emote-theatrical",
            "179": "emote-wings", "ibelieve": "emote-wings",
            "180": "idle-angry", "irritated": "idle-angry",
            "181": "idle-floorsleeping", "cozynap": "idle-floorsleeping",
            "182": "idle-floorsleeping2", "relaxing": "idle-floorsleeping2",
            "183": "idle-hero", "heropose": "idle-hero",
            "184": "idle-lookup", "ponder": "idle-lookup",
            "185": "idle-posh", "posh": "idle-posh",
            "186": "idle-sad", "poutyface": "idle-sad",
            "187": "emote-dab", "dab": "emote-dab",
            "188": "emote-gangnam", "gangnamstyle": "emote-gangnam",
            "189": "emoji-crying", "sob": "emoji-crying",
            "190": "idle-loop-tapdance", "taploop": "idle-loop-tapdance",
            "191": "idle-sleep", "sleepy": "idle-sleep",
            "192": "dance-sexy", "wiggledance": "dance-sexy",
            "193": "emoji-eyeroll", "eyeroll": "emoji-eyeroll",
            "194": "emote-gordonshuffle", "moonwalk": "emote-gordonshuffle",
            "195": "idle-fighter", "fighter": "idle-fighter",
            "196": "idle-dance-tiktok7", "renegade": "idle-dance-tiktok7",
            "197": "emote-exasperatedb", "facepalm": "emote-exasperatedb",
            "198": "idle-dance-headbobbing", "feelthebeat": "idle-dance-headbobbing",
            "199": "emote-happy", "happy": "emote-happy",
            "200": "emote-hug", "hug": "emote-hug",
            "201": "emote-slap", "slap": "emote-slap",
            "202": "emoji-clapping", "clap": "emoji-clapping",
            "203": "emote-exasperated", "exasperated": "emote-exasperated",
            "204": "emote-kissing-bound", "sweetsmooch": "emote-kissing-bound",
            "205": "emote-tapdance", "tapdance": "emote-tapdance",
            "206": "emote-thumbsuck", "thumbsuck": "emote-thumbsuck",
            "207": "emote-harlemshake", "harlemshake": "emote-harlemshake",
            "208": "emote-heartfingers", "hearthands": "emote-heartfingers",
            "209": "idle-loop-aerobics", "aerobics": "idle-loop-aerobics",
            "210": "emote-heartshape", "partnerheartarms": "emote-heartshape",
            "211": "emote-hearteyes", "loveflutter": "emote-hearteyes",
            "212": "dance-wild", "karma": "dance-wild",
            "213": "emoji-scared", "gasp": "emoji-scared",
            "214": "emote-think", "think": "emote-think",
            "215": "emoji-dizzy", "stunned": "emoji-dizzy",
            "216": "emote-embarrassed", "embarrassed": "emote-embarrassed",
            "217": "emote-disappear", "blastoff": "emote-disappear",
            "218": "idle-loop-annoyed", "annoyed": "idle-loop-annoyed",
            "219": "dance-zombie", "zombiedance": "dance-zombie",
            "220": "idle-loop-happy", "chillin": "idle-loop-happy",
            "221": "emote-frustrated", "pissedoff": "emote-frustrated",
            "222": "idle-loop-sad", "bummed": "idle-loop-sad",
            "223": "emoji-ghost", "ghost": "emoji-ghost",
            "224": "emoji-mind-blown", "mindblown": "emoji-mind-blown"
        }
        
        self.load_data()

    # =============================================
    # DATA MANAGEMENT
    # =============================================
    def save_data(self):
        try:
            data = {
                "owners": self.owners,
                "coowners": self.coowners,
                "senioradmins": self.senioradmins,
                "moderators": self.moderators,
                "designers": self.designers,
                "vips": self.vips,
                "blocked_users": self.blocked_users,
                "subscribers": self.subscribers,
                "teleport_points": {k: [v.x, v.y, v.z, v.facing] for k, v in self.teleport_points.items()},
                "teleport_roles": self.teleport_roles,
                "join_messages": self.join_messages,
                "leave_messages": self.leave_messages,
                "loop_messages": self.loop_messages,
                "loop_cooldown": self.loop_cooldown,
                "vip_cost": self.vip_cost,
                "vip_duration": self.vip_duration,
                "vip_join_messages": self.vip_join_messages,
                "vip_leave_messages": self.vip_leave_messages,
                "warnings": self.warnings,
                "moderation_history": self.moderation_history,
                "invite_room_id": self.invite_room_id,
                "command_aliases": self.command_aliases,
                "autotele_enabled": self.autotele_enabled
            }
            with open("bot_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("Data saved successfully")
        except Exception as e:
            print(f"Save error: {e}")

    def load_data(self):
        try:
            if os.path.exists("bot_data.json"):
                with open("bot_data.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.owners = data.get("owners", [BOT_OWNER_ID])
                self.coowners = data.get("coowners", [])
                self.senioradmins = data.get("senioradmins", [])
                self.moderators = data.get("moderators", [])
                self.designers = data.get("designers", [])
                self.vips = data.get("vips", {})
                self.blocked_users = data.get("blocked_users", [])
                self.subscribers = data.get("subscribers", [])
                tp_data = data.get("teleport_points", {})
                for name, coords in tp_data.items():
                    self.teleport_points[name] = Position(coords[0], coords[1], coords[2], coords[3])
                self.teleport_roles = data.get("teleport_roles", {})
                self.join_messages = data.get("join_messages", {})
                self.leave_messages = data.get("leave_messages", {})
                self.loop_messages = data.get("loop_messages", {})
                self.loop_cooldown = data.get("loop_cooldown", 60)
                self.vip_cost = data.get("vip_cost", 0)
                self.vip_duration = data.get("vip_duration", "permanent")
                self.vip_join_messages = data.get("vip_join_messages", {})
                self.vip_leave_messages = data.get("vip_leave_messages", {})
                self.warnings = data.get("warnings", {})
                self.moderation_history = data.get("moderation_history", [])
                self.invite_room_id = data.get("invite_room_id")
                self.command_aliases = data.get("command_aliases", {})
                self.autotele_enabled = data.get("autotele_enabled", False)
                print("Data loaded successfully")
        except Exception as e:
            print(f"Load error: {e}")

    # =============================================
    # PERMISSION CHECKS
    # =============================================
    def is_owner(self, user: User) -> bool:
        return user.id in self.owners

    def is_coowner(self, user: User) -> bool:
        return user.id in self.coowners or self.is_owner(user)

    def is_senior(self, user: User) -> bool:
        return user.id in self.senioradmins or self.is_coowner(user)

    def is_mod(self, user: User) -> bool:
        return user.id in self.moderators or self.is_senior(user)

    def is_designer(self, user: User) -> bool:
        return user.id in self.designers or self.is_mod(user)

    def is_vip(self, user: User) -> bool:
        if user.id in self.vips:
            vip_data = self.vips[user.id]
            if vip_data.get("expiry") == "permanent":
                return True
            if vip_data.get("expiry") and time.time() < vip_data.get("expiry"):
                return True
            else:
                del self.vips[user.id]
                self.save_data()
                return False
        return self.is_mod(user)

    def is_blocked(self, user: User) -> bool:
        return user.id in self.blocked_users

    def get_user_role(self, user_id: str) -> str:
        if user_id in self.owners:
            return "owner"
        if user_id in self.coowners:
            return "coowner"
        if user_id in self.senioradmins:
            return "senioradmin"
        if user_id in self.moderators:
            return "moderator"
        if user_id in self.designers:
            return "designer"
        if user_id in self.vips:
            return "vip"
        return "guest"

    def can_use_teleport(self, user: User, tp_name: str) -> bool:
        required_role = self.teleport_roles.get(tp_name, "public")
        if required_role == "public":
            return True
        if required_role == "vip":
            return self.is_vip(user)
        if required_role == "mod":
            return self.is_mod(user)
        if required_role == "senioradmin":
            return self.is_senior(user)
        if required_role == "coowner":
            return self.is_coowner(user)
        if required_role == "owner":
            return self.is_owner(user)
        return True

    # =============================================
    # HELPER FUNCTIONS
    # =============================================
    async def get_user_by_name(self, username: str):
        room_users = (await self.highrise.get_room_users()).content
        username_clean = username.lower().replace("@", "").strip()
        for u, pos in room_users:
            if u.username.lower() == username_clean:
                return u, pos
        return None, None

    async def get_my_position(self, user: User):
        room_users = (await self.highrise.get_room_users()).content
        for u, pos in room_users:
            if u.id == user.id:
                return pos
        return None

    async def get_all_users(self):
        room_users = (await self.highrise.get_room_users()).content
        return room_users

    async def send_chunked_message(self, text: str, chunk_size: int = 240):
        """250 karakter limitine uygun mesaj gonder"""
        words = text.split()
        current_chunk = ""
        for word in words:
            if len(current_chunk) + len(word) + 1 <= chunk_size:
                current_chunk += word + " "
            else:
                if current_chunk:
                    await self.highrise.chat(current_chunk.strip())
                    await asyncio.sleep(0.3)
                current_chunk = word + " "
        if current_chunk:
            await self.highrise.chat(current_chunk.strip())

    # =============================================
    # LOOP TASKS
    # =============================================
    async def emote_loop_task(self, user_id: str, emote_id: str):
        try:
            while True:
                await self.highrise.send_emote(emote_id, user_id)
                await asyncio.sleep(8)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Emote loop error: {e}")

    async def follow_loop_task(self, follower_id: str, target_id: str):
        try:
            while follower_id in self.follow_mode:
                room_users = await self.get_all_users()
                target_pos = None
                for u, pos in room_users:
                    if u.id == target_id:
                        target_pos = pos
                        break
                if target_pos:
                    await self.highrise.teleport(follower_id, target_pos)
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Follow loop error: {e}")

    async def message_loop_task(self):
        try:
            while self.loop_running:
                if self.loop_messages:
                    for idx in sorted(self.loop_messages.keys()):
                        if not self.loop_running:
                            break
                        msg = self.loop_messages[idx]
                        await self.send_chunked_message(msg)
                        await asyncio.sleep(self.loop_cooldown)
                else:
                    await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Message loop error: {e}")

    async def freeze_loop_task(self, user_id: str):
        try:
            while user_id in self.frozen_users:
                if user_id in self.freeze_positions:
                    pos = self.freeze_positions[user_id]
                    await self.highrise.teleport(user_id, pos)
                await asyncio.sleep(0.5)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Freeze loop error: {e}")

    # =============================================
    # EVENTS
    # =============================================
    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print(f"Bot started!")
        print(f"Bot ID: {session_metadata.user_id}")
        print(f"Room ID: {ROOM_ID}")
        await self.highrise.chat("Bot aktif!")
        
        if self.loop_messages and self.loop_running:
            self.loop_task = asyncio.create_task(self.message_loop_task())

    async def on_user_join(self, user: User, position: Position) -> None:
        # VIP ozel mesaj
        if user.id in self.vip_join_messages:
            msg = self.vip_join_messages[user.id].replace("@user", user.username)
            await self.send_chunked_message(msg)
        elif self.join_messages:
            msg_list = list(self.join_messages.values())
            if msg_list:
                msg = random.choice(msg_list).replace("@user", user.username)
                await self.send_chunked_message(msg)

    async def on_user_leave(self, user: User) -> None:
        # Temizlik
        if user.id in self.active_emote_loops:
            self.active_emote_loops[user.id].cancel()
            del self.active_emote_loops[user.id]
        if user.id in self.follow_mode:
            del self.follow_mode[user.id]
        if user.id in self.follow_tasks:
            self.follow_tasks[user.id].cancel()
            del self.follow_tasks[user.id]
        if user.id in self.flash_users:
            self.flash_users.remove(user.id)
        if user.id in self.frozen_users:
            self.frozen_users.remove(user.id)
        if user.id in self.freeze_positions:
            del self.freeze_positions[user.id]
        
        # VIP ozel mesaj
        if user.id in self.vip_leave_messages:
            msg = self.vip_leave_messages[user.id].replace("@user", user.username)
            await self.send_chunked_message(msg)
        elif self.leave_messages:
            msg_list = list(self.leave_messages.values())
            if msg_list:
                msg = random.choice(msg_list).replace("@user", user.username)
                await self.send_chunked_message(msg)

    async def on_user_move(self, user: User, pos: Position) -> None:
        # Flash mode
        if user.id in self.flash_users:
            await self.highrise.teleport(user.id, pos)
        
        # Freeze check
        if user.id in self.frozen_users and user.id in self.freeze_positions:
            await self.highrise.teleport(user.id, self.freeze_positions[user.id])

    async def on_tip(self, sender: User, receiver: User, tip) -> None:
        # VIP otomatik satin alma
        if self.vip_cost > 0:
            tip_amount = int(str(tip.amount).replace("gold_bar_", ""))
            if tip_amount >= self.vip_cost:
                if sender.id not in self.vips:
                    if self.vip_duration == "permanent":
                        self.vips[sender.id] = {"expiry": "permanent"}
                    else:
                        days = int(self.vip_duration)
                        expiry = time.time() + (days * 24 * 60 * 60)
                        self.vips[sender.id] = {"expiry": expiry}
                    self.save_data()
                    await self.highrise.chat(f"VIP verildi: {sender.username}")

    # =============================================
    # MAIN CHAT HANDLER
    # =============================================
    async def on_chat(self, user: User, message: str) -> None:
        if self.is_blocked(user):
            return
        
        msg = message.strip()
        msg_lower = msg.lower()
        
        # Emote shortcut (prefix olmadan)
        if msg_lower in self.emotes:
            emote_id = self.emotes[msg_lower]
            if user.id in self.active_emote_loops:
                self.active_emote_loops[user.id].cancel()
            task = asyncio.create_task(self.emote_loop_task(user.id, emote_id))
            self.active_emote_loops[user.id] = task
            return
        
        # Teleport shortcut
        if msg_lower in self.teleport_points:
            if self.can_use_teleport(user, msg_lower):
                await self.highrise.teleport(user.id, self.teleport_points[msg_lower])
            return
        
        # Stop komutu
        if msg_lower == "stop":
            if user.id in self.active_emote_loops:
                self.active_emote_loops[user.id].cancel()
                del self.active_emote_loops[user.id]
                await self.highrise.chat(f"Emote durduruldu: {user.username}")
            return
        
        # Emote + username
        parts = msg_lower.split()
        if len(parts) == 2 and parts[0] in self.emotes:
            emote_id = self.emotes[parts[0]]
            target_user, _ = await self.get_user_by_name(parts[1])
            if target_user:
                if target_user.id in self.active_emote_loops:
                    self.active_emote_loops[target_user.id].cancel()
                task = asyncio.create_task(self.emote_loop_task(target_user.id, emote_id))
                self.active_emote_loops[target_user.id] = task
            return
        
        # [emote]all komutu
        if msg_lower.endswith("all") and msg_lower[:-3] in self.emotes:
            emote_name = msg_lower[:-3]
            emote_id = self.emotes[emote_name]
            room_users = await self.get_all_users()
            for u, _ in room_users:
                try:
                    await self.highrise.send_emote(emote_id, u.id)
                except:
                    pass
            return
        
        # Stop [username]
        if msg_lower.startswith("stop "):
            target_name = msg[5:].strip()
            target_user, _ = await self.get_user_by_name(target_name)
            if target_user and target_user.id in self.active_emote_loops:
                self.active_emote_loops[target_user.id].cancel()
                del self.active_emote_loops[target_user.id]
                await self.highrise.chat(f"Emote durduruldu: {target_user.username}")
            return
        
        # TP [location] [username]
        if len(parts) == 2 and parts[0] in self.teleport_points:
            tp_name = parts[0]
            target_user, _ = await self.get_user_by_name(parts[1])
            if target_user and self.can_use_teleport(user, tp_name):
                await self.highrise.teleport(target_user.id, self.teleport_points[tp_name])
            return
        
        # Prefix komutlari
        if msg.startswith(self.prefix):
            await self.handle_command(user, msg)

    # =============================================
    # COMMAND HANDLER
    # =============================================
    async def handle_command(self, user: User, message: str) -> None:
        parts = message[1:].split()
        if not parts:
            return
        
        cmd = parts[0].lower()
        args = parts[1:]
        
        # Command alias check
        if cmd in self.command_aliases:
            cmd = self.command_aliases[cmd]
        
        try:
            # =============================================
            # EMOTE COMMANDS
            # =============================================
            if cmd == "emotelist" or cmd == "emote" and args and args[0].lower() == "list":
                emote_names = [k for k in self.emotes.keys() if not k.isdigit()]
                unique_emotes = list(set(emote_names))[:50]
                chunk = ", ".join(unique_emotes[:25])
                await self.highrise.chat(chunk)
                await asyncio.sleep(0.3)
                chunk2 = ", ".join(unique_emotes[25:50])
                if chunk2:
                    await self.highrise.chat(chunk2)

            # =============================================
            # MOVEMENT & TELEPORTATION COMMANDS
            # =============================================
            elif cmd == "goto":
                if not args:
                    await self.highrise.chat("Kullanim: !goto @username")
                    return
                target_user, target_pos = await self.get_user_by_name(args[0])
                if target_user and target_pos:
                    await self.highrise.teleport(user.id, target_pos)
                    await self.highrise.chat(f"{user.username} -> {target_user.username}")
                else:
                    await self.highrise.chat("Kullanici bulunamadi!")

            elif cmd == "bring":
                if not self.is_mod(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if not args:
                    await self.highrise.chat("Kullanim: !bring @username / all")
                    return
                
                my_pos = await self.get_my_position(user)
                if not my_pos:
                    return
                
                if args[0].lower() == "all":
                    room_users = await self.get_all_users()
                    count = 0
                    for u, _ in room_users:
                        if u.id != user.id:
                            try:
                                await self.highrise.teleport(u.id, my_pos)
                                count += 1
                            except:
                                pass
                    await self.highrise.chat(f"{count} kisi getirildi!")
                else:
                    target_user, _ = await self.get_user_by_name(args[0])
                    if target_user:
                        await self.highrise.teleport(target_user.id, my_pos)
                        await self.highrise.chat(f"{target_user.username} getirildi!")
                    else:
                        await self.highrise.chat("Kullanici bulunamadi!")

            elif cmd == "switch":
                if not self.is_mod(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if not args:
                    await self.highrise.chat("Kullanim: !switch @username")
                    return
                
                my_pos = await self.get_my_position(user)
                target_user, target_pos = await self.get_user_by_name(args[0])
                
                if target_user and target_pos and my_pos:
                    await self.highrise.teleport(user.id, target_pos)
                    await self.highrise.teleport(target_user.id, my_pos)
                    await self.highrise.chat(f"Yer degistirildi: {user.username} <-> {target_user.username}")

            elif cmd == "follow":
                if not args:
                    await self.highrise.chat("Kullanim: !follow @username")
                    return
                target_user, _ = await self.get_user_by_name(args[0])
                if target_user:
                    self.follow_mode[user.id] = target_user.id
                    task = asyncio.create_task(self.follow_loop_task(user.id, target_user.id))
                    self.follow_tasks[user.id] = task
                    await self.highrise.chat(f"{user.username} takip ediyor: {target_user.username}")

            elif cmd == "stopfollow" or (cmd == "stop" and args and args[0].lower() == "follow"):
                if user.id in self.follow_mode:
                    del self.follow_mode[user.id]
                if user.id in self.follow_tasks:
                    self.follow_tasks[user.id].cancel()
                    del self.follow_tasks[user.id]
                await self.highrise.chat(f"Takip durduruldu: {user.username}")

            elif cmd == "createtele" or cmd == "create":
                if not self.is_mod(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if len(args) < 1:
                    await self.highrise.chat("Kullanim: !create [isim] [rol]")
                    return
                
                tp_name = args[0].lower()
                role = args[1].lower() if len(args) > 1 else "public"
                
                my_pos = await self.get_my_position(user)
                if my_pos:
                    self.teleport_points[tp_name] = my_pos
                    self.teleport_roles[tp_name] = role
                    self.save_data()
                    await self.highrise.chat(f"TP olusturuldu: {tp_name} ({role})")

            elif cmd == "removetele" or cmd == "remove":
                if not self.is_mod(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if not args:
                    await self.highrise.chat("Kullanim: !remove [isim/all]")
                    return
                
                if args[0].lower() == "all":
                    self.teleport_points = {}
                    self.teleport_roles = {}
                    self.save_data()
                    await self.highrise.chat("Tum TP noktlari silindi!")
                else:
                    tp_name = args[0].lower()
                    if tp_name in self.teleport_points:
                        del self.teleport_points[tp_name]
                        if tp_name in self.teleport_roles:
                            del self.teleport_roles[tp_name]
                        self.save_data()
                        await self.highrise.chat(f"TP silindi: {tp_name}")
                    else:
                        await self.highrise.chat("TP bulunamadi!")

            elif cmd == "telelist" or cmd == "tele" and args and args[0].lower() == "list":
                if not self.teleport_points:
                    await self.highrise.chat("Kayitli TP yok!")
                    return
                tp_list = ", ".join(self.teleport_points.keys())
                await self.send_chunked_message(f"TP Listesi: {tp_list}")

            elif cmd == "teleall" or cmd == "tele" and args and args[0].lower() == "all":
                if not self.is_mod(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if len(args) < 2:
                    await self.highrise.chat("Kullanim: !teleall [konum]")
                    return
                
                tp_name = args[1].lower() if cmd == "tele" else args[0].lower()
                if tp_name in self.teleport_points:
                    pos = self.teleport_points[tp_name]
                    room_users = await self.get_all_users()
                    for u, _ in room_users:
                        try:
                            await self.highrise.teleport(u.id, pos)
                        except:
                            pass
                    await self.highrise.chat(f"Herkes {tp_name} konumuna isinlandi!")

            elif cmd == "flash":
                if not self.is_mod(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if user.id not in self.flash_users:
                    self.flash_users.append(user.id)
                    await self.highrise.chat(f"Flash modu acildi: {user.username}")
                else:
                    await self.highrise.chat("Flash modu zaten acik!")

            elif cmd == "stopflash" or (cmd == "stop" and args and args[0].lower() == "flash"):
                if user.id in self.flash_users:
                    self.flash_users.remove(user.id)
                    await self.highrise.chat(f"Flash modu kapatildi: {user.username}")

            elif cmd == "goback":
                if self.saved_position:
                    await self.highrise.walk_to(self.saved_position)
                    await self.highrise.chat("Kaydedilen konuma donuluyor...")

            elif cmd == "come":
                my_pos = await self.get_my_position(user)
                if my_pos:
                    await self.highrise.walk_to(my_pos)
                    await self.highrise.chat(f"Geliyorum: {user.username}")

            elif cmd == "out":
                if not self.is_mod(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if not args:
                    return
                target_user, _ = await self.get_user_by_name(args[0])
                if target_user:
                    far_pos = Position(9999, 9999, 9999)
                    await self.highrise.teleport(target_user.id, far_pos)

            # =============================================
            # MODERATION COMMANDS
            # =============================================
            elif cmd == "ban":
                if not self.is_mod(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if not args:
                    await self.highrise.chat("Kullanim: !ban @username [dakika]")
                    return
                
                target_user, _ = await self.get_user_by_name(args[0])
                duration = int(args[1]) * 60 if len(args) > 1 and args[1].isdigit() else 3600
                
                if target_user:
                    try:
                        await self.highrise.moderate_room(target_user.id, "ban", duration)
                        self.moderation_history.append({
                            "action": "ban",
                            "target": target_user.username,
                            "by": user.username,
                            "time": time.time(),
                            "duration": duration
                        })
                        self.save_data()
                        await self.highrise.chat(f"Banlandi: {target_user.username}")
                    except Exception as e:
                        await self.highrise.chat(f"Hata: {e}")

            elif cmd == "unban":
                if not self.is_mod(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if not args:
                    await self.highrise.chat("Kullanim: !unban @username")
                    return
                
                target_user, _ = await self.get_user_by_name(args[0])
                if target_user:
                    try:
                        await self.highrise.moderate_room(target_user.id, "unban")
                        await self.highrise.chat(f"Ban kaldirildi: {target_user.username}")
                    except Exception as e:
                        await self.highrise.chat(f"Hata: {e}")

            elif cmd == "mute":
                if not self.is_mod(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if not args:
                    await self.highrise.chat("Kullanim: !mute @username [dakika]")
                    return
                
                target_user, _ = await self.get_user_by_name(args[0])
                duration = int(args[1]) * 60 if len(args) > 1 and args[1].isdigit() else 300
                
                if target_user:
                    try:
                        await self.highrise.moderate_room(target_user.id, "mute", duration)
                        self.moderation_history.append({
                            "action": "mute",
                            "target": target_user.username,
                            "by": user.username,
                            "time": time.time(),
                            "duration": duration
                        })
                        self.save_data()
                        await self.highrise.chat(f"Susturuldu: {target_user.username}")
                    except Exception as e:
                        await self.highrise.chat(f"Hata: {e}")

            elif cmd == "unmute":
                if not self.is_mod(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if not args:
                    await self.highrise.chat("Kullanim: !unmute @username")
                    return
                
                target_user, _ = await self.get_user_by_name(args[0])
                if target_user:
                    try:
                        await self.highrise.moderate_room(target_user.id, "mute", 1)
                        await self.highrise.chat(f"Susturma kaldirildi: {target_user.username}")
                    except Exception as e:
                        await self.highrise.chat(f"Hata: {e}")

            elif cmd == "kick":
                if not self.is_mod(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if not args:
                    await self.highrise.chat("Kullanim: !kick @username")
                    return
                
                target_user, _ = await self.get_user_by_name(args[0])
                if target_user:
                    try:
                        await self.highrise.moderate_room(target_user.id, "kick")
                        self.moderation_history.append({
                            "action": "kick",
                            "target": target_user.username,
                            "by": user.username,
                            "time": time.time()
                        })
                        self.save_data()
                        await self.highrise.chat(f"Atildi: {target_user.username}")
                    except Exception as e:
                        await self.highrise.chat(f"Hata: {e}")

            elif cmd == "freeze":
                if not self.is_mod(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if not args:
                    await self.highrise.chat("Kullanim: !freeze @username")
                    return
                
                target_user, target_pos = await self.get_user_by_name(args[0])
                if target_user and target_pos:
                    self.frozen_users.append(target_user.id)
                    self.freeze_positions[target_user.id] = target_pos
                    asyncio.create_task(self.freeze_loop_task(target_user.id))
                    await self.highrise.chat(f"Donduruldu: {target_user.username}")

            elif cmd == "unfreeze":
                if not self.is_mod(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if not args:
                    await self.highrise.chat("Kullanim: !unfreeze @username")
                    return
                
                target_user, _ = await self.get_user_by_name(args[0])
                if target_user:
                    if target_user.id in self.frozen_users:
                        self.frozen_users.remove(target_user.id)
                    if target_user.id in self.freeze_positions:
                        del self.freeze_positions[target_user.id]
                    await self.highrise.chat(f"Cozuldu: {target_user.username}")

            elif cmd == "warn":
                if not self.is_mod(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if not args:
                    await self.highrise.chat("Kullanim: !warn @username [sebep]")
                    return
                
                target_user, _ = await self.get_user_by_name(args[0])
                reason = " ".join(args[1:]) if len(args) > 1 else "Belirtilmedi"
                
                if target_user:
                    if target_user.id not in self.warnings:
                        self.warnings[target_user.id] = []
                    self.warnings[target_user.id].append({
                        "reason": reason,
                        "by": user.username,
                        "time": time.time()
                    })
                    self.save_data()
                    warn_count = len(self.warnings[target_user.id])
                    await self.highrise.chat(f"Uyari verildi: {target_user.username} ({warn_count}. uyari)")

            elif cmd == "warnlist" or (cmd == "warn" and args and args[0].lower() == "list"):
                if not self.warnings:
                    await self.highrise.chat("Kayitli uyari yok!")
                    return
                msg = "Uyari Listesi: "
                for uid, warns in self.warnings.items():
                    msg += f"ID:{uid[:8]}... ({len(warns)} uyari), "
                await self.send_chunked_message(msg)

            elif cmd == "clearwarn":
                if not self.is_mod(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if not args:
                    await self.highrise.chat("Kullanim: !clearwarn @username")
                    return
                
                target_user, _ = await self.get_user_by_name(args[0])
                if target_user and target_user.id in self.warnings:
                    del self.warnings[target_user.id]
                    self.save_data()
                    await self.highrise.chat(f"Uyarilar temizlendi: {target_user.username}")

            elif cmd == "clearallwarn":
                if not self.is_owner(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                self.warnings = {}
                self.save_data()
                await self.highrise.chat("Tum uyarilar temizlendi!")

            elif cmd == "moderationlist" or cmd == "modlist":
                if not self.moderation_history:
                    await self.highrise.chat("Moderasyon gecmisi bos!")
                    return
                recent = self.moderation_history[-5:]
                msg = "Son islemler: "
                for h in recent:
                    msg += f"{h['action']}-{h['target']}, "
                await self.send_chunked_message(msg)

            # =============================================
            # MESSAGE COMMANDS
            # =============================================
            elif cmd == "setjoin":
                if not self.is_mod(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if len(args) < 2:
                    await self.highrise.chat("Kullanim: !setjoin [numara] [mesaj]")
                    return
                
                idx = args[0]
                msg = " ".join(args[1:])
                self.join_messages[idx] = msg
                self.save_data()
                await self.highrise.chat(f"Giris mesaji {idx} ayarlandi!")

            elif cmd == "setleave":
                if not self.is_mod(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if len(args) < 2:
                    await self.highrise.chat("Kullanim: !setleave [numara] [mesaj]")
                    return
                
                idx = args[0]
                msg = " ".join(args[1:])
                self.leave_messages[idx] = msg
                self.save_data()
                await self.highrise.chat(f"Cikis mesaji {idx} ayarlandi!")

            elif cmd == "joinlist" or (cmd == "join" and args and args[0].lower() == "list"):
                if not self.join_messages:
                    await self.highrise.chat("Giris mesaji yok!")
                    return
                msg = "Giris mesajlari: "
                for idx, m in self.join_messages.items():
                    msg += f"[{idx}] {m[:20]}..., "
                await self.send_chunked_message(msg)

            elif cmd == "leavelist" or (cmd == "leave" and args and args[0].lower() == "list"):
                if not self.leave_messages:
                    await self.highrise.chat("Cikis mesaji yok!")
                    return
                msg = "Cikis mesajlari: "
                for idx, m in self.leave_messages.items():
                    msg += f"[{idx}] {m[:20]}..., "
                await self.send_chunked_message(msg)

            elif cmd == "loop":
                if not self.is_mod(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if not args:
                    await self.highrise.chat("Kullanim: !loop [numara] [mesaj] veya !loop [numara]")
                    return
                
                idx = args[0]
                if len(args) == 1:
                    # Temizle
                    if idx in self.loop_messages:
                        del self.loop_messages[idx]
                        self.save_data()
                        await self.highrise.chat(f"Loop {idx} silindi!")
                else:
                    # Ayarla
                    msg = " ".join(args[1:])
                    self.loop_messages[idx] = msg
                    self.save_data()
                    await self.highrise.chat(f"Loop {idx} ayarlandi!")

            elif cmd == "startloop":
                if not self.is_mod(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if not self.loop_running:
                    self.loop_running = True
                    self.loop_task = asyncio.create_task(self.message_loop_task())
                    await self.highrise.chat("Loop baslatildi!")

            elif cmd == "stoploop":
                if not self.is_mod(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                self.loop_running = False
                if self.loop_task:
                    self.loop_task.cancel()
                    self.loop_task = None
                await self.highrise.chat("Loop durduruldu!")

            elif cmd == "loopcooldown":
                if not self.is_mod(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if not args or not args[0].isdigit():
                    await self.highrise.chat("Kullanim: !loopcooldown [saniye]")
                    return
                self.loop_cooldown = int(args[0])
                self.save_data()
                await self.highrise.chat(f"Loop bekleme suresi: {self.loop_cooldown} saniye")

            elif cmd == "looplist" or (cmd == "loop" and len(args) > 0 and args[0].lower() == "list"):
                if not self.loop_messages:
                    await self.highrise.chat("Loop mesaji yok!")
                    return
                msg = "Loop mesajlari: "
                for idx, m in self.loop_messages.items():
                    msg += f"[{idx}] {m[:20]}..., "
                await self.send_chunked_message(msg)

            elif cmd == "spam":
                if not self.is_mod(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if len(args) < 2:
                    await self.highrise.chat("Kullanim: !spam [mesaj] [sayi]")
                    return
                
                count = int(args[-1]) if args[-1].isdigit() else 5
                text = " ".join(args[:-1]) if args[-1].isdigit() else " ".join(args)
                count = min(count, 10)  # Max 10
                
                for _ in range(count):
                    await self.highrise.chat(text)
                    await asyncio.sleep(0.5)

            # =============================================
            # VIP COMMANDS
            # =============================================
            elif cmd == "vipcost" or (cmd == "vip" and args and args[0].lower() == "cost"):
                if not self.is_owner(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if len(args) < 2 if cmd == "vip" else len(args) < 1:
                    await self.highrise.chat("Kullanim: !vipcost [miktar]")
                    return
                
                amount = args[1] if cmd == "vip" else args[0]
                if amount.isdigit():
                    self.vip_cost = int(amount)
                    self.save_data()
                    await self.highrise.chat(f"VIP ucreti: {self.vip_cost}")

            elif cmd == "vipduration" or (cmd == "vip" and args and args[0].lower() == "duration"):
                if not self.is_owner(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if len(args) < 2 if cmd == "vip" else len(args) < 1:
                    await self.highrise.chat("Kullanim: !vipduration [gun/permanent]")
                    return
                
                duration = args[1] if cmd == "vip" else args[0]
                self.vip_duration = duration.lower()
                self.save_data()
                await self.highrise.chat(f"VIP suresi: {self.vip_duration}")

            elif cmd == "addvip":
                if not self.is_owner(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if not args:
                    await self.highrise.chat("Kullanim: !addvip @username [gun]")
                    return
                
                target_user, _ = await self.get_user_by_name(args[0])
                duration = args[1] if len(args) > 1 else self.vip_duration
                
                if target_user:
                    if duration == "permanent":
                        self.vips[target_user.id] = {"expiry": "permanent"}
                    else:
                        days = int(duration) if duration.isdigit() else 30
                        expiry = time.time() + (days * 24 * 60 * 60)
                        self.vips[target_user.id] = {"expiry": expiry}
                    self.save_data()
                    await self.highrise.chat(f"VIP verildi: {target_user.username}")

            elif cmd == "removevip":
                if not self.is_owner(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if not args:
                    await self.highrise.chat("Kullanim: !removevip @username")
                    return
                
                target_user, _ = await self.get_user_by_name(args[0])
                if target_user and target_user.id in self.vips:
                    del self.vips[target_user.id]
                    self.save_data()
                    await self.highrise.chat(f"VIP kaldirildi: {target_user.username}")

            elif cmd == "viplist" or (cmd == "vip" and args and args[0].lower() == "list"):
                if not self.vips:
                    await self.highrise.chat("VIP yok!")
                    return
                msg = f"VIP Listesi: {len(self.vips)} kisi"
                await self.highrise.chat(msg)

            elif cmd == "setvipjoin":
                if not self.is_owner(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if len(args) < 2:
                    await self.highrise.chat("Kullanim: !setvipjoin @username [mesaj]")
                    return
                
                target_user, _ = await self.get_user_by_name(args[0])
                msg = " ".join(args[1:])
                if target_user:
                    self.vip_join_messages[target_user.id] = msg
                    self.save_data()
                    await self.highrise.chat(f"VIP giris mesaji ayarlandi: {target_user.username}")

            elif cmd == "setvipleave":
                if not self.is_owner(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if len(args) < 2:
                    await self.highrise.chat("Kullanim: !setvipleave @username [mesaj]")
                    return
                
                target_user, _ = await self.get_user_by_name(args[0])
                msg = " ".join(args[1:])
                if target_user:
                    self.vip_leave_messages[target_user.id] = msg
                    self.save_data()
                    await self.highrise.chat(f"VIP cikis mesaji ayarlandi: {target_user.username}")

            elif cmd == "vipstatus":
                if not args:
                    await self.highrise.chat("Kullanim: !vipstatus @username")
                    return
                
                target_user, _ = await self.get_user_by_name(args[0])
                if target_user:
                    if target_user.id in self.vips:
                        vip_data = self.vips[target_user.id]
                        if vip_data.get("expiry") == "permanent":
                            await self.highrise.chat(f"{target_user.username}: VIP (Surumaiz)")
                        else:
                            remaining = int((vip_data.get("expiry", 0) - time.time()) / 86400)
                            await self.highrise.chat(f"{target_user.username}: VIP ({remaining} gun kaldi)")
                    else:
                        await self.highrise.chat(f"{target_user.username}: VIP degil")

            # =============================================
            # REACTION COMMANDS
            # =============================================
            elif cmd == "heart" or cmd == "h":
                if not args:
                    await self.highrise.chat("Kullanim: !h @username [sayi]")
                    return
                
                target_user, _ = await self.get_user_by_name(args[0])
                count = int(args[1]) if len(args) > 1 and args[1].isdigit() else 1
                count = min(count, 10)
                
                if target_user:
                    for _ in range(count):
                        try:
                            await self.highrise.react("heart", target_user.id)
                            await asyncio.sleep(0.3)
                        except:
                            pass

            elif cmd == "heartall" or cmd == "hall":
                room_users = await self.get_all_users()
                for u, _ in room_users:
                    try:
                        await self.highrise.react("heart", u.id)
                        await asyncio.sleep(0.2)
                    except:
                        pass

            elif cmd == "waveall":
                room_users = await self.get_all_users()
                for u, _ in room_users:
                    try:
                        await self.highrise.react("wink", u.id)
                        await asyncio.sleep(0.2)
                    except:
                        pass

            # =============================================
            # ROLE COMMANDS
            # =============================================
            elif cmd == "giverole":
                if not self.is_owner(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if len(args) < 2:
                    await self.highrise.chat("Kullanim: !giverole @username [rol]")
                    return
                
                target_user, _ = await self.get_user_by_name(args[0])
                role = args[1].lower()
                
                if target_user:
                    if role == "owner":
                        if target_user.id not in self.owners:
                            self.owners.append(target_user.id)
                    elif role == "coowner":
                        if target_user.id not in self.coowners:
                            self.coowners.append(target_user.id)
                    elif role == "senioradmin":
                        if target_user.id not in self.senioradmins:
                            self.senioradmins.append(target_user.id)
                    elif role == "moderator" or role == "mod":
                        if target_user.id not in self.moderators:
                            self.moderators.append(target_user.id)
                    elif role == "designer":
                        if target_user.id not in self.designers:
                            self.designers.append(target_user.id)
                    else:
                        await self.highrise.chat("Gecersiz rol!")
                        return
                    
                    self.save_data()
                    await self.highrise.chat(f"Rol verildi: {target_user.username} -> {role}")

            elif cmd == "removerole":
                if not self.is_owner(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if not args:
                    await self.highrise.chat("Kullanim: !removerole @username")
                    return
                
                target_user, _ = await self.get_user_by_name(args[0])
                if target_user:
                    removed = False
                    if target_user.id in self.coowners:
                        self.coowners.remove(target_user.id)
                        removed = True
                    if target_user.id in self.senioradmins:
                        self.senioradmins.remove(target_user.id)
                        removed = True
                    if target_user.id in self.moderators:
                        self.moderators.remove(target_user.id)
                        removed = True
                    if target_user.id in self.designers:
                        self.designers.remove(target_user.id)
                        removed = True
                    
                    if removed:
                        self.save_data()
                        await self.highrise.chat(f"Rol kaldirildi: {target_user.username}")

            elif cmd == "rolelist":
                msg = "Roller: "
                msg += f"Owner: {len(self.owners)}, "
                msg += f"CoOwner: {len(self.coowners)}, "
                msg += f"Senior: {len(self.senioradmins)}, "
                msg += f"Mod: {len(self.moderators)}, "
                msg += f"Designer: {len(self.designers)}"
                await self.highrise.chat(msg)

            elif cmd == "clearroles":
                if not self.is_owner(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                self.coowners = []
                self.senioradmins = []
                self.moderators = []
                self.designers = []
                self.save_data()
                await self.highrise.chat("Tum roller temizlendi!")

            elif cmd == "block":
                if not self.is_owner(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if not args:
                    await self.highrise.chat("Kullanim: !block @username")
                    return
                
                target_user, _ = await self.get_user_by_name(args[0])
                if target_user:
                    if target_user.id not in self.blocked_users:
                        self.blocked_users.append(target_user.id)
                        self.save_data()
                        await self.highrise.chat(f"Engellendi: {target_user.username}")

            elif cmd == "unblock":
                if not self.is_owner(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if not args:
                    await self.highrise.chat("Kullanim: !unblock @username")
                    return
                
                target_user, _ = await self.get_user_by_name(args[0])
                if target_user and target_user.id in self.blocked_users:
                    self.blocked_users.remove(target_user.id)
                    self.save_data()
                    await self.highrise.chat(f"Engel kaldirildi: {target_user.username}")

            elif cmd == "blocklist":
                if not self.blocked_users:
                    await self.highrise.chat("Engelli kullanici yok!")
                    return
                await self.highrise.chat(f"Engelli: {len(self.blocked_users)} kisi")

            elif cmd == "promote":
                if not self.is_owner(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if len(args) < 2:
                    await self.highrise.chat("Kullanim: !promote @username [mod/designer]")
                    return
                
                target_user, _ = await self.get_user_by_name(args[0])
                role = args[1].lower()
                
                if target_user:
                    if role == "moderator" or role == "mod":
                        if target_user.id not in self.moderators:
                            self.moderators.append(target_user.id)
                            self.save_data()
                            await self.highrise.chat(f"Moderator yapildi: {target_user.username}")
                    elif role == "designer":
                        if target_user.id not in self.designers:
                            self.designers.append(target_user.id)
                            self.save_data()
                            await self.highrise.chat(f"Designer yapildi: {target_user.username}")

            elif cmd == "demote":
                if not self.is_owner(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if not args:
                    await self.highrise.chat("Kullanim: !demote @username")
                    return
                
                target_user, _ = await self.get_user_by_name(args[0])
                if target_user:
                    if target_user.id in self.moderators:
                        self.moderators.remove(target_user.id)
                    if target_user.id in self.designers:
                        self.designers.remove(target_user.id)
                    self.save_data()
                    await self.highrise.chat(f"Yetki dusuruldu: {target_user.username}")

            # =============================================
            # BROADCAST & INVITES COMMANDS
            # =============================================
            elif cmd == "broadcast":
                if not self.is_owner(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if not args:
                    await self.highrise.chat("Kullanim: !broadcast [mesaj]")
                    return
                
                msg = " ".join(args)
                count = 0
                for sub_id in self.subscribers:
                    try:
                        await self.highrise.send_whisper(sub_id, f"[Broadcast] {msg}")
                        count += 1
                        await asyncio.sleep(0.5)
                    except:
                        pass
                await self.highrise.chat(f"Yayim gonderildi: {count} kisi")

            elif cmd == "sub":
                if user.id not in self.subscribers:
                    self.subscribers.append(user.id)
                    self.save_data()
                    await self.highrise.chat(f"Abone olundu: {user.username}")
                else:
                    await self.highrise.chat("Zaten abonesiniz!")

            elif cmd == "unsub":
                if user.id in self.subscribers:
                    self.subscribers.remove(user.id)
                    self.save_data()
                    await self.highrise.chat(f"Abonelik iptal: {user.username}")

            elif cmd == "sublist":
                if not self.is_mod(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                await self.highrise.chat(f"Abone sayisi: {len(self.subscribers)}")

            elif cmd == "setinvite":
                if not self.is_owner(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if not args:
                    await self.highrise.chat("Kullanim: !setinvite [room_id]")
                    return
                self.invite_room_id = args[0]
                self.save_data()
                await self.highrise.chat("Davet odasi ayarlandi!")

            elif cmd == "invite":
                if not self.is_owner(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if not self.invite_room_id:
                    await self.highrise.chat("Once !setinvite ile oda ayarlayin!")
                    return
                
                count = 0
                for sub_id in self.subscribers:
                    try:
                        await self.highrise.send_whisper(sub_id, f"Odaya davet: {self.invite_room_id}")
                        count += 1
                        await asyncio.sleep(0.5)
                    except:
                        pass
                await self.highrise.chat(f"Davet gonderildi: {count} kisi")

            elif cmd == "removeallsubs":
                if not self.is_owner(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                self.subscribers = []
                self.save_data()
                await self.highrise.chat("Tum aboneler silindi!")

            # =============================================
            # SETTINGS COMMANDS
            # =============================================
            elif cmd == "botroom":
                if not self.is_owner(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                await self.highrise.chat("Oda degistirmek icin kodu duzenleyin!")

            elif cmd == "restartbot":
                if not self.is_owner(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                await self.highrise.chat("Bot yeniden baslatiliyor...")
                # Python restart gerektirir

            elif cmd == "setpos":
                if not self.is_mod(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                my_pos = await self.get_my_position(user)
                if my_pos:
                    self.saved_position = my_pos
                    await self.highrise.chat("Pozisyon kaydedildi!")

            elif cmd == "editcommand":
                if not self.is_owner(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                if len(args) < 2:
                    await self.highrise.chat("Kullanim: !editcommand [komut] [alternatif/default/list/clearall]")
                    return
                
                if args[0].lower() == "list":
                    if not self.command_aliases:
                        await self.highrise.chat("Alias yok!")
                        return
                    msg = "Aliases: " + ", ".join([f"{k}->{v}" for k, v in self.command_aliases.items()])
                    await self.send_chunked_message(msg)
                elif args[0].lower() == "clearall":
                    self.command_aliases = {}
                    self.save_data()
                    await self.highrise.chat("Tum aliaslar silindi!")
                elif args[1].lower() == "default":
                    cmd_name = args[0].lower()
                    if cmd_name in self.command_aliases:
                        del self.command_aliases[cmd_name]
                        self.save_data()
                        await self.highrise.chat(f"Alias kaldirildi: {cmd_name}")
                else:
                    alias = args[0].lower()
                    original = args[1].lower()
                    self.command_aliases[alias] = original
                    self.save_data()
                    await self.highrise.chat(f"Alias eklendi: {alias} -> {original}")

            elif cmd == "autotele":
                if not self.is_owner(user):
                    await self.highrise.chat("Yetkiniz yok!")
                    return
                self.autotele_enabled = not self.autotele_enabled
                self.save_data()
                status = "acik" if self.autotele_enabled else "kapali"
                await self.highrise.chat(f"AutoTele: {status}")

            elif cmd == "help":
                await self.highrise.chat("Emotes | Movement | Moderation")
                await asyncio.sleep(0.3)
                await self.highrise.chat("Messages | VIP | Roles | Settings")
                await asyncio.sleep(0.3)
                await self.highrise.chat("!help [kategori] yazin")

            elif cmd == "updates":
                await self.highrise.chat("Bot v2.0 - Tum ozellikler aktif!")

            elif cmd == "suggest":
                if not args:
                    await self.highrise.chat("Kullanim: !suggest [mesaj]")
                    return
                suggestion = " ".join(args)
                await self.highrise.chat(f"Oneri alindi: {user.username}")
                # Oneriyi kaydetme islemi

            elif cmd == "id":
                await self.highrise.send_whisper(user.id, f"ID: {user.id}")

            elif cmd == "users":
                room_users = await self.get_all_users()
                await self.highrise.chat(f"Odada {len(room_users)} kisi var")

            elif cmd == "ping":
                await self.highrise.chat("Pong!")

        except Exception as e:
            print(f"Command error: {e}")
            await self.highrise.chat(f"Hata olustu!")


# =============================================
# BOT CALISTIRMA
# =============================================
if __name__ == "__main__":
    import sys
    import asyncio
    from highrise.__main__ import BotDefinition, main
    
    if BOT_OWNER_ID == "BURAYA_OWNER_ID_YAZIN":
        print("HATA: Lutfen BOT_OWNER_ID'yi ayarlayin!")
        sys.exit(1)
    
    if ROOM_ID == "BURAYA_ROOM_ID_YAZIN":
        print("HATA: Lutfen ROOM_ID'yi ayarlayin!")
        sys.exit(1)
    
    if BOT_TOKEN == "BURAYA_BOT_TOKEN_YAZIN":
        print("HATA: Lutfen BOT_TOKEN'i ayarlayin!")
        sys.exit(1)
    
    # BotDefinition olustur
    bot_instance = Bot()
    definitions = [
        BotDefinition(
            bot=bot_instance, 
            room_id=ROOM_ID, 
            api_token=BOT_TOKEN
        )
    ]
    
    while True:
        try:
            # asyncio.run ile main fonksiyonunu calistir
            asyncio.run(main(definitions))
        except Exception as e:
            print(f"Bot hatasi: {e}")
            print("5 saniye sonra yeniden baslatiiliyor...")
            time.sleep(5)
