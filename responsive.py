import random

# key = trigger, valuie = responses
d_responses = {}
d_responses["ligma"] = ["ligma balls", "ligma nuts", "ligma dick", "ligma ass"]
d_responses["sugma"] = ["sugma balls", "sugma nuts", "sugma dick"]
d_responses["cringe"] = ["du e cringe"]
d_responses["håll käften"] = ["Jag ser att du skrev \"käften\". Ville du skriva \"Kräfta\", eller kanske \"Jag är oskuld\"?"]
d_responses["based"] = ["Based? Based on what? In your dick? Please shut the fuck up and use words properly you fuckin troglodyte, do you think God gave us a freedom of speech just to spew random words that have no meaning that doesn't even correllate to the topic of the conversation? Like please you always complain about why no one talks to you or no one expresses their opinions on you because you're always spewing random shit like poggers based cringe and when you try to explain what it is and you just say that it's funny like what? What the fuck is funny about that do you think you'll just become a stand-up comedian that will get a standing ovation just because you said \"cum\" in the stage? HELL NO YOU FUCKIN IDIOT, so please shut the fuck up and use words properly you dumb bitch",
                        "Based 👌? Based 👌💯💦 on 🔛 what? In your 👉👌 dick 🍆? Please 🍆💦😂 shut 😷 the fuck 👉 up ☝ and use 🏻 words 🔚 properly 🎩 you 👉 fuckin 👌 troglodyte, do you 👈😀 think 💭 God 😇 gave 🎁📐 us 🇺🇸 a freedom 🙌 of speech 🗣 just to spew ⛲ random 🎰 words 🔚 that have no 😣 meaning 😏 that doesn't even 🌃 correllate to the topic ➕ of the conversation 🗣? Like 😄 please 🙏 you 👈 always 🕔 complain 🗣 about 💦 why 🤔 no 🙅 one ☝ talks 🗣 to you 👈 or no 🚫 one ☝💯 expresses 😤 their opinions 😤 on 🔛 you 😪💤👈 because you're always 🔥 spewing 💭 random 🎲 shit 👌 like 👍 poggers 😎💅 based ❌👨‍❤️‍👨 cringe 😬 and when 🍑 you 👈 try 😐 to explain 🤔💬 what it is and you 👈🏼 just say 💬 that it's funny 😃 like 😄 what? What the fuck 👉🌎🚫 is funny 😃 about ✨💦 that do you 👈 think 🤔 you'll just become 🅱💦😥 a stand-up comedian 🤡 that will get 🉐 a standing 🚹⬆ ovation just because you 👉 said 💬 \"cum 💦🔛\" in the stage 👄? HELL 👿🔥 NO 🚫 YOU 👉 FUCKIN 👉👌 IDIOT 💢, so please 🙏 shut 😷 the fuck 👉 up ⬆🆙 and use 🏻 words 🔚 properly 🎩 you 🌠👦🏼👉 dumb 👅 bitch 🐶🐕♀"]

def get_response_trigger(msg):
    for response_trigger in d_responses:
        if response_trigger in msg:
            return response_trigger
    return ""

def generate_response_by_trigger(response_trigger):
    return random.choice(d_responses[response_trigger])

# EMOJI REACTIONS
d_reactions = {}
# basic
d_reactions["harold"] = ["Harold"]
d_reactions["pog"] = ["pogchamp"]
d_reactions["sad"] = ["PepeHands"]
d_reactions["rat"] = ["ratSHAKE"]
d_reactions["smart"] = ["smart"]
d_reactions["lol"] = ["pepekek"]
d_reactions["lmao"] = ["pepekek"]
d_reactions["rat"] = ["ratSHAKE"]
d_reactions["gains"] = ["hunghhhhhhuuu"]
# league of legends
d_reactions["league"] = ["Harold"]
# world of warcraft 
d_reactions["spela wow"] = ["Harold"]
d_reactions["raid"] = ["Harold"]
d_reactions["dungeon"] = ["Harold"]
d_reactions["keys"] = ["Harold"]
d_reactions["transmog"] = ["Harold"]

def get_reactions(msg, available_emojis):
    reactions = []

    for reaction_trigger in d_reactions:
        if reaction_trigger in msg:
            reaction_emoji = random.choice(d_reactions[reaction_trigger])
            for emoji in available_emojis:
                if reaction_emoji == emoji.name:
                    reactions.append(emoji)

    return reactions


d_unique_responses = {}
d_unique_responses[".jahhok"] = ["ahh ok då fattar jag", "makes sense", "låter rimligt asså"]
d_unique_responses[".jwtf"] = ["asså what the fuck hahaha", "wow wtf", "asså wtf"]

def get_unique_response(msg):
    for unique_response_trigger in d_unique_responses:
        if msg.startswith(unique_response_trigger):
            return generate_unique_response(unique_response_trigger)
    return ""

def generate_unique_response(trigger):
    return random.choice(d_unique_responses[trigger])