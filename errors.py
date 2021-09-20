import discord


class Pay:
    self_error = discord.Embed(color=0x900C3F)
    self_error.add_field(name='Poops...',
                         value='>You tried to pay yourself.\n>It did not work.\n>You feel stupid.')

    amount_error = discord.Embed(color=0x900C3F)
    amount_error.add_field(name="There's... nothing there.",
                           value='You forgot to actually say *how* much to pay!')

    self_register_error = discord.Embed(color=0x900C3F)
    self_register_error.add_field(name='Oh, you ARE new!',
                                  value="I don't see you in the database :(\nIt's okay, just use `!bal`")

    lack_nugs_error = discord.Embed(color=0x900C3F)
    lack_nugs_error.add_field(name='Broke boiii :grimacing:',
                              value='You do not have enough nugs!')

    negative_nugs_error = discord.Embed(color=0x900C3F)
    negative_nugs_error.add_field(name='Poops...',
                                  value='>You tried to pay a negative amount.\n>It did not work.\n>You feel stupid.')

    channel_error = discord.Embed(color=0x900C3F)
    channel_error.add_field(name='Something aint right!',
                            value='Use this command in <#700293298652315648> please!')

    balance_error = discord.Embed(color=0x900C3F)
    balance_error.add_field(name='I know whats wrong!',
                            value="Yeah. It seems like you don't have a kingdom role!")


class Treasury:
    store_lack_nugs_error = discord.Embed(color=0x900C3F)
    store_lack_nugs_error.add_field(name=f'Could not store in the Kingdom Treasury!',
                                    value='Reason: You do not have enough nugs!')

    take_lack_nugs_error = discord.Embed(color=0x900C3F)
    take_lack_nugs_error.add_field(name=f'Could not take from the Kingdom Treasury!',
                                   value='Reason: There is too little nugs in there!')

    negative_nugs_error = discord.Embed(color=0x900C3F)
    negative_nugs_error.add_field(name='Unsuccessful!',
                                  value='Reason: You can not take a negative amount!')

    ruler_error = discord.Embed(color=0x900C3F)
    ruler_error.add_field(name=f'Could not access the Treasury!',
                          value='Reason: You are not a Ruler!')

class Shop:
    ticket_buy_error = discord.Embed(color=0x900C3F)
    ticket_buy_error.add_field(name=f'Not today buddy...',
                               value="I'm really sorry, but tickets can only be bought from the 19th till the 25th!")
