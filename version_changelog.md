### Version Info
Version: v1.8.1

### Changelog - Profile Update
* Separated dbclass into the db package
* Created the uikit package
* The all-new profile is now here:
  * Multiple pages, and an edit button
  * When editing, a modal text pops up
  * 

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