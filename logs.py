import discord
from datetime import datetime


def transaction(payable_id, receivable_id, amount, reason):
    if type(receivable_id) == int:
        log_embed = discord.Embed(color=0xF4C430)
        log_embed.add_field(name="**Transaction**",
                            value=f"<@{payable_id}> paid <@{receivable_id}> **<:Nug:884320353202081833>{amount}**\n"
                                  f"Reason: {reason}")
    else:
        log_embed = discord.Embed(color=0xF4C430)
        log_embed.add_field(name="**Transaction**",
                            value=f"<@{payable_id}> paid {receivable_id} **<:Nug:884320353202081833>{amount}**\n"
                                  f"Reason: {reason}")
    log_embed.set_footer(text=f'{datetime.now().replace(microsecond=0)}')
    return log_embed


def balance_edit(moderator, receivable_id, amount):
    log_embed = discord.Embed(color=0xF4C430)
    log_embed.add_field(name="**Balance Edit**",
                        value=f"<@{moderator}> edited <@{receivable_id}>'s balance\n"
                              f"Add/Remove: **{amount}<:Nug:884320353202081833>**\n")
    log_embed.set_footer(text=f'{datetime.now().replace(microsecond=0)}')
    return log_embed


def gulag(moderator, user_id):
    log_embed = discord.Embed(color=0xF4C430)
    log_embed.add_field(name="**Gulag**",
                        value=f"<@{moderator}> gulaged <@{user_id}>")
    log_embed.set_footer(text=f'{datetime.now().replace(microsecond=0)}')
    return log_embed


def message_delete(message):
    log_embed = discord.Embed(color=0xF4C430)
    if message.content is not None:
        log_embed.add_field(name="**Message Deleted**",
                            value=f"{message.author.mention} deleted a message in "
                                  f"<#{message.channel.id}>:\n{message.content}")
        log_embed.set_footer(text=f'{datetime.now().replace(microsecond=0)}')
        return log_embed
    else:
        return None


def message_edit(before, after):
    log_embed = discord.Embed(color=0xF4C430)
    if before.content != after.content:
        log_embed.add_field(name="**Message Edited**",
                            value=f"{before.author.mention} edited a message in <#{before.channel.id}>:\n"
                                  f"**BEFORE:**\n{before.content}\n**AFTER:**\n{after.content}")
        log_embed.set_footer(text=f'{datetime.now().replace(microsecond=0)}')
        return log_embed
    else:
        return None
