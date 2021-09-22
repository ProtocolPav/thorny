import json

import discord
from discord.ext import commands


config_file = open('config.json', 'r+')
config = json.load(config_file)
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
\t:coin: `!ambria` - **{}**
\t:star2: `!asbahamael` - **{}**
\t:japanese_castle: `!dalvasha` - **{}**
\t:classical_building: `!eireann` - **{}**
\t:dove: `!stregabor` - **{}**\n
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

    @commands.command(aliases=['gate', 'g', 'ga'])
    async def gateway(self, ctx, gatenum=None):
        config_file = open('config.json', 'r+')
        config = json.load(config_file)
        send_text = ''
        if gatenum is None:
            send_text = gateway_0
        elif gatenum == '1':
            send_text = gateway_1.format(config['gateways']['ruler_ambria'], config['gateways']['ruler_asbahamael'],
                                         config['gateways']['ruler_dalvasha'], config['gateways']['ruler_eireann'],
                                         config['gateways']['ruler_stregabor'])
        elif gatenum == '2':
            send_text = gateway_2
        elif gatenum == '3':
            send_text = gateway_3
        elif gatenum == '4':
            send_text = gateway_4
        else:
            send_text = gateway_0
        await ctx.send(f'{send_text}')

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def newruler(self, ctx, kingdom, *ruler):
        config['gateways'][f'ruler_{kingdom.lower()}'] = f'{" ".join(ruler)}'
        json.dump(config, open('config.json', 'w'), indent=3)