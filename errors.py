import discord


class Activity:
    connect_error = discord.Embed(color=0xD70040)
    connect_error.add_field(name="Aww... Shucks",
                            value="I don't recall you connecting actually...")


class Pay:
    self_error = discord.Embed(color=0xD70040)
    self_error.add_field(name='Poops...',
                         value='>You tried to pay yourself.\n>It did not work.\n>You feel stupid.')

    amount_error = discord.Embed(color=0xD70040)
    amount_error.add_field(name="There's nothing there.",
                           value='You forgot to actually say *how* much to pay!')

    self_register_error = discord.Embed(color=0xD70040)
    self_register_error.add_field(name='Oh, you ARE new!',
                                  value="I don't see you in the database :(\nIt's okay, just use `!bal`")

    lack_nugs_error = discord.Embed(color=0xD70040)
    lack_nugs_error.add_field(name='Broke boiii :grimacing:',
                              value='You do not have enough nugs!')

    negative_nugs_error = discord.Embed(color=0xD70040)
    negative_nugs_error.add_field(name='Poops...',
                                  value='>You tried to pay a negative amount.\n>It did not work.\n>You feel stupid.')

    channel_error = discord.Embed(color=0xD70040)
    channel_error.add_field(name='Something aint right!',
                            value='Use this command in <#700293298652315648> please!')

    balance_error = discord.Embed(color=0xD70040)
    balance_error.add_field(name='I know whats wrong!',
                            value="Yeah. It seems like you don't have a kingdom role!")


class Treasury:
    store_lack_nugs_error = discord.Embed(color=0xD70040)
    store_lack_nugs_error.add_field(name=f'Could not store in the Kingdom Treasury!',
                                    value='Reason: You do not have enough nugs!')

    take_lack_nugs_error = discord.Embed(color=0xD70040)
    take_lack_nugs_error.add_field(name=f'Could not take from the Kingdom Treasury!',
                                   value='Reason: There is too little nugs in there!')

    negative_nugs_error = discord.Embed(color=0xD70040)
    negative_nugs_error.add_field(name='Unsuccessful!',
                                  value='Reason: You can not take a negative amount!')

    ruler_error = discord.Embed(color=0xD70040)
    ruler_error.add_field(name=f'Could not access the Treasury!',
                          value='Reason: You are not a Ruler!')


class Shop:
    ticket_buy_error = discord.Embed(color=0xD70040)
    ticket_buy_error.add_field(name=f'Not today buddy...',
                               value="I'm really sorry, but tickets can only be bought from the 19th till the 25th!")


class Leaderboard:
    page_error = discord.Embed(color=0xD70040)
    page_error.add_field(name="Not so fast!",
                         value="You're trying to get to a page that doesn't exist!")

    month_syntax_error = discord.Embed(color=0xD70040)
    month_syntax_error.add_field(name="Oh",
                                 value="This command is **!leaderboard activity <month> <page>**, means you need to "
                                       "write the month first and then flip the pages!")
