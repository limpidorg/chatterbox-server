import asyncio
import threading
from .chatterbot.run import bot
import time

loop = asyncio.new_event_loop()


class Promise(object):
    def __init__(self, timeout=10):
        super().__setattr__("data", {})
        super().__setattr__("resolved", False)
        super().__setattr__("timeout", timeout)

    def resolve(self):
        self.resolved = True

    def wait(self):
        t = time.time()
        while not self.resolved and time.time() - t < self.timeout:
            time.sleep(0.05)
        if not self.resolved:
            raise TimeoutError("Promise timed out")
        return self

    def __setattr__(self, __name, __value) -> None:
        try:
            super().__setattr__(__name, __value)
        except:
            self.data[__name] = __value

    def __getattr__(self, __name):
        data = super().__getattribute__("data")
        if __name in data:
            return data[__name]
        else:
            raise AttributeError(f"{__name} not found")


def hasJoinedDiscord(username):
    promise = Promise()
    loop.call_soon_threadsafe(asyncio.ensure_future, bot.get_discord_user(username, promise))
    promise.wait()
    return promise.has_joined_discord


def getDiscordInternalId(username):
    promise = Promise()
    loop.call_soon_threadsafe(asyncio.ensure_future, bot.get_discord_user(username, promise))
    promise.wait()
    return promise.discord_id


def getDiscordUser(username):
    promise = Promise()
    loop.call_soon_threadsafe(asyncio.ensure_future, bot.get_discord_user(username, promise))
    promise.wait()
    return {"hasJoinedDiscord": promise.has_joined_discord, "discordId": promise.discord_id}


def sendMessage(id, message):
    asyncio.ensure_future(bot.send_message(id, message))


loop.call_soon_threadsafe(loop.stop)


def discordVerification(discordId):
    return hasJoinedDiscord(discordId)
