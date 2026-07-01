import disnake

version = "2.4.0"
prefix = "=="

COGS = [
    "jishaku",
    "cogs.admin",
    "cogs.misc",
    # "cogs.raid",
    "cogs.rdanny",
    "cogs.devtools",
    # "cogs.timeout",
    # 'cogs.logchamp',
]

ADMINS = {
    204414611578028034,  # rev
    304695409031512064,  # dove
    448250281097035777,  # nojons
    325454303387058176,  # axo
}

MODS = {
    """
    204414611578028034,  # nwunder#0003
    279722793891790848,  # Moistley#5939
    533087803261714433,  # Neptune's Helper#0039
    375375057138089986,  # Saturnfive050#1337
    304695409031512064,  # dovedevic#0522
    426550338141683713,  # dee
    280874216310439938,  # egg#2222
    448250281097035777,  # No Jons#1299
    224323277370294275,  # Kiwi#6666
    299023554127593473,  # mzone#1771
    298497141490450432,  # AdventurousSwine#9894
"""
}

intents = disnake.Intents(
    # most stuff still enabled
    guilds=True,
    members=True,
    bans=True,
    emojis=True,
    integrations=True,
    webhooks=True,
    invites=True,
    voice_states=True,
    # presences is bad
    presences=False,
    # enable guild stuff
    guild_messages=True,
    guild_reactions=True,
    guild_typing=True,
    # disable DM stuff
    dm_messages=False,
    dm_reactions=False,
    dm_typing=False,
    # fuck message content
    message_content=True,
)
