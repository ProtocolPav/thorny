import json

import discord
from discord.ext import commands
from modules import help
import functions


gateway_0 = f'''
> **The Gateway Command**
> Here you can find all of the gates and their corresponding numbers!\n

**!gate 1** - Welcome Message For Newbies
**!gate 2** - Quick Command Help
**!gate 3** - Discord Channels Guide
**!gate 4** - Everthorn Donations
'''

gateway_1 = '''
> **Gateway 1 - Welcome Message**
> Welcome to Everthorn!\n

:blue_book: Check out **<#789395875712860222>** for self-roles and the **guidelines!**\n
:postal_horn: Join a **Kingdom** by messaging it's **Ruler!** To see more info, use their `!command`
\t<:flag_ambria:902942850365394964> `!ambria` - **{}**
\t<:flag_asbahamael:900025995929739284> `!asbahamael` - **{}**
\t<:flag_dalvasha:900025995954905098> `!dalvasha` - **{}**
\t<:flag_eireann:900025995912953946> `!eireann` - **{}**
\t<:flag_stregabor:900025995749363733> `!stregabor` - **{}**\n
:incoming_envelope: To get the **Realm Code**, reach **Level 3** by talking here with us and **pick a kingdom**! Then, ask a CM!\n
:person_raising_hand: Use **!gateway** to see more helpful guides for Everthorn!\n
:heart: **Chat** with us more! We are so happy to have you here!
'''

gateway_2 = f'''
> **Gateway 2 - Quick Command Help**
> All of the most useful commands on Thorny!\n

<:ar_bl:862635275230511114>**!remember-birthday [Y-M-D]** - Sets your birthday, to be announced in #players on that day!
<:ar_bl:862635275230511114>**!wiki [Page]** - Sends the wiki article for your specified page
<:ar_bl:862635275230511114>**!rank** - Checks your Server Level!
<:ar_bl:862635275230511114>**!levels** - Sends the Server Level Leaderboard
<:ar_bl:862635275230511114>**!afk** - Sets your AFK status!

<:ar_pi:862635275695554560>**!connect [reminder]** - Logs your connect time. | `!c`
<:ar_pi:862635275695554560>**!disconnect** - Logs your disconnect time. | `!dc`

<:ar_gr:862635275633033226>**!leaderboard** - See all the leaderboards available! | `!lb`
<:ar_gr:862635275633033226>**!lb activity [month]** - Send the activity leaderboard! | `!act`
<:ar_gr:862635275633033226>**!lb nugs [page]** - Send the nugs leaderboard! | `!money`
<:ar_gr:862635275633033226>**!lb treasuries** - See the Kingdom Treasuries! | `!tries, !treasury search`

<:ar_or:862635275799887882>**!bal** - Checks your Nugs Balance | `In Bank`
<:ar_or:862635275799887882>**!pay [@player] [amount] [reason]** - Pays a player! | `In Bank`
<:ar_or:862635275799887882>**!treasury store [amount]** - Donate to your Kingdom! | `!tres store`
<:ar_or:862635275799887882>**!treasury take [amount]** - Take from Treasury | `Only Rulers`
'''

gateway_3 = f'''
> **Gateway 3 - Discord Channel Guide**
> Here is a list of all our channels.

**Everthorn News**
<:ar_bl:862635275230511114><#789395875712860222> - All the guidelines and self-roles of Everthorn
<:ar_bl:862635275230511114><#629033415873921059> - Find all Everthorn news here. **Turn on notifications!**
<:ar_bl:862635275230511114><#690682679489724437> - See who donated or boosted here
<:ar_bl:862635275230511114><#611271483062485032> - Vote on polls, and changes, discussed in <#848873160328740904>
<:ar_bl:862635275230511114><#611714842864123906> - Find joins and leaves, birthday messages and strikes here

**Everthorn Chats**
<:ar_gr:862635275633033226><#687720871972044826> - Chat with citizens and form friendships
<:ar_gr:862635275633033226><#848873160328740904> - Discuss new ideas and the changes that are in <#611271483062485032>
<:ar_gr:862635275633033226><#629398635511283722> - memes.
<:ar_gr:862635275633033226><#620441027043524618> - Use commands and spam here

**Community Posts**
<:ar_or:862635275799887882><#803873438334320641> - Show Everthorn who YOU are by posting your art or music. (**6h Cooldown**)
<:ar_or:862635275799887882><#638439323468955691> - Post realm-related posts here, like ads. (**16h Cooldown**)
<:ar_or:862635275799887882><#821625520545595393> - Set up community or kingdom projects here!
<:ar_or:862635275799887882><#831891696567451653> - Post wiki articles, and look for different articles here
<:ar_or:862635275799887882><#700293298652315648> - Pay people and check your nugs balance here
'''

gateway_4 = f'''
> **Gateway 4 - Everthorn Donations**
> Donations are a way to show your support for Everthorn, by helping it stay up for longer! Don’t worry though, it’s not mandatory. 

**Perks**
You get a wide range of perks for donating:

<:ar_gr:862635275633033226>You get a statue build just for you at spawn!

<:ar_or:862635275799887882>Your donation gets acknowledged in #donations

<:ar_bl:862635275230511114>You get a **permanent** donator role!

<:ar_ye:862635275837243402>You receive nugs, which last for as long as you don’t spend them!

<:ar_pi:862635275695554560>You receive a **Custom Role!** It can be anything you want. It stays for a certain amount of time though.

**PayPal Link**
Donations are only accepted through PayPal, and for safety, 4€ and up.
The realm costs 8€ a month to maintain, and Thorny costs 3€ to maintain.
I pay on the 25th of every month.

https://www.paypal.me/everthorn '''


class Gateway(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['gate', 'g'], help="The Unified Information Command!")
    async def gateway(self, ctx, number=None):
        config_file = open('./../thorny_data/config.json', 'r+')
        config = json.load(config_file)
        if number is None:
            send_text = gateway_0
        elif number == '1':
            send_text = gateway_1.format(config['kingdoms']['ambria']['ruler'],
                                         config['kingdoms']['asbahamael']['ruler'],
                                         config['kingdoms']['dalvasha']['ruler'],
                                         config['kingdoms']['eireann']['ruler'],
                                         config['kingdoms']['stregabor']['ruler'])
        elif number == '2':
            send_text = gateway_2
        elif number == '3':
            send_text = gateway_3
        elif number == '4':
            send_text = gateway_4
        else:
            send_text = gateway_0
        await ctx.send(send_text)

    @commands.command(help="CM Only | Change the ruler within the Gateway Command", hidden=True)
    @commands.has_permissions(administrator=True)
    async def newruler(self, ctx, kingdom, *ruler):
        config['kingdoms'][f'{kingdom.lower()}']['ruler'] = f'{" ".join(ruler)}'
        json.dump(config, open('./../thorny_data/config.json', 'w'), indent=3)

    @commands.command(help="Shows the kingdom description for Asbahamael", aliases=['asba'])
    async def asbahamael(self, ctx):
        kingdom = "asbahamael"
        config_file = open('./../thorny_data/config.json', 'r+')
        config = json.load(config_file)

        kingdom_embed = discord.Embed(title=f"**{kingdom.capitalize()}, {config['kingdoms'][kingdom]['slogan']}**",
                                      color=0xE1C16E)
        kingdom_embed.add_field(name=f":city_sunset: **Information**",
                                value=f"**Ruler:** {config['kingdoms'][kingdom]['ruler']}\n"
                                      f"**Capital City:** {config['kingdoms'][kingdom]['capital']}\n"
                                      f"**Towns:** {config['kingdoms'][kingdom]['towns']}\n\n"
                                      f"**Kingdom Borders:** {config['kingdoms'][kingdom]['borders']}\n"
                                      f"**Government:** {config['kingdoms'][kingdom]['government']}\n"
                                      f"**Alliances:** {config['kingdoms'][kingdom]['alliances']}")
        kingdom_embed.add_field(name=f":bar_chart: **Statistics**",
                                value=f"**Kingdom Treasury:** <:Nug:884320353202081833>"
                                      f"{config['kingdoms'][kingdom]['nugs_treasury']}\n"
                                      f"**Citizen Balances:** <:Nug:884320353202081833>"
                                      f"{config['kingdoms'][kingdom]['nugs_total']}\n"
                                      f"**Kingdom Activity:** {config['kingdoms'][kingdom]['playtime_total']}\n"
                                      f"**Members:** {config['kingdoms'][kingdom]['members']}\n"
                                      f"**Popularity Poll Rating:** {config['kingdoms'][kingdom]['poll_ratings']}\n"
                                      f"**Started On:** {config['kingdoms'][kingdom]['created_on']}")
        kingdom_embed.add_field(name=f"**Kingdom Wiki Page**",
                                value=f"{config['kingdoms'][kingdom]['wiki.gov']}",
                                inline=False)
        kingdom_embed.add_field(name=":scroll: **Description**",
                                value=f"{config['kingdoms'][kingdom]['description']}",
                                inline=False)
        kingdom_embed.add_field(name=":postal_horn: **Kingdom Lore**",
                                value=f"{config['kingdoms'][kingdom]['lore']}",
                                inline=False)

        await ctx.send(embed=kingdom_embed)

    @commands.command(help="Shows the kingdom description for Ambria")
    async def ambria(self, ctx):
        kingdom = "ambria"
        config_file = open('./../thorny_data/config.json', 'r+')
        config = json.load(config_file)

        kingdom_embed = discord.Embed(title=f"**{kingdom.capitalize()}, {config['kingdoms'][kingdom]['slogan']}**",
                                      color=0xFFD700)
        kingdom_embed.add_field(name=f":city_sunset: **Information**",
                                value=f"**Ruler:** {config['kingdoms'][kingdom]['ruler']}\n"
                                      f"**Capital City:** {config['kingdoms'][kingdom]['capital']}\n"
                                      f"**Towns:** {config['kingdoms'][kingdom]['towns']}\n\n"
                                      f"**Kingdom Borders:** {config['kingdoms'][kingdom]['borders']}\n"
                                      f"**Government:** {config['kingdoms'][kingdom]['government']}\n"
                                      f"**Alliances:** {config['kingdoms'][kingdom]['alliances']}")
        kingdom_embed.add_field(name=f":bar_chart: **Statistics**",
                                value=f"**Kingdom Treasury:** <:Nug:884320353202081833>"
                                      f"{config['kingdoms'][kingdom]['nugs_treasury']}\n"
                                      f"**Citizen Balances:** <:Nug:884320353202081833>"
                                      f"{config['kingdoms'][kingdom]['nugs_total']}\n"
                                      f"**Kingdom Activity:** {config['kingdoms'][kingdom]['playtime_total']}\n"
                                      f"**Members:** {config['kingdoms'][kingdom]['members']}\n"
                                      f"**Popularity Poll Rating:** {config['kingdoms'][kingdom]['poll_ratings']}\n"
                                      f"**Started On:** {config['kingdoms'][kingdom]['created_on']}")
        kingdom_embed.add_field(name=f"**Kingdom Wiki Page**",
                                value=f"{config['kingdoms'][kingdom]['wiki.gov']}",
                                inline=False)
        kingdom_embed.add_field(name=":scroll: **Description**",
                                value=f"{config['kingdoms'][kingdom]['description']}",
                                inline=False)
        kingdom_embed.add_field(name=":postal_horn: **Kingdom Lore**",
                                value=f"{config['kingdoms'][kingdom]['lore']}",
                                inline=False)

        await ctx.send(embed=kingdom_embed)

    @commands.command(help="Shows the kingdom description for Dalvasha", aliases=['dal'])
    async def dalvasha(self, ctx):
        kingdom = "dalvasha"
        config_file = open('./../thorny_data/config.json', 'r+')
        config = json.load(config_file)

        kingdom_embed = discord.Embed(title=f"**{kingdom.capitalize()}, {config['kingdoms'][kingdom]['slogan']}**",
                                      color=0xC70039)
        kingdom_embed.add_field(name=f":city_sunset: **Information**",
                                value=f"**Ruler:** {config['kingdoms'][kingdom]['ruler']}\n"
                                      f"**Capital City:** {config['kingdoms'][kingdom]['capital']}\n"
                                      f"**Towns:** {config['kingdoms'][kingdom]['towns']}\n\n"
                                      f"**Kingdom Borders:** {config['kingdoms'][kingdom]['borders']}\n"
                                      f"**Government:** {config['kingdoms'][kingdom]['government']}\n"
                                      f"**Alliances:** {config['kingdoms'][kingdom]['alliances']}")
        kingdom_embed.add_field(name=f":bar_chart: **Statistics**",
                                value=f"**Kingdom Treasury:** <:Nug:884320353202081833>"
                                      f"{config['kingdoms'][kingdom]['nugs_treasury']}\n"
                                      f"**Citizen Balances:** <:Nug:884320353202081833>"
                                      f"{config['kingdoms'][kingdom]['nugs_total']}\n"
                                      f"**Kingdom Activity:** {config['kingdoms'][kingdom]['playtime_total']}\n"
                                      f"**Members:** {config['kingdoms'][kingdom]['members']}\n"
                                      f"**Popularity Poll Rating:** {config['kingdoms'][kingdom]['poll_ratings']}\n"
                                      f"**Started On:** {config['kingdoms'][kingdom]['created_on']}")
        kingdom_embed.add_field(name=f"**Kingdom Wiki Page**",
                                value=f"{config['kingdoms'][kingdom]['wiki.gov']}",
                                inline=False)
        kingdom_embed.add_field(name=":scroll: **Description**",
                                value=f"{config['kingdoms'][kingdom]['description']}",
                                inline=False)
        kingdom_embed.add_field(name=":postal_horn: **Kingdom Lore**",
                                value=f"{config['kingdoms'][kingdom]['lore']}",
                                inline=False)

        await ctx.send(embed=kingdom_embed)

    @commands.command(help="Shows the kingdom description for Eireann", aliases=['eir'])
    async def eireann(self, ctx):
        kingdom = "eireann"
        config_file = open('./../thorny_data/config.json', 'r+')
        config = json.load(config_file)

        kingdom_embed = discord.Embed(title=f"**{kingdom.capitalize()}, {config['kingdoms'][kingdom]['slogan']}**",
                                      color=0x4169E1)
        kingdom_embed.add_field(name=f":city_sunset: **Information**",
                                value=f"**Ruler:** {config['kingdoms'][kingdom]['ruler']}\n"
                                      f"**Capital City:** {config['kingdoms'][kingdom]['capital']}\n"
                                      f"**Towns:** {config['kingdoms'][kingdom]['towns']}\n\n"
                                      f"**Kingdom Borders:** {config['kingdoms'][kingdom]['borders']}\n"
                                      f"**Government:** {config['kingdoms'][kingdom]['government']}\n"
                                      f"**Alliances:** {config['kingdoms'][kingdom]['alliances']}")
        kingdom_embed.add_field(name=f":bar_chart: **Statistics**",
                                value=f"**Kingdom Treasury:** <:Nug:884320353202081833>"
                                      f"{config['kingdoms'][kingdom]['nugs_treasury']}\n"
                                      f"**Citizen Balances:** <:Nug:884320353202081833>"
                                      f"{config['kingdoms'][kingdom]['nugs_total']}\n"
                                      f"**Kingdom Activity:** {config['kingdoms'][kingdom]['playtime_total']}\n"
                                      f"**Members:** {config['kingdoms'][kingdom]['members']}\n"
                                      f"**Popularity Poll Rating:** {config['kingdoms'][kingdom]['poll_ratings']}\n"
                                      f"**Started On:** {config['kingdoms'][kingdom]['created_on']}")
        kingdom_embed.add_field(name=f"**Kingdom Wiki Page**",
                                value=f"{config['kingdoms'][kingdom]['wiki.gov']}",
                                inline=False)
        kingdom_embed.add_field(name=":scroll: **Description**",
                                value=f"{config['kingdoms'][kingdom]['description']}",
                                inline=False)
        kingdom_embed.add_field(name=":postal_horn: **Kingdom Lore**",
                                value=f"{config['kingdoms'][kingdom]['lore']}",
                                inline=False)

        await ctx.send(embed=kingdom_embed)

    @commands.command(help="Shows the kingdom description for Stregabor", aliases=['streg'])
    async def stregabor(self, ctx):
        kingdom = "stregabor"
        config_file = open('./../thorny_data/config.json', 'r+')
        config = json.load(config_file)

        kingdom_embed = discord.Embed(title=f"**{kingdom.capitalize()}, {config['kingdoms'][kingdom]['slogan']}**",
                                      color=0x89CFF0)
        kingdom_embed.add_field(name=f":city_sunset: **Information**",
                                value=f"**Ruler:** {config['kingdoms'][kingdom]['ruler']}\n"
                                      f"**Capital City:** {config['kingdoms'][kingdom]['capital']}\n"
                                      f"**Towns:** {config['kingdoms'][kingdom]['towns']}\n\n"
                                      f"**Kingdom Borders:** {config['kingdoms'][kingdom]['borders']}\n"
                                      f"**Government:** {config['kingdoms'][kingdom]['government']}\n"
                                      f"**Alliances:** {config['kingdoms'][kingdom]['alliances']}")
        kingdom_embed.add_field(name=f":bar_chart: **Statistics**",
                                value=f"**Kingdom Treasury:** <:Nug:884320353202081833>"
                                      f"{config['kingdoms'][kingdom]['nugs_treasury']}\n"
                                      f"**Citizen Balances:** <:Nug:884320353202081833>"
                                      f"{config['kingdoms'][kingdom]['nugs_total']}\n"
                                      f"**Kingdom Activity:** {config['kingdoms'][kingdom]['playtime_total']}\n"
                                      f"**Members:** {config['kingdoms'][kingdom]['members']}\n"
                                      f"**Popularity Poll Rating:** {config['kingdoms'][kingdom]['poll_ratings']}\n"
                                      f"**Started On:** {config['kingdoms'][kingdom]['created_on']}")
        kingdom_embed.add_field(name=f"**Kingdom Wiki Page**",
                                value=f"{config['kingdoms'][kingdom]['wiki.gov']}",
                                inline=False)
        kingdom_embed.add_field(name=":scroll: **Description**",
                                value=f"{config['kingdoms'][kingdom]['description']}",
                                inline=False)
        kingdom_embed.add_field(name=":postal_horn: **Kingdom Lore**",
                                value=f"{config['kingdoms'][kingdom]['lore']}",
                                inline=False)

        await ctx.send(embed=kingdom_embed)

    @commands.command(help="Ruler Only | Edit what your Kingdom Command says", aliases=['kingdom'])
    @commands.has_role('Ruler')
    async def kedit(self, ctx, field=None, *value):
        kingdom = 'None'
        kingdoms_list = ['Stregabor', 'Ambria', 'Eireann', 'Dalvasha', 'Asbahamael']
        for item in kingdoms_list:
            if discord.utils.find(lambda r: r.name == item, ctx.message.guild.roles) in ctx.author.roles:
                kingdom = item.lower()
                functions.profile_update(user, kingdom, "kingdom")

        config_file = open('./../thorny_data/config.json', 'r+')
        config = json.load(config_file)
        wrong_field = False

        if field.lower() == "ruler":
            if len(" ".join(value)) <= 35:
                config['kingdoms'][kingdom]['ruler'] = " ".join(value)
            else:
                await ctx.send('Hmmmm... Seems like this was more than 35 characters')
                wrong_field = True

        elif field.lower() == "slogan":
            if len(" ".join(value)) <= 25:
                config['kingdoms'][kingdom]['slogan'] = " ".join(value)
            else:
                await ctx.send("That's over 25 characters!")
                wrong_field = True

        elif field.lower() == "capital":
            if len(" ".join(value)) <= 30:
                config['kingdoms'][kingdom]['capital'] = " ".join(value)
            else:
                await ctx.send('Seems like one long name for a town! (over 30 characters)'
                               '\nLet Pav know if I made a mistake!')
                wrong_field = True

        elif field.lower() == "borders":
            if len(" ".join(value)) <= 30:
                config['kingdoms'][kingdom]['borders'] = " ".join(value)
            else:
                await ctx.send("That's over 30 characters!")
                wrong_field = True

        elif field.lower() == "government":
            if len(value) <= 5 and len(" ".join(value)) <= 30:
                config['kingdoms'][kingdom]['government'] = " ".join(value)
            else:
                await ctx.send('That seems like over 30 characters!')
                wrong_field = True

        elif field.lower() == "alliances" or field.lower() == "alliance":
            if len(" ".join(value)) <= 50:
                config['kingdoms'][kingdom]['alliances'] = " ".join(value)
            else:
                await ctx.send('This looks like it is more than 50 characters!')
                wrong_field = True

        elif field.lower() == "wiki" or field.lower() == "article":
            if 'https://everthorn.fandom.com/wiki/' in " ".join(value):
                config['kingdoms'][kingdom]['wiki.gov'] = " ".join(value)
            else:
                await ctx.send('Woah there buckaroo! This doesnt look like no wiki link...')
                wrong_field = True

        elif field.lower() == "description":
            if len(" ".join(value)) <= 250:
                config['kingdoms'][kingdom]['description'] = " ".join(value)
            else:
                await ctx.send('This looks like it is more than 30 words! (over 250 characters)')
                wrong_field = True

        elif field.lower() == "lore" or field.lower() == "story":
            if len(" ".join(value)) <= 250:
                config['kingdoms'][kingdom]['lore'] = " ".join(value)
            else:
                await ctx.send('This looks like it is more than 30 words! (over 250 characters)')
                wrong_field = True

        else:
            await help.Help.kingdoms(self, ctx)
            wrong_field = True

        if not wrong_field:
            config_file.truncate(0)
            config_file.seek(0)
            json.dump(config, config_file, indent=3)
            config_file.close()
            await ctx.send(f"Done! Now the **{field}** of **{kingdom.capitalize()}** is '*{' '.join(value)}*'")