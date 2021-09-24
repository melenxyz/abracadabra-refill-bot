from discord_webhook import DiscordWebhook, DiscordEmbed
import os
from dotenv import load_dotenv
from time import sleep

load_dotenv() #Check Environment Variables in .env file
webhook_url= os.getenv('WEBHOOK')

webhook = DiscordWebhook(url=webhook_url) #Discord WebHook URL

def sendMessage(tokens, amount, cauldrons, settings, chain):
    amount=int(amount)
    amount=(f"{amount:,}")
    embed=DiscordEmbed(title=cauldrons[tokens]['title'], url=cauldrons[tokens]['website'], color=settings[chain]['color'])
    embed.set_thumbnail(url=cauldrons[tokens]['logo'])
    embed.add_embed_field(name="%s Market Replenish" %tokens, value="%s MIMs are available for minting on %s! <:MIM:888155951016857662>" %(amount,settings[chain]['message_name']), inline=False)
    embed.set_footer(text=chain)
    webhook.add_embed(embed)
    response = webhook.execute(remove_embeds=True)
    print("discord sent!")
    sleep(5)