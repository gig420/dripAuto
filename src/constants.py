'''
    constants.py
    -
    - This file is for varibles used throught the bot.
    -
'''

import os

NAME = "GiggleLab"
DESCRIPTION = "Auto Hydrate - drip.community"
VERSION = "1.0 - Public"

FAUCET_ADDRESS = "0xFFE811714ab35360b67eE195acE7C10D93f89D8C"
RESERVOIR_ADDRESS = "0xB486857fac4254A7ffb3B1955EE0C0A2B2ca75AB"
DRIP_ADDRESS = "0x20f663CEa80FaCE82ACDFA3aAE6862d246cE0333"
TAXPOOL_ADDRESS = "0xBFF8a1F9B5165B787a00659216D7313354D25472"
FOUNTAIN_ADDRESS = "0x4Fe59AdcF621489cED2D674978132a54d432653A"
BR34P_ADDRESS = "0xa86d305A36cDB815af991834B46aD3d7FbB38523"
PCS_ADDRESS = "0xa0feB3c81A36E885B6608DF7f0ff69dB97491b58"
PRICE_CONTRACT = "0x64a4c814311bd6acdc589aa907b19920404b9a0d"

DIR_SRC = os.path.basename(os.path.dirname(__file__))
DIR_TEM = "templates"
DIR_PLG = "plugins"
DIR_RES = "res"
DIR_CFG = "cfg"
DIR_LOG = "log"
DIR_DAT = "dat"
DIR_TMP = "tmp"
DIR_DIR = "src"

FILE_DAT = "global.db"
FILE_CFG = "config.toml"
FILE_TMPCFG = "config_template.toml"
FILE_LOG = f"hydrate.log"

ASCII_ART = "logo.md"
