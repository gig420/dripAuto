'''
  - drip.py

'''

import os
import json
import logging
import threading
import src.constants as con
import src.utils as util

from src.config import Config
from web3 import Web3
from cryptography.fernet import Fernet

class Drip:
    def __init__(self, decrypted_password):
        self.config = Config()

        threading.current_thread().name = "Drip"

        self.bsc = "https://bsc-dataseed.binance.org/"
        self.web3 = Web3(Web3.HTTPProvider(self.bsc))

        with open(os.path.join(con.DIR_RES, 'faucet.json')) as f:
            self.faucetAbi = json.load(f)
        with open(os.path.join(con.DIR_RES, 'reservoir.json')) as f:
            self.reservoirAbi = json.load(f)
        with open(os.path.join(con.DIR_RES, 'drip.json')) as f:
            self.dripAbi = json.load(f)
        with open(os.path.join(con.DIR_RES, 'drippricereader.json')) as f:
            self.priceAbi = json.load(f)

        self.faucetContract = self.web3.eth.contract(address=con.FAUCET_ADDRESS, abi=self.faucetAbi)
        self.dripContract = self.web3.eth.contract(address=con.DRIP_ADDRESS, abi=self.dripAbi)
        self.reservoirContract = self.web3.eth.contract(address=con.RESERVOIR_ADDRESS, abi=self.reservoirAbi)
        self.priceContract = self.web3.eth.contract(address=self.web3.toChecksumAddress(con.PRICE_CONTRACT), abi=self.priceAbi)
        
        self.loadWallets(decrypted_password)

    def loadWallets(self, decrypted_password):

        logging.info('Loading wallets...')

        wallet_number = 1
        while True:
            wallet_data = self.config.get(f'WALLET-{wallet_number}')
            if wallet_data is None:
                break
            name = wallet_data['NAME']
            private_key = Fernet(decrypted_password).decrypt(wallet_data['ENCRYPTED_PK'].encode()).decode()
            address = wallet_data['WALLET_ADDRESS']
            current_ratio = wallet_data['CURRENT_RATIO']
            hydrate = wallet_data['HYDRATE']
            claim = wallet_data['CLAIM']
            refresh_interval = wallet_data['REFRESH_INTERVAL']

            util.repeater(refresh_interval, self.checkWallet, wallet_number, name, private_key, address, hydrate, claim, current_ratio)
            
            self.checkWallet(wallet_number, name, private_key, address, hydrate, claim, current_ratio)
            
            wallet_number += 1

        logging.info(f'{wallet_number - 1} wallets loaded successful')
        return

    def checkWallet(self, wallet_number, name, private_key, address, hydrate, claim, current_ratio):
        threading.current_thread().name = name
        balanceBNB = Web3.fromWei(self.web3.eth.getBalance(address), 'ether')
        if balanceBNB < 0.003:
            logging.fatal(f'Insufficient BNB for GAS, Balance: {balanceBNB:,.3f} BNB')
            return
        else:
            claims_available = self.faucetContract.functions.claimsAvailable(address).call() / 1e18
            deposit_amount = self.faucetContract.functions.userInfoTotals(address).call()[1] / 1e18
            deposit_percent = deposit_amount / 100
            
            if claims_available > deposit_percent:
                if current_ratio % (hydrate + claim) < hydrate:
                    try:
                        tx = self.faucetContract.functions.roll().buildTransaction({'nonce': self.web3.eth.get_transaction_count(address), 'gas': 500000, 'gasPrice': self.web3.toWei('5','gwei'),})
                        logging.info(f'Successfully HYDRATED {claims_available:,.2f} DRiP (TXN: xx)')
                        current_ratio += 1
                        if current_ratio >= hydrate + claim:
                            current_ratio = 0
                        self.config.set(f'WALLET-{wallet_number}', 'CURRENT_RATIO', current_ratio)

                    except ValueError as e:
                        logging.error(f'Failed to build roll transaction: {e}')
                        return

                else:
                    try:
                        tx = self.faucetContract.functions.claim().buildTransaction({'nonce': self.web3.eth.get_transaction_count(address), 'gas': 500000, 'gasPrice': self.web3.toWei('5','gwei'),})
                        logging.info(f'[{name}] Successfully HYDRATED {claims_available:,.2f} DRiP (TXN: xx)')
                        current_ratio += 1
                        if current_ratio >= hydrate + claim:
                            current_ratio = 0
                        self.config.set(f'WALLET-{wallet_number}', 'CURRENT_RATIO', current_ratio)

                    except ValueError as e:

                        logging.error(f'Failed to build claim transaction: {e}')
                        return
                signedTX = self.web3.eth.account.sign_transaction(tx, private_key)
                try:
                    self.web3.eth.send_raw_transaction(signedTX.rawTransaction)
                except ValueError as e:
                    logging.error(f'Failed to send transaction: {e}')
            else:
                logging.info(f'Avalible drip has not hit 1%, {deposit_percent - claims_available:,.2f} drip left to go. Will try again later.')
                return

