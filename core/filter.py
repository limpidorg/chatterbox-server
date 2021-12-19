import core.notifications
import core.session
from integrations.discordbot import getDiscordId, sendMessage
from utils import returnMessage

MESSAGE_TYPES = {
    "insults": [
        "fuck",
        "bitch",
        "stfu",
        "jerk",
        "nigger",
        "nigga",
        "dick",
        "pussy",
        "bastard",
        "cunt",
        "damn",
        "bollocks",
        "bugger",
        "choad",
    ],
    "extremBehaviours": ["suicide", "kys", "kill", "depression", "traumatised", "phobia", "panic", "murder", "rape"],
}


def classifyMessage(message):
    loweredMessage = message.lower()
    words = loweredMessage.split(" ")

    for key in MESSAGE_TYPES:
        for keyword in MESSAGE_TYPES[key]:
            if keyword in words:
                if key == "insults":
                    return False, "insults", keyword
                elif key == "extremBehaviours":
                    return False, "extremBehaviours", keyword

    return True, "", ""


def messageValidation(sessionId, chatId, message, socketId):
    allowed, type, keyword = classifyMessage(message)
    if not allowed:
        # Sends warning message to the client
        core.notifications.sendNotificationToSocketId(
            socketId,
            "show-alert",
            returnMessage(
                0,
                message="You are not allowed to use that word.",
                title="Warning",
                actions=[
                    {"type": "cancel", "title": "OK"},
                ],
            ),
        )

        session = core.session.getSession(sessionId)
        if session:
            discordId = session.discordId
            discord_internal_id = getDiscordId(discordId)

        if discord_internal_id != None:
            if type == "insults":
                message = {
                    "title": "Hello",
                    "description": f"**{keyword}**, and any other insults are not allowed 🤐",
                    "subColumns": [
                        {
                            "title": "Use fun alternatives instead! Or doodle your feelings out! 😉",
                            "description": "Please be polite to others and to yourself 💙",
                        }
                    ],
                }
            elif type == "extremBehaviours":
                message = {
                    "title": "Hello",
                    "description": "This is a safe and comfortable space for all. If you're upset or feeling down, please refer to the resources below!",
                    "url": "https://checkpointorg.com/global/",
                    "subColumns": [
                        {
                            "title": "There is always hope, even in the most difficult times 💙",
                            "description": "[Visit this website for useful hotlines](https://www.opencounseling.com/suicide-hotlines)",
                        },
                        {
                            "title": "You're priceless!",
                            "description": "Always be kind and take care of yourself. Be mindful of others.",
                        },
                    ],
                }
            sendMessage(discord_internal_id, message)
        return False  # Return false in messageValidation stops the message from being sent.
    return True
