import os
import random
import re
from datetime import timezone
from os.path import exists
from time import time

import discord
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('BOT_TOKEN')

league_channel = int(os.getenv('LEAGUE_CHANNEL'))
league_cooldowns = {}

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_member_update(before, after):
    game = [i for i in after.activities if str(
        i.type) == "ActivityType.playing"]
    for i in game:
        if i.name.lower() == "league of legends" and time() > league_cooldowns.get(after.id, 0):
            if i.start:
                await client.get_channel(league_channel).send(
                    f"{after.mention}, stop playing league! You have been playing for {int(time() - i.start.replace(tzinfo=timezone.utc).timestamp())} seconds")
            else:
                await client.get_channel(league_channel).send(
                    f"{after.mention}, stop playing league!")
            league_cooldowns.pop(after.id, None)
            league_cooldowns[after.id] = time() + 3600

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 69*random.random() < 1:
        filename = os.getcwd() + '/points/' + str(message.author.id) + '.txt'

        if exists(filename):
            f = open(filename, 'r')
            score = int(f.readline())
            f.close()
        else:
            score = 0

        score += 1
        f = open(filename, 'w')
        f.write(str(score))
        f.close()
        print("gave out some points")
        # react to message to indicate a point has been earnt
        await message.add_reaction(':bungalow:980140106868477973')
        # old code
        # await message.channel.send("Congratulations, you have earnt 1 bungalow point. You now have " + str(score) + " points! Don't spend them all in one place!")

    if message.content.startswith('$points'):
        filename = os.getcwd() + '/points/' + str(message.author.id) + '.txt'

        if not exists(filename):
            await message.channel.send("You have 0 points. Send some messages. Or else.")
            return

        f = open(filename, 'r')
        score = int(f.readline())
        f.close()
        await message.channel.send("You have " + str(score) + " points!")
        return

    if message.content.startswith('$help'):
        await message.channel.send("""Hello! I am quotebot3000. Usage:

$addquote [name] [quote] - this adds a quote to the given person!

$quote [name] - this will output a random quote by the given person!

$quote - this will output a random quote by a random person! (because I am doing this fast this will transfer across servers, so you can get quotes entered by users on other servers)""")

    if message.content.lower().startswith('$addquote '):
        try:
            # max split of 3, so [0] is '$quote', [1] is the name and [2] is the quote
            content = message.content.split(' ', 2)
            if content[1].lower().startswith('<'):
                ID = re.findall('[0-9]+', content[1].lower())[0]
                filename = os.getcwd() + '/quote-files/' + ID + '.txt'
            else:
                filename = os.getcwd() + '/quote-files/' + \
                    content[1].lower() + '.txt'
            if not exists(filename):
                towrite = content[2]
            else:
                towrite = '\n' + content[2]
            f = open(filename, 'a')
            f.write(towrite)
            f.close()
            await message.channel.send('Quote by ' + content[1] + ' has been stored!')

        except Exception as e:
            print(e)
            await message.channel.send('Badly formatted $addquote attempt! Use $help for more info.')

        finally:
            return

    if message.content.lower().startswith('$quote'):
        try:
            content = message.content.split()
            if message.content.lower() == '$quote':  # if the user has entered only '$quote'
                filename = os.getcwd() + '/quote-files/' + \
                    random.choice(os.listdir(os.getcwd() + '/quote-files'))
                out = ' - Someone'
            else:
                if content[1].lower().startswith('<'):
                    ID = re.findall('[0-9]+', content[1].lower())[0]
                    filename = os.getcwd() + '/quote-files/' + ID + '.txt'
                else:
                    filename = os.getcwd() + '/quote-files/' + \
                        content[1].lower() + '.txt'
                out = ' - ' + content[1]
            f = open(filename, 'r')
            quotes = f.readlines()
            f.close()
            selected_quote = random.choice(quotes)
            await message.channel.send(selected_quote + out)

        except Exception as e:
            print(e)
            await message.channel.send('Badly formatted $quote attempt! Are you sure that person has quotes? Use $help for more info.')

        finally:
            return

client.run(token)
