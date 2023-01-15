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

        self.web3 = Web3(Web3.HTTPProvider(self.config.get('MAIN', 'NODE')))

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
        if balanceBNB < self.config.get('MIN_AMOUNT_BNB'):
            logging.fatal(f'Insufficient BNB for GAS, Balance: {balanceBNB:,.3f} BNB')
            return
        else:
            claims_available = self.faucetContract.functions.claimsAvailable(address).call() / 1e18
            deposit_amount = self.faucetContract.functions.userInfoTotals(address).call()[1] / 1e18
            deposit_percent = deposit_amount / 100

            min_avalible = self.config.get(f'WALLET-{wallet_number}', 'MIN_HYDRATE_AMOUNT')
        if self.config.get(f'WALLET-{wallet_number}', 'MIN_HYDRATE_MODE') == True:
            if min_avalible > claims_available:
                # Select either roll or claim based on current_ratio
                action = self.faucetContract.functions.roll if current_ratio % (hydrate + claim) < hydrate else self.faucetContract.functions.claim
                try:
                    tx = action().buildTransaction({
                        'nonce': self.web3.eth.get_transaction_count(address), 
                        'gas': self.config.get('MAIN', 'GAS'), 
                        'gasPrice': self.web3.toWei(self.config.get('MAIN', 'GWEI'),'gwei'),
                    })
                    if action == self.faucetContract.functions.roll:
                        logging.info(f'[{name}] Successfully HYDRATED {claims_available:,.2f} DRiP (TXN: xx)')
                    else:
                        logging.info(f'[{name}] Successfully CLAIMED {claims_available:,.2f} DRiP (TXN: xx)')
                    current_ratio += 1
                    if current_ratio >= hydrate + claim:
                        current_ratio = 0
                    self.config.set(f'WALLET-{wallet_number}', 'CURRENT_RATIO', current_ratio)

                except ValueError as e:
                    logging.error(f'[MHM] Failed to build transaction: {e}')
                    return

            else:
                logging.info(f'The amount of avalible drip has not hit the minimum amomunt, {min_avalible - claims_available:,.2f} drip left to go. Will try again later.')
                return

        # If minimum hydrate mode is not enabled, or minimum amount of drip has been reached
        elif claims_available > deposit_percent:
            # Select either roll or claim based on current_ratio
            action = self.faucetContract.functions.roll if current_ratio % (hydrate + claim) < hydrate else self.faucetContract.functions.claim
            try:
                tx = action().buildTransaction({
                    'nonce': self.web3.eth.get_transaction_count(address), 
                    'gas': self.config.get('MAIN', 'GAS'), 
                    'gasPrice': self.web3.toWei(self.config.get('MAIN', 'GWEI'),'gwei'),
                })
                if action == self.faucetContract.functions.roll:
                    logging.info(f'[{name}] Successfully HYDRATED {claims_available:,.2f} DRiP (TXN: xx)')
                else:
                    logging.info(f'[{name}] Successfully CLAIMED {claims_available:,.2f} DRiP (TXN: xx)')
                current_ratio += 1
                if current_ratio >= hydrate + claim:
                    current_ratio = 0
                self.config.set(f'WALLET-{wallet_number}', 'CURRENT_RATIO', current_ratio)

            except ValueError as e:
                logging.error(f'[{name}] Failed to build transaction: {e}')
                return
            
            signedTX = self.web3.eth.account.sign_transaction(tx, private_key)
        try:
            self.web3.eth.send_raw_transaction(signedTX.rawTransaction)
        except ValueError as e:
            logging.error(f'Failed to send transaction: {e}')