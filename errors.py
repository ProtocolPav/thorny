import discord


class UnexpectedError1(discord.ApplicationCommandError):
    """ Raised when something truly unexpected happens """
    def __init__(self, tb: str):
        self.error: discord.Embed = discord.Embed(color=0xD70040)
        self.traceback = tb

    def return_embed(self) -> discord.Embed:
        self.error.add_field(name="<:_no:921840417362804777> I have NEVER seen this before...",
                             value=f"This is something that I didn't expect to happen. Here's the issue: "
                                   f"{self.traceback}")
        self.error.set_footer(text=f"Error Reference: {self.__class__.__name__}")
        return self.error


class UnexpectedError2(discord.ApplicationCommandError):
    """ Raised when something unexpected happens """
    def __init__(self, tb: str):
        self.error: discord.Embed = discord.Embed(color=0xD70040)
        self.traceback = tb

    def return_embed(self) -> discord.Embed:
        self.error.add_field(name="<:_no:921840417362804777> Sorry for this...",
                             value="I had a bit of a glitch in my code. Here's the issue:\n"
                                   f"{self.traceback}")
        self.error.set_footer(text=f"Error Reference: {self.__class__.__name__}")
        return self.error


class ThornyError(discord.ApplicationCommandError):
    def __init__(self):
        self.error: discord.Embed = discord.Embed(color=0xD70040)

    def return_embed(self) -> discord.Embed:
        pass


class NotConnectedError(ThornyError):
    """ Raised when somebody tries disconnecting when they are not connected """

    def return_embed(self) -> discord.Embed:
        self.error.add_field(name="<:_no:921840417362804777> Oh, bother.",
                             value="Either you haven't connected, or someone's hacked me!")
        self.error.set_footer(text=f"Error Reference: {self.__class__.__name__}")
        return self.error


class AlreadyConnectedError(ThornyError):
    """ Raised when somebody tries connecting when they've already connected """

    def return_embed(self) -> discord.Embed:
        self.error.add_field(name="<:_no:921840417362804777> Not so fast!",
                             value="You're already connected. If you are really *that* keen on connecting, you gotta "
                                   "`/disconnect` first!")
        self.error.set_footer(text=f"Error Reference: {self.__class__.__name__}")
        return self.error


class SelfPaymentError(ThornyError):
    """ Raised when somebody attempts to pay themselves """

    def return_embed(self) -> discord.Embed:
        self.error.add_field(name="<:_no:921840417362804777> Lmao what a L0$3R!",
                             value="You **really** thought that you could... pay YOURSELF? Damn.")
        self.error.set_footer(text=f"Error Reference: {self.__class__.__name__}")
        return self.error


class BrokeError(ThornyError):
    """ Raised when somebody does not have enough funds in their balance for a transaction """

    def return_embed(self) -> discord.Embed:
        self.error.add_field(name="<:_no:921840417362804777> I don't know how to tell you this...",
                             value="You're broke. You can't pay, because you're too broke for that. "
                                   "Maybe try buying something you can afford?")
        self.error.set_footer(text=f"Error Reference: {self.__class__.__name__}")
        return self.error


class NegativeAmountError(ThornyError):
    """ Raised when somebody tries to enter a negative amount in places where they can't """

    def return_embed(self) -> discord.Embed:
        self.error.add_field(name="<:_no:921840417362804777> Okay, did you really think that would work?",
                             value="Seriously debating whether to publicly announce this to everyone. "
                                   "Of course you can't put a negative number there...")
        self.error.set_footer(text=f"Error Reference: {self.__class__.__name__}")
        return self.error


class StoreError(ThornyError):
    """ Raised when somebody tries storing money but is not in a kingdom """

    def return_embed(self) -> discord.Embed:
        self.error.add_field(name="<:_no:921840417362804777> Well, well, well...",
                             value="You tried donating to your kingdom... But you're not in one!")
        self.error.set_footer(text=f"Error Reference: {self.__class__.__name__}")
        return self.error


class ItemNotAvailableError(ThornyError):
    """ Raised when somebody tries buying / redeeming an item that does not exist or is not available """

    def return_embed(self) -> discord.Embed:
        self.error.add_field(name="<:_no:921840417362804777> This item seems funky.",
                             value="This item isn't available to purchase or redeem.")
        self.error.set_footer(text=f"Error Reference: {self.__class__.__name__}")
        return self.error


class FaultyTicketError(ThornyError):
    """ Raised only when the ticket redeeming chances happens """
    def return_embed(self) -> discord.Embed:
        self.error.add_field(name="<:_no:921840417362804777> Uh oh",
                             value="Seems like you were sold a fake ticket!")
        self.error.set_footer(text=f"Error Reference: {self.__class__.__name__}")
        return self.error


class MissingItemError(ThornyError):
    """ Raised when the item that is redeemed or removed does not exist"""
    def return_embed(self) -> discord.Embed:
        self.error.add_field(name="<:_no:921840417362804777> Uh oh",
                             value="This item does not exist in the user's inventory!")
        self.error.set_footer(text=f"Error Reference: {self.__class__.__name__}")
        return self.error


class DataTooLongError(ThornyError):
    """ Raised when the data entered is too long for the database to hold"""
    def __init__(self, length: int, database_length: int):
        super().__init__()
        self.length = length
        self.db_length = database_length

    def return_embed(self) -> discord.Embed:
        self.error.add_field(name="<:_no:921840417362804777> Welp. I guess shorten this",
                             value="I checked the database, whatever you just tried writing in is too long.\n"
                                   f"Your input's length: {self.length}\nDatabase max. length: {self.db_length}")
        self.error.set_footer(text=f"Error Reference: {self.__class__.__name__}")
        return self.error


class ItemMaxCountError(ThornyError):
    """ Raised when the item in question has reached its maximum count"""

    def __init__(self, max_count: int = 0):
        super().__init__()
        self.max_count = max_count

    def return_embed(self) -> discord.Embed:
        self.error.add_field(name="<:_no:921840417362804777> Too much man... Too. Much.",
                             value="You can't have this much stuff!\n"
                                   f"You can only have maximum {self.max_count} of this item.")
        self.error.set_footer(text=f"Error Reference: {self.__class__.__name__}")
        return self.error


class IncorrectStrikeID(ThornyError):
    """Raised when a wrong strike ID was entered"""

    def __init__(self):
        super().__init__()

    def return_embed(self) -> discord.Embed:
        self.error.add_field(name="<:_no:921840417362804777> Darn",
                             value="Seems to me like you entered a Strike ID that doesn't exist!")
        self.error.set_footer(text=f"Error Reference: {self.__class__.__name__}")
        return self.error


class AccessDenied(ThornyError):
    """Raised when command is disabled"""

    def __init__(self):
        super().__init__()

    def return_embed(self) -> discord.Embed:
        self.error.add_field(name="<:_no:921840417362804777> Darn",
                             value="This command has been disabled for this server!")
        self.error.set_footer(text=f"Error Reference: {self.__class__.__name__}")
        return self.error


class RedeemError(ThornyError):
    """Raised when a redeemable does not have a redemption function (This would be rare)"""

    def __init__(self):
        super().__init__()

    def return_embed(self) -> discord.Embed:
        self.error.add_field(name="<:_no:921840417362804777> Darn",
                             value="You've redeemed the item, but it does nothing!")
        self.error.set_footer(text=f"Error Reference: {self.__class__.__name__}")
        return self.error
