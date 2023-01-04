Auto Hydrater for the Drip.community
This script is designed for the Drip.community to allow users to automatically Hydrate or Claim their rewards every time 1% is generated. It is easy to set up, and the contracts are located in the constants.py file.

One of the main concerns when building this script was the storage of private keys. When the script starts, it will ask you to enter a password. This password is important and should not be forgotten, as it is used to encrypt the private keys that are stored in the config.toml file. Without the password, the script will not work. If you have a better way to store the private keys, please let me know.

The configuration file, config.toml, is simple to use. You do not need to edit the [MAIN] section, as it will be filled in automatically.
Only thing you might want to change is the NODE, GAS AND GWEI section - if you want to change node settings - please understand what you are doing.

To add more wallets, just copy and paste the WALLET-{NUMBER} section, replacing the number with the next one in line.

The RATIO section allows you to set the ratio of Hydrate to Claim for the week. The days must add up to a total of 7 days. For example, HYDRATE = 4 and CLAIM = 3 would mean that 4 days out of the week are for Hydrating and 3 days are for Claiming. If you want to fully Hydrate, set HYDRATE = 7 and CLAIM = 0. Leave the CURRENT_RATIO value alone.

The REFRESH_INTERVAL value determines how often the script checks for 1% that is ready to be Hydrated. It is set in seconds, so a value of 3600 means the script will check every hour.

Usage:
python -m src -log 20

Encrypting keys: python -m src -encrypt
Encrypt your private keys, This will need to be run and used for every new wallet.

(can use run.bat or encrypt.bat)

-

You may need to run 'pip install -r requirements.txt' to install the correct packages to go with the script.

-

This is advanced crypto. Anyone not comfortable with it should probably just do it manually, Use this at your own risk. Please be careful when it comes to automation and even more careful when it comes to your Private Keys.
I have left this opensource and thanks to the few people who helped me with a few issues and reviewing my work. Much appreicated guys.

There will be following updates coming with a couple of other features. I will also be working on Animal farm shortly.
-
Fancy buying me a coffee? My Drip wallet: 0xD64D99F41c3D5fBCE4207856F93F31950Ae74AAb
Want to look more into drip? Check out the Resviour.
.