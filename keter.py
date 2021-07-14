# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

from src.file_verification import file_verification


# Le token de votre Bot Discord:



# Les mots bannis dans les fichiers envoyés, par défaut 'token':
key = "token"

# Fichiers autorisés, laisser vide pour enlever la restriction:
authorized = ['py', 'txt', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4', 'json', 'bat']

# Voulez-vous recevoir les logs en message privé?
logs = True

# Votre identifiant Discord, si les logs sont activés:
user_logs = 401779573865316384

# Taille maximum autorisée pour le renvoi des fichiers, si les logs sont activés:

# Exemple : 1KB = 1000 | 1MB = 1000000 | ∞ = 0

max_size = 0

# N'oubliez pas de débloquer vos messages privés si les logs sont activés!


intents = discord.Intents.all()
intents.members = True



keter = commands.Bot( command_prefix= "keter", description= "keter", intents=intents)


def content_type(file):
    return file.filename.split('.')[-1]




@keter.event
async def on_ready():
    global user_logs

    await keter.change_presence(activity=discord.Game(name='Protege Ton Serveur Des Fichiers Malveillants'))
    print("Prêt!")


    user_logs = keter.get_user(user_logs) if logs else user_logs




@keter.listen()
async def on_message(message):

    author = message.author
    channel = message.channel

    if author.bot:
        return

    for file in message.attachments:
        if len(authorized) and content_type(file).lower() not in authorized:
                await message.delete()
                await channel.send(content=f"L'extensions de ton fichier ['{content_type(file).lower()}'] ne fait pas partie de celles autorisées {authorized} {author.mention}!")
                return


        if await file_verification(file, author, key, max_size, user_logs) if logs else await file_verification(file, author, key, max_size):
            await message.delete()
            await channel.send(content=f"Ton fichier à l'air malveillants {author.mention}!")



keter.run(token)
