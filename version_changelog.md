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
  * Stores all events, such as connect, disconnect, adjust
* Updated `functions.py` to store other functions, such as getting leaderboard info,
and other non-ThornyUser affiliated things and removed un-used functions
* Added a new `/events` command, which fetches all current scheduled events
* Added new updated responses, now stored in `config.json`

### Database Changes

* Added `redeemable` (boolean, default True) to `thorny.item_type`