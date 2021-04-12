import discord
import asyncio
import json
import random
import os
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import requests

client = discord.Client()



with open('data.json', 'r') as f:
    data = json.load(f)

with open('coin.json', 'r') as f:
    coin = json.load(f)





@client.event
async def on_ready():
    await bt()

@client.event
async def on_message(message):


    if message.content.startswith("제리야"):
        if str(message.author.id) not in coin:
            coin[str(message.author.id)] = [500000, 0, 0]
        if message.content[4:] == "":
            async with message.channel.typing():
                await asyncio.sleep(0.07)
            await message.channel.send('🤔')
        else:
            vote = message.content[4:].split(" ")
            a = vote[0]

        if a == "도움":
            embed = discord.Embed(title="정찰목록", description="-제리", color=0xFFE400)
            embed.add_field(name="제리야 배워", value="사용법:```제리야 배워 (단어)/(뜻)```\n단어에는 띄어쓰기를 사용할수 없어요.", inline=True)
            embed.add_field(name="제리야 코인", value="사용법:```제리야 종목```\n종목들을 한번에 확인하세요!", inline=True)
            await message.channel.send(embed=embed)

        elif a == "배워":
            i = message.content[7:].split("/")
            if i[0] in data:
                data[i[0]].append(i[1])
                coin[str(message.author.id)][0] += 300
            else:
                data[i[0]] = [i[1]]
                coin[str(message.author.id)][0] += 300

            await message.channel.send("ㅇㅇ")

        elif a == "디버깅":
            await message.channel.send(data[vote[1]])
            for i in data:
                print(i)

        elif a == "개발자":
           if message.author.id ==  507504723184844813:
                if vote[1] == "삭제":
                   i = message.content[11:].split("/")
                   await message.channel.send("`" + str(data[i[0]]) + "`1에서 `" + i[1] + "`삭제")
                   data[i[0]].remove(i[1])
                if vote[1] == "삭제2":
                    i = message.content[12:]
                    await message.channel.send(i)
                    del data[i]

        elif a == "종목":
            embed = discord.Embed(title="종목", description="자산 : " + str(coin[str(message.author.id)][0]), color=0xFFE400)
            embed.add_field(name="톰코인", value=str(coin["coin"]), inline=True)
            embed.add_field(name="제리전자", value=str(coin["coin2"]), inline=True)
            await message.channel.send(embed=embed)

        elif a == "톰코인":
            try:
                if vote[1] == "매수":
                    if coin[str(message.author.id)][0] >= coin["coin"] * int(vote[2]):
                        coin[str(message.author.id)][0] -= coin["coin"] * int(vote[2])
                        coin[str(message.author.id)][1] += int(vote[2])

                
                if vote[1] == "매도":
                    if coin[str(message.author.id)][1] >= int(vote[2]):
                        coin[str(message.author.id)][0] += coin["coin"] * int(vote[2])
                        coin[str(message.author.id)][1] -= int(vote[2])

            except IndexError:
                pass

            embed = discord.Embed(title="톰코인", description="현재가 : " + str(coin["coin"]), color=0xFFE400)
            embed.add_field(name="총평가", value=str(coin["coin"] * coin[str(message.author.id)][1]), inline=True)
            embed.add_field(name="자산", value=str(coin[str(message.author.id)][0]), inline=True)
            embed.add_field(name="매도가능", value=str(coin[str(message.author.id)][1]), inline=True)
            await message.channel.send(embed=embed)

        elif a == "제리전자":
            try:
                if vote[1] == "매수":
                    if coin[str(message.author.id)][0] >= coin["coin2"] * int(vote[2]):
                        coin[str(message.author.id)][0] -= coin["coin2"] * int(vote[2])
                        coin[str(message.author.id)][2] += int(vote[2])

                
                if vote[1] == "매도":
                    if coin[str(message.author.id)][2] >= int(vote[2]):
                        coin[str(message.author.id)][0] += coin["coin2"] * int(vote[2])
                        coin[str(message.author.id)][2] -= int(vote[2])

            except IndexError:
                pass

            embed = discord.Embed(title="제리전자", description="현재가 : " + str(coin["coin2"]), color=0xFFE400)
            embed.add_field(name="총평가", value=str(coin["coin2"] * coin[str(message.author.id)][1]), inline=True)
            embed.add_field(name="자산", value=str(coin[str(message.author.id)][0]), inline=True)
            embed.add_field(name="매도가능", value=str(coin[str(message.author.id)][2]), inline=True)
            await message.channel.send(embed=embed)

        else:
            if a in data:
                await message.channel.send(data[a][random.randrange(0, len(data[a]))])
                coin[str(message.author.id)][0] += 100
                

    with open('data.json', 'w') as f:
        json.dump(data, f, indent="\t")

    with open('coin.json', 'w') as f:
        json.dump(coin, f, indent="\t")

async def bt():
    await client.wait_until_ready()

    while not client.is_closed():

        if random.choice([True, False]):
            coin["coin"] += 1000
            if random.choice([True, False]):
                coin["coin2"] += 500
                await client.change_presence(status=discord.Status.online, activity=discord.Game("톰코인 : " + str(coin["coin"]) + "↑\n제리전자 : " + str(coin["coin2"]) + "↑"))
            else:
                if coin["coin2"] != 0:
                    coin["coin2"] -= 500
                    await client.change_presence(status=discord.Status.online, activity=discord.Game("톰코인 : " + str(coin["coin"]) + "↑\n제리전자 : " + str(coin["coin2"]) + "↓"))
        else:
            if coin["coin"] != 0:
                coin["coin"] -= 1000
            if random.choice([True, False]):
                coin["coin2"] += 500
                await client.change_presence(status=discord.Status.online, activity=discord.Game("톰코인 : " + str(coin["coin"]) + "↓\n제리전자 : " + str(coin["coin2"]) + "↑"))
            else:
                if coin["coin2"] != 0:
                    coin["coin2"] -= 500
                    await client.change_presence(status=discord.Status.online, activity=discord.Game("톰코인 : " + str(coin["coin"]) + "↓\n제리전자 : " + str(coin["coin2"]) + "↓"))
    
        await asyncio.sleep(random.randrange(4, 6))





client.run(os.environ['token'])
