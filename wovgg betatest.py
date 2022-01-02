import discord
from discord import Embed, File
from discord.ext import commands
import requests
import urllib.request
import time
import random
from bs4 import BeautifulSoup

client = commands.Bot(command_prefix="!")


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(f"web scraping | !help"))
    print("Bot is ready")

@client.event
async def on_message(message):
    if message.content.startswith("!stats"):
        username = message.content[7:]
        channel = message.channel
        url = 'https://na.op.gg/summoner/userName=' + username
        response = requests.get(url)
        soup = BeautifulSoup(response.text,'lxml')
        rank = soup.find('div', class_="TierRank" )
        LP = soup.find('span', class_="LeaguePoints" )
        WR = soup.find('span', class_="winratio" )
        Champs = soup.find_all('div', class_="ChampionName" )
        Champ_KDA = soup.find_all('span', class_="KDA" )
        Champ_WR = soup.find_all('div', class_="Played" )
        Unranked = soup.find('div', class_="TierRank unranked" )

        #Unranked
        if Unranked != None:
            await channel.send("This user has not played any ranked games recently!")

        #Opening
        #print("\n" + "Summoner stats for: ",username)
        Opening = "\n" + "Summoner stats for: " + str(username)

        #try (NOT DONE)
        #if str(rank) == "None":
            #print("This username does not exist!")
            #quit()

        #Rank
        bigrank = str(rank.text) + ", "

        #LP
        if len(LP.text) == 14:
            LP_text = LP.text[-9:-4]
            #print(bigrank + LP.text[-9:-4])
        elif len(LP.text) == 13:
            LP_text = LP.text[-8:-4]
            #print(bigrank + LP.text[-8:-4])
        elif len(LP.text) == 15:
            LP_text = LP.text[-10:-4]
        else:
            LP_text = LP.text[-12:-4]

        #WR
        #print(WR.text)
        WR = str(WR.text)

        #KDA
        a = 0
        Champ_KDAList = []
        for node in Champ_KDA:
            #print(''.join(node.findAll(text=True)))
            Champ_KDAList.append(''.join(node.findAll(text=True)))
            a += 1
            if a >= 3:
                a = 0
                break

        #ChampWR
        Champ_WRList = []
        for node in Champ_WR:
            #NOT SURE WHAT A NODE IS
            #print(''.join(node.findAll(text=True)))
            Champ_WRList.append(''.join(node.findAll(text=True)))
            a += 1
            if a >= 3:
                a = 0
                break

        for i in range(3):
            Champ_WRList[i] = Champ_WRList[i].replace("\n\n\t\t\t\t\t","")
            Champ_WRList[i] = Champ_WRList[i].replace("\n\t\t\t\t\n", " over ")
            Champ_WRList[i] = Champ_WRList[i].replace("\n", "")

        Champ_List = []
        for text in Champs:
            #print(text.get('title')," KDA: ", Champ_KDAList[a], " WR: ",Champ_WRList[a])
            Champ_List.append(text.get('title'))
            a += 1
            if a >= 3:
                a = 0
                break

        message_1 = "``" + str(Champ_List[0]) + " KDA: " + str(Champ_KDAList[0]) + " WR: "+ str(Champ_WRList[0])+"``"
        message_2 = "``" + str(Champ_List[1]) + " KDA: " + str(Champ_KDAList[1]) + " WR: "+ str(Champ_WRList[1])+"``"
        message_3 = "``" + str(Champ_List[2]) + " KDA: " + str(Champ_KDAList[2]) + " WR: "+ str(Champ_WRList[2])+"``"


        await channel.send(f'{Opening}\n{bigrank + LP_text}\n{WR}\n**-------------------------------------------------------**\nTop champions played in Ranked:\n{message_1}\n{message_2}\n{message_3}')
        #await channel.send(f'Top champions played in Ranked:\n{message_1}\n{message_2}\n{message_3} ')
    await client.process_commands(message)

@client.command(brief="Cumulative hrs in League")
async def lolhours(ctx):
    username = ctx.message.content[10:]
    url = 'https://wol.gg/stats/na/' + username + '/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'lxml')
    leeghrs = soup.find('div',{"id": "time-hours"}, class_= "time center" )
    leeghrs = leeghrs.text
    #print(leeghrs.text)
    leeghrs = leeghrs.replace("hours","")

    await ctx.send(f'{username} has played for {leeghrs} hours!')

@client.command(brief="Convenient Excuse!")
async def excuse(ctx):
    excuses = ["gotta go eat dinner", "Have to do HW", "need to grind physics", "I got an essay to finish up", "need to use the bathroom first", "im too tired",
    "Nah gonna grind Osu","Persona Break","I don't feel like it","i have a dentist appointment","I have to wash the dishes","I’m gonna sleep","Adi is using my computer","my wifi isn’t working"]
    await ctx.send(f'{excuses[random.randint(0, 13)]}')


@client.command(brief="Veggie Tales.")
async def veggietales(ctx):
    await ctx.send(f'If you like to talk to tomatoes,\nIf a squash can make you smile,\nIf you like to waltz with potatoes\nUp and down the produce aisle',tts=True)
    await ctx.send(f'Have we got a show for you!\nVeggieTales!\nBroccoli\nCelery\nGotta be\nVeggieTales!',tts = True)

@client.command(brief="Sussy Gif!!!")
async def sussy(ctx):
    await ctx.send("https://tenor.com/view/imposter-sussy-sus-kronik-gif-21535924")

#@client.command()
#async def helpme(ctx):
    #line_2 = "!excuse: Generates an excuse for why you cant do something. Very Convenient!\n!sealandy: Displays the ranked stats of the infamous Sealandy. Will stop working if he actually plays another champ."
    #await ctx.send(f"`Leegbot version 1.0 Commands:\n!stats <username>: Dislplays Ranked statistics of a summoner, including their top 3 played champions\n!veggietales: For people who like to talk to tomatoes\n{line_2}`")


#@client.command(brief="Chard.zip")
#async def chard(ctx):
    #randompic = str(random.randint(1,14))
    #await ctx.send(file=File(r'C:\Users\Abhishek\AppData\Local\Programs\Python\Python38-32\Richz\Richz SS' + randompic + ".png"))
    

#Valorant
@client.command(brief="Comp + Unrated Playtime")
async def valhours(ctx):
    j = 0
    k = 0
    totalList = []
    for i in range(2):
        modeListOne = ['/agents?season=all','/agents?playlist=unrated&season=all']
        modeListTwo = ['competitive','unrated']
        username = ctx.message.content[10:]
        if "#" in username:
            newusername = username.replace("#","%23")
            #if " " in username:
                #newusername = username.replace(" ","%20")
        #url = 'https://tracker.gg/valorant/profile/riot/' + newusername + '/agents?playlist=competitive'
        url = 'https://tracker.gg/valorant/profile/riot/' + newusername + modeListOne[i]
        response = requests.get(url)
        soup = BeautifulSoup(response.text,'lxml')
        agent = soup.find_all('span', class_="agent__name-name" )
        time = soup.find_all('span', class_="agent__name-time" )
        WR = soup.find_all('div', class_="agent_stat" )

        #hours
        a = 0
        time_List = []
        for node in time:
            #print(text.get('title')," KDA: ", Champ_KDAList[a], " WR: ",Champ_WRList[a])
            time_List.append(''.join(node.findAll(text=True)))
            #print(''.join(node.findAll(text=True)))
            #a += 1
            #if a >= 3:
                #a = 0
                #break

        #agent
        agent_List = []
        for node in agent:
            #print(text.get('title')," KDA: ", Champ_KDAList[a], " WR: ",Champ_WRList[a])
            agent_List.append(''.join(node.findAll(text=True)))
            a += 1
            if a >= 3:
                a = 0
                break

        #WR
        WR_List = []
        for text in WR:
            #print(text.get('title')," KDA: ", Champ_KDAList[a], " WR: ",Champ_WRList[a])
            WR_List.append(text.get())
            print(text.get())
            a += 1
            if a >= 3:
                a = 0
                break
        #KDA
        #agent_KDA_List = []
        #for node in agent_KDA:
            #print(text.get('title')," KDA: ", Champ_KDAList[a], " WR: ",Champ_WRList[a])
            #agent_KDA_List.append(''.join(node.findAll(text=True)))
            #a += 1
            #if a >= 3:
                #a = 0
                #break

        for i in range(len(time_List)):
            if "Played 0" in time_List[i]:
                time_List[i] = time_List[i].replace("Played 0","")
            if "d" in time_List[i]:
                time_List[i] = time_List[i].replace("Played ","")
                d  = "*1440"
                time_List[i] = time_List[i].replace("d",d)
            if "s" in time_List[i]:
                time_List[i] = time_List[i].replace(time_List[i][-4:-1],"")
                time_List[i] = time_List[i].replace("s","")
                #time_List[i] = time_List[i].replace("s","")
                #time_List[i] = time_List[i][:7]
            if "h" in time_List[i]:
                time_List[i] = time_List[i].replace("Played","")
                h  = "*60"
                time_List[i] = time_List[i].replace("h",h)
            if "m" in time_List[i]:
                time_List[i] = time_List[i].replace("Played","")
                m  = "*1"
                time_List[i] = time_List[i].replace("m",m)
            time_List[i] = time_List[i].replace(" ","+")
            if "+0" in time_List[i]:
                time_List[i] = time_List[i].replace("+0","+")
            time_List[i] = eval(time_List[i])

        total_v0 = sum(time_List)/60
        total_vf = round(total_v0,2)
        totalList.append(total_vf)
        #await ctx.send(f'{totalList[j]}')
        #await ctx.send(f'{username} has played a total of {total_vf} hours in competitive!')

        #await ctx.send(f'{username} has played a total of {total_vf} hours in {modeListTwo[j]}!')
        j += 1
        #await ctx.send(f'{username} has played a total of {totalList[0]} hours in {modeListTwo[0]} and {totalList[1]} hours in {modeListTwo[1]}! \n this is a total of {sum(totalList[0] +totalList[1])} hours!')

    #await ctx.send(f'Total = {sum(totalList)}')
    #await ctx.send(f'{totalList[1]}')
    print(totalList[0])
    await ctx.send(f'{username} has played a total of {totalList[0]} hours in competitive and {totalList[1]} hours in unrated! \nThis is a total of **{round(sum(totalList),2)}** hours!')
        #await ctx.send(f'{WR_List}')

@client.command(brief="Top 3 comp agents by playtime")
async def valtop3(ctx):
    username = ctx.message.content[9:]
    if "#" in username:
        newusername = username.replace("#","%23")
        #if " " in username:
           #newusername = username.replace(" ","%20")
    url = 'https://tracker.gg/valorant/profile/riot/' + newusername + '/agents?season=all'
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'lxml')
    agent = soup.find_all('span', class_="agent__name-name" )
    time = soup.find_all('span', class_="agent__name-time" )
    WR = soup.find_all('div', class_="agent_stat" )

    #hours
    a = 0
    time_List = []
    for node in time:
        #print(text.get('title')," KDA: ", Champ_KDAList[a], " WR: ",Champ_WRList[a])
        time_List.append(''.join(node.findAll(text=True)))
        a += 1
        if a >= 3:
            a = 0
            break
    #agent
    agent_List = []
    for node in agent:
        #print(text.get('title')," KDA: ", Champ_KDAList[a], " WR: ",Champ_WRList[a])
        agent_List.append(''.join(node.findAll(text=True)))
        a += 1
        if a >= 3:
            a = 0
            break

    #WR
    WR_List = []
    for text in WR:
        #print(text.get('title')," KDA: ", Champ_KDAList[a], " WR: ",Champ_WRList[a])
        WR_List.append(text.get())
        print(text.get())
        a += 1
        if a >= 3:
            a = 0
            break

    for i in range(3):
        if "d" in time_List[i]:
            time_List[i] = time_List[i].replace("Played ","")
            d  = "*1440"
            time_List[i] = time_List[i].replace("d",d)
        if "s" in time_List[i]:
            time_List[i] = time_List[i].replace(time_List[i][-4:-1],"")
            time_List[i] = time_List[i].replace("s","")
        if "h" in time_List[i]:
            time_List[i] = time_List[i].replace("Played","")
            h  = "*60"
            time_List[i] = time_List[i].replace("h",h)
        if "m" in time_List[i]:
            time_List[i] = time_List[i].replace("Played","")
            m  = "*1"
            time_List[i] = time_List[i].replace("m",m)
        time_List[i] = time_List[i].replace(" ","+")
        if "+0" in time_List[i]:
            time_List[i] = time_List[i].replace("+0","+")
        time_List[i] = eval(time_List[i])

    total_v0 = sum(time_List)/60
    total_vf = round(total_v0,2)

    breaker = "**-----------------------------------------------------------------**"
    await ctx.send(f'The top 3 agents played in comp by {username} are:\n{breaker}\n{agent_List[0]} for {round(time_List[0]/60,2)} hrs\n{agent_List[1]} for {round(time_List[1]/60,2)} hrs\n{agent_List[2]} for {round(time_List[2]/60,2)} hrs')

client.run("NzkxOTYwODM3MjgzMjUwMjE2.X-WxAQ.l6H2la4k60WdT_6vBevv1Z8pdEo")
