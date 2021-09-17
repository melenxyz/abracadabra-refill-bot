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

cauldrons = json.loads(open("Cauldrons.json", 'r').read()) #Loads Cauldrons.json as a nested dic
settings= json.loads(open("Settings.json", 'r').read()) #Loads Chains Info

webhook = DiscordWebhook(url=webhook_url) #Discord WebHook URL

for chain in settings.keys(): #Go though each chain
    w3 = Web3(Web3.HTTPProvider(settings[chain]['RPC'])) #Network RPC
    bb_address = w3.toChecksumAddress(settings[chain]['bentobox']) #BentoBox Contract Address
    MIM_contract_address=w3.toChecksumAddress(settings[chain]['MIM']) #MIM Contract Address
    bb_ABI = json.load(open('BentoBoxV1.json', 'r')) #BentoBox ABI load, from BentoBoxV1.json
    bentobox = w3.eth.contract(address=bb_address, abi=bb_ABI) 

    def  getMIMAmount(mim_address, cauldron):
        mim_amount=bentobox.functions.balanceOf(mim_address, cauldron).call()
        mim_amount=w3.fromWei(mim_amount, 'ether')
        return mim_amount


    def sendMessage(tokens, amount):
        amount=int(amount)
        amount=(f"{amount:,}")
        embed=DiscordEmbed(title=cauldrons[tokens]['title'], url=cauldrons[tokens]['website'], color=settings[chain]['color'])
        embed.set_thumbnail(url=cauldrons[tokens]['logo'])
        embed.add_embed_field(name="%s Market Replenish" %tokens, value="%s MIMs are available for minting on %s! <:MIM:888155951016857662>" %(amount,settings[chain]['message_name']), inline=False)
        embed.set_footer(text=chain)
        webhook.add_embed(embed)
        response = webhook.execute(remove_embeds=True)
        sleep(5)

    for tokens in cauldrons.keys(): #Go through each Cauldron entry
        if cauldrons[tokens]['chain'] == chain: #Check wether the Cauldron entry is on the chain we are working with 
            amount=getMIMAmount(MIM_contract_address, w3.toChecksumAddress(cauldrons[tokens]['address'])) #Gets MIM available for the cauldron
            print("%s :" %tokens)
            print("Old amount : ", cauldrons[tokens]['previous_amount'])
            
            if amount - Decimal(cauldrons[tokens]['previous_amount']) > settings[chain]['threshold']: #Compare amount with previous amount and check if above threshold, defined per chain
                sendMessage(tokens, amount) #Send discord msg
            
            cauldrons[tokens]['previous_amount']=str(amount) #Store amount as Previous_amount
            print("New amount : ", cauldrons[tokens]['previous_amount'])
            print("-----")

    
    json.dump(cauldrons, open("Cauldrons.json", 'w'), indent=4, sort_keys=True)