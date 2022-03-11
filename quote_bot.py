from pydoc import cli
from dotenv import load_dotenv
import random
import discord
import os

load_dotenv()

token = os.getenv('BOT_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$help'):
        await message.channel.send("""Hello! I am quotebot3000. Usage:

$addquote [name] [quote] - this adds a quote to the given person!

$quote [name] - this will output a random quote by the given person!

$quote - this will output a random quote by a random person! (because I am doing this fast this will transfer across servers, so you can get quotes entered by users on other servers)""")

    if message.content.lower().startswith('$addquote'):
        try:
            content = message.content.split(' ', 2) #max split of 3, so [0] is '$quote', [1] is the name and [2] is the quote
            filename = os.getcwd() + '/quote-files/' + content[1].lower() + '.txt'
            f = open(filename, 'a')
            f.write('\n' + content[2])
            f.close()
            await message.channel.send('Quote by ' + content[1] + ' has been stored!')

        except Exception as e:
            print(e)
            await message.channel.send('Badly formatted $addquote attempt!')

        finally:
            return

    if message.content.lower().startswith('$quote'):
        try:
            content = message.content.split()
            if message.content.lower() == '$quote': #if the user has entered only '$quote'
                filename = os.getcwd() + '/quote-files/' + random.choice(os.listdir(os.getcwd() + '/quote-files'))
                out = ' - Someone'
            else:
                filename = os.getcwd() + '/quote-files/' + content[1].lower() + '.txt'
                out = ' - ' + content[1]
            f = open(filename, 'r')
            quotes = f.readlines()
            f.close()
            selected_quote = random.choice(quotes)
            await message.channel.send(selected_quote + out)

        except Exception as e:
            print(e)
            await message.channel.send('Badly formatted $quote attempt! Are you sure that person has quotes?')

        finally:
            return

client.run(token)