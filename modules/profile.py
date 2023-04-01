from datetime import datetime, timedelta
import discord
from discord.ext import commands
from discord import utils
import json
from thorny_core.uikit import slashoptions, views, embeds
from thorny_core.db import UserFactory, commit, GuildFactory, generator

version_json = json.load(open('./version.json', 'r'))
v = version_json["version"]


class Profile(commands.Cog):
    def __init__(self, client):
        self.client: discord.Client = client

    @commands.slash_command(description="See your or a user's profile",
                            guild_ids=GuildFactory.get_guilds_by_feature('PROFILE'))
    async def profile(self, ctx: discord.ApplicationContext,
                      user: discord.Option(discord.Member, "See someone's profile. Leave blank to see yours.",
                                           default=None)):
        if user is None:
            user = ctx.author
        thorny_user = await UserFactory.build(user)

        if discord.utils.find(lambda r: r.name == 'Legacy Donator Role', ctx.guild.roles) in user.roles:
            is_donator = f'I donated to Everthorn!'
        elif discord.utils.find(lambda r: r.name == 'Patreon Supporter', ctx.guild.roles) in user.roles:
            is_donator = 'I am an Everthorn Patreon Supporter!'
        else:
            is_donator = ''

        pages = [await embeds.profile_main_embed(thorny_user, is_donator),
                 await embeds.profile_lore_embed(thorny_user),
                 await embeds.profile_stats_embed(thorny_user)]
        await ctx.respond(embed=pages[0], view=views.Profile(thorny_user, pages, ctx))

    birthday = discord.SlashCommandGroup("birthday", "Birthday commands",
                                         guild_ids=GuildFactory.get_guilds_by_feature('PROFILE'))

    @birthday.command(description="Set your birthday")
    async def set(self, ctx, month: discord.Option(str, "Pick or type a month",
                                                   autocomplete=utils.basic_autocomplete(slashoptions.months)),
                  day: discord.Option(int, "Pick or type a day",
                                      autocomplete=utils.basic_autocomplete(slashoptions.days)),
                  year: discord.Option(int, "Pick or type a year",
                                       autocomplete=utils.basic_autocomplete(slashoptions.years))):
        if year is not None:
            date = f'{month} {day} {year}'
            date_system = datetime.strptime(date, "%B %d %Y")
        else:
            date = f'{month} {day}'
            date_system = datetime.strptime(date, "%B %d")

        thorny_user = await UserFactory.build(ctx.author)
        thorny_user.birthday.time = date_system
        await commit(thorny_user)
        await ctx.respond(f"Your Birthday is set to: **{thorny_user.birthday}**", ephemeral=True)

    @birthday.command(description="Remove your birthday")
    async def remove(self, ctx):
        thorny_user = await UserFactory.build(ctx.author)
        thorny_user.birthday.time = None
        await commit(thorny_user)
        await ctx.respond(f"I've removed your birthday! You'll lose out on Birthday messages :(",
                          ephemeral=True)

    gamertag = discord.SlashCommandGroup("gamertag", "Gamertag commands",
                                         guild_ids=GuildFactory.get_guilds_by_feature('EVERTHORN'))

    @gamertag.command(description="Search the database for gamertags")
    async def search(self, ctx: discord.ApplicationContext, gamertag: discord.Option(str, "Enter parts of a gamertag")):
        gamertags = await UserFactory.get_gamertags(ctx.guild.id, gamertag[0:4])
        send_text = []
        for tag in gamertags:
            send_text.append(f"<@{tag['user_id']}> • {tag['whitelisted_gamertag']}")
        if not send_text:
            send_text.append("No matches found!")

        gamertag_embed = discord.Embed(colour=0x64d5ac)
        gamertag_embed.add_field(name=f"**Gamertags matching `{gamertag}`:**",
                                 value="\n".join(send_text))
        await ctx.respond(embed=gamertag_embed)

    @commands.slash_command(description="See all upcoming birthdays!")
    async def birthdays(self, ctx: discord.ApplicationContext):
        thorny_user = await UserFactory.build(ctx.user)
        upcoming_bdays = await generator.upcoming_birthdays(thorny_user.connection_pool)
        events_embed = discord.Embed(title="Birthdays", colour=0xFF69B4)
        for user in upcoming_bdays:
            if user['guild_id'] == thorny_user.guild.guild_id:
                temp_thorny_user = await UserFactory.fetch_by_id(thorny_user.guild, user['thorny_user_id'])

                if str(temp_thorny_user.age + 1)[-1] == "1":
                    suffix = "st"
                elif str(temp_thorny_user.age + 1)[-1] == "2":
                    suffix = "nd"
                elif str(temp_thorny_user.age + 1)[-1] == "3":
                    suffix = "rd"
                else:
                    suffix = "th"

                birthday_found = False
                for field in events_embed.fields:
                    if str(temp_thorny_user.birthday).split(',')[0] == field.name:
                        field.value = f"{field.value}\n{temp_thorny_user.username} • {temp_thorny_user.age + 1}{suffix} birthday"
                        birthday_found = True

                if not birthday_found:
                    events_embed.add_field(name=str(temp_thorny_user.birthday).split(',')[0],
                                           value=f"{temp_thorny_user.username} • {temp_thorny_user.age + 1}{suffix} birthday")

        await ctx.respond(embed=events_embed)
