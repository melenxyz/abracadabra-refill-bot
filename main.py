import os
import json
from decimal import Decimal
from time import sleep
from web3 import Web3
from eth_typing import abi
from web3.types import ABI
from dotenv import load_dotenv
from discord_webhook import DiscordWebhook, DiscordEmbed



load_dotenv() #Check Environment Variables in .env file
project_id = os.getenv('PROJECT_ID')
webhook_url= os.getenv('WEBHOOK')

webhook = DiscordWebhook(url=webhook_url) #Discord WebHook URL
w3 = Web3(Web3.HTTPProvider('https://rpc.ftm.tools/')) #Network RPC

bb_address = w3.toChecksumAddress("0x74A0BcA2eeEdf8883cb91E37e9ff49430f20a616") #BentoBox Contract Address
MIM_contract_address=w3.toChecksumAddress("0x82f0b8b456c1a451378467398982d4834b6829c1") #MIM Contract Address
bb_ABI = json.load(open('BentoBoxV1.json', 'r')) #BentoBox ABI load, from BentoBoxV1.json
bentobox = w3.eth.contract(address=bb_address, abi=bb_ABI) 

cauldrons = json.loads(open("Cauldrons.json", 'r').read()) #Loads Cauldrons.json as a nested dic

def  getMIMAmount(mim_address, cauldron):
    mim_amount=bentobox.functions.balanceOf(mim_address, cauldron).call()
    mim_amount=w3.fromWei(mim_amount, 'ether')
    return mim_amount


def sendMessage(tokens, amount):
    amount=int(amount)
    amount=(f"{amount:,}")
    embed=DiscordEmbed(title=cauldrons[tokens]['title'], url=cauldrons[tokens]['website'], color=0x1b96f0)
    embed.set_thumbnail(url=cauldrons[tokens]['logo'])
    embed.add_embed_field(name="%s Market Replenish" %tokens, value="%s MIMs are available for minting on Fantom Opera! <:MIM:888155951016857662>" %amount, inline=False)
    embed.set_footer(text="FANTOM OPERA")
    webhook.add_embed(embed)
    response = webhook.execute(remove_embeds=True)
    sleep(5)




for tokens in cauldrons.keys():
    amount=getMIMAmount(MIM_contract_address, w3.toChecksumAddress(cauldrons[tokens]['address']))
    print("%s :" %tokens)
    print("Old amount : ", cauldrons[tokens]['previous_amount'])
    
    if amount - Decimal(cauldrons[tokens]['previous_amount']) > 100000 and cauldrons[tokens]['monitored']==True: #test Balance increase
        sendMessage(tokens, amount) #Send discord msg
    
    cauldrons[tokens]['previous_amount']=str(amount)
    print("New amount : ", cauldrons[tokens]['previous_amount'])
    print("-----")

 
json.dump(cauldrons, open("Cauldrons.json", 'w'), indent=4, sort_keys=True)