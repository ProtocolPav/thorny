### Version Info
Version: v1.7.1  
Nickname: Revival 

### Changelog

* Added the ThornyUserSlot and ThornyUserStrike classes to `dbclass.py`
* Renamed `gateway.py` to `information.py`
* Added `dbcommit.py`, which will be used to commit transactions into the database
  * The `commit` function is the main one to be used, at the end of every command which uses ThornyUser
* Renamed files:
  * `gateway.py` -> `information.py` Reflects the changes in commands
* Separated the ThornyFactory class from dbclass
* Created new ThornyEvent class, and `dbevent.py` file
  * Stores all events, such as connect, disconnect, adjust, etc.
* Updated `functions.py` to store other functions, such as getting leaderboard info,
and other non-ThornyUser affiliated things and removed un-used functions
* Added a new `/events` command, which fetches all current scheduled events
* Added new updated responses, now stored in `config.json`
* Fixed a bug where your rank would not show up on leaderboards
*

### New Pooling Updates
* `bank.py` has been fully updated to support the new Pooling Method
* `inventory.py` has been fully updated
* `profile.py` has been fully updated

### Database Changes

* Added `redeemable` (boolean, default True) to `thorny.item_type`
* Added a new table `guilds` where all guild data is stored. 
But this needs working on and will be introduced fully in **v1.7.2**
* 