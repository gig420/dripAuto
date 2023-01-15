Auto Hydrater for the Drip.community

The Auto Hydrater script is designed for the Drip.community to allow users to automatically Hydrate or Claim their rewards every time 1% is generated. It is easy to set up and the contracts are located in the constants.py file.

One of the main concerns when building this script was the storage of private keys. The script starts by prompting the user to enter a password, which is used to encrypt the private keys stored in the config.toml file. Without the password, the script will not work. If you have a better way to store the private keys, please let us know.

The configuration file, config.toml, is simple to use. You do not need to edit the [MAIN] section, as it will be filled in automatically. The only thing you might want to change is the NODE, GAS, AND GWEI section - if you want to change node settings - please understand what you are doing.

To add more wallets, just copy and paste the WALLET-{NUMBER} section, replacing the number with the next one in line.

The RATIO section allows you to set the ratio of Hydrate to Claim for the week. The days must add up to a total of 7 days. For example, HYDRATE = 4 and CLAIM = 3 would mean that 4 days out of the week are for Hydrating and 3 days are for Claiming. If you want to fully Hydrate, set HYDRATE = 7 and CLAIM = 0. Leave the CURRENT_RATIO value alone.

The MIN_HYDRATE_MODE should be set to True or False. This will hydrate every MIN_HYDRATE_AMOUNT generated. If set to false it will revert to 1% Mode.

The REFRESH_INTERVAL value determines how often the script checks for 1% that is ready to be Hydrated. It is set in seconds, so a value of 3600 means the script will check every hour.

To use the script, run "python -m src -log 20" in the command line. To encrypt your private keys, run "python -m src -encrypt". You can also use the "run.bat" or "encrypt.bat" files.

You may need to run 'pip install -r requirements.txt' to install the necessary packages.

Please note that this script involves advanced crypto and anyone not comfortable with it should probably just do it manually. Use this at your own risk and be careful when it comes to automation and your private keys.

This script is open source and we would like to thank the few people who helped us with a few issues and reviewing our work. Future updates will include a couple of other features and we will be working on Animal farm shortly.

If you would like to support the development of this script, you can buy me a coffee at my Drip wallet address: 0xD64D99F41c3D5fBCE4207856F93F31950Ae74AAb.

For more information on Drip, check out the RESERVOIR.