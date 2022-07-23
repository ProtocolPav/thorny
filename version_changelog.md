### Version Info
Version: v1.8 

### Changelog - Class Update
* Changed Errors
* Added Birthday Events
* Fixed bug where you would not get a level up message upon leveling up through disconnecting
* Separated item redeeming functions in their own file, NEEDS WORK
* Fixed bug where online shows other servers
* Removed /profile sections
* Fixed bug where you could not edit role
* Added /birthday remove
* MAJOR FEATURE: /setup command
* Made the /level command appear differently for mobile users
* Removed /kingdoms and associated commands
* Disabled /setup for v1.7.4

### Future Plans
* Separate dbclass into a directory with multiple files
* Create init files (?) where i wouldnt need to import things all the time
* Improve upon redeemingfuncs file
* Remove kingdom checker
* Delete kingdom database tables

### Database Changes
* Add new table (using SQL script) called guilds. It stores: 
  * Guild IDs
  * Join Channel ID
  * General Channel ID
  * Gulag channel ID
  * Log channel ID
~~* Add new column to `user` table: `xuid`
  * This will be the main way that I communicate to the Minecraft Server, using xuids~~

### Project dependencies
None