import discord


class Activity:
    connect_error = discord.Embed(color=0xD70040)
    connect_error.add_field(name="<:_no:921840417362804777> Aww... Shucks",
                            value="I don't recall you connecting actually...")


class Pay:
    self_error = discord.Embed(color=0xD70040)
    self_error.add_field(name='<:_no:921840417362804777> Poops...',
                         value='>You tried to pay yourself.\n>It did not work.\n>You feel stupid.')

    amount_error = discord.Embed(color=0xD70040)
    amount_error.add_field(name="<:_no:921840417362804777> There's nothing there.",
                           value='You forgot to actually say *how* much to pay!')

    self_register_error = discord.Embed(color=0xD70040)
    self_register_error.add_field(name='<:_no:921840417362804777> Oh, you ARE new!',
                                  value="I don't see you in the database :(\nIt's okay, just use `!bal`")

    lack_nugs_error = discord.Embed(color=0xD70040)
    lack_nugs_error.add_field(name='<:_no:921840417362804777> Broke boiii :grimacing:',
                              value='You do not have enough nugs!')

    negative_nugs_error = discord.Embed(color=0xD70040)
    negative_nugs_error.add_field(name='<:_no:921840417362804777> Poops...',
                                  value='>You tried to pay a negative amount.\n>It did not work.\n>You feel stupid.')

    channel_error = discord.Embed(color=0xD70040)
    channel_error.add_field(name='<:_no:921840417362804777> Something aint right!',
                            value='Use this command in <#700293298652315648> please!')

    balance_error = discord.Embed(color=0xD70040)
    balance_error.add_field(name='<:_no:921840417362804777> I know whats wrong!',
                            value="Yeah. It seems like you don't have a kingdom role!")


class Treasury:
    store_lack_nugs_error = discord.Embed(color=0xD70040)
    store_lack_nugs_error.add_field(name=f'<:_no:921840417362804777> Could not store in the Kingdom Treasury!',
                                    value='Reason: You do not have enough nugs!')

    take_lack_nugs_error = discord.Embed(color=0xD70040)
    take_lack_nugs_error.add_field(name=f'<:_no:921840417362804777> Could not take from the Kingdom Treasury!',
                                   value='Reason: There is too little nugs in there!')

    negative_nugs_error = discord.Embed(color=0xD70040)
    negative_nugs_error.add_field(name='<:_no:921840417362804777> Unsuccessful!',
                                  value='Reason: You can not take a negative amount!')

    ruler_error = discord.Embed(color=0xD70040)
    ruler_error.add_field(name=f'<:_no:921840417362804777> Could not access the Treasury!',
                          value='Reason: You are not a Ruler!')


class Shop:
    item_error = discord.Embed(color=0xD70040)
    item_error.add_field(name=f'<:_no:921840417362804777> Hey...',
                         value="This item doesn't exist! To see what items DO exist, use `!store`")

    faulty_ticket_error = discord.Embed(color=0xD70040)
    faulty_ticket_error.add_field(name="<:_no:921840417362804777> Oh No!",
                                  value="You try to scratch the ticket, and realise they sold you a fake!")

    empty_inventory_error = discord.Embed(color=0xD70040)
    empty_inventory_error.add_field(name="<:_no:921840417362804777> Cheeky.",
                                    value="You tried redeeming something that you don't even own!")


class Leaderboard:
    page_error = discord.Embed(color=0xD70040)
    page_error.add_field(name="<:_no:921840417362804777> Not so fast!",
                         value="You're trying to get to a page that doesn't exist!")

    month_syntax_error = discord.Embed(color=0xD70040)
    month_syntax_error.add_field(name="<:_no:921840417362804777> Oh",
                                 value="This command is **!leaderboard activity <month> <page>**, means you need to "
                                       "write the month first and then flip the pages!")
