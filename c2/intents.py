##list of intents to create for the c2 system.
#
#close system
#close vm system
#open vm
#run update
#start vnc on certain servers based on config file. 
#
import discord
import os
from discord.ext import commands,tasks
import c2
import logging



DISCORD_TOKEN = os.getenv("discord_token_Eris")
intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot=commands.Bot(command_prefix="$", intents=intents)

def start_bot():
    return bot.start(DISCORD_TOKEN)

@bot.command(name="start_vm", help="tells the bot to start a VM based on the ID")
async def start_vm(ctx, vmid):
    try:
        if await Check_whiteList(ctx):
            server = ctx.message.guild
            async with ctx.typing():
                vmData = await c2.prox_instances.get_status_name(vmid)
            await ctx.send("starting vm " + str(vmid) + " name: " + str(vmData[0]) +" status: "+ str(vmData[1]))
            await c2.prox_instances.start_vm(vmid)
            async with ctx.typing():
                await c2.prox_instances.wait_till_running(vmid)
            await ctx.send("VM " + str(vmid) + " is now running " + ctx.author.display_name)
            logging.info('VM '+ str(vmid) + ' was started by ' + str(ctx.author.display_name))
    except:
        await ctx.send("vm could not be started")
        logging.error('vm could not be started ' + str(vmid))

@bot.command(name="Remote_management", help="tells the bot to start a VM based on the ID")
async def enable_remoteControl(ctx, vmid):
    try:
        if await Check_whiteList(ctx):
            server = ctx.message.guild
            async with ctx.typing():
                vmData = await c2.prox_instances.get_status_name(vmid)
            await ctx.send("Starting remote vnc on: " + str(vmid) + " name: " + str(vmData[0]) +" status: "+ str(vmData[1]))
            if vmData[1] == "stopped":
                await ctx.send("VM offline - startng vm")
                c2.prox_instances.start_vm(vmid)
                async with ctx.typing():
                    await c2.prox_instances.wait_till_running(vmid)
                    await ctx.send("VM " + str(vmid) + " is now running")

        ########## more functionality needed. and requires ansible more than likely
    except:
        await ctx.send("could not start remote vnc")
        logging.error('vm + vnc could not be started ' + str(vmid))


@bot.command(name="stop_VM", help="tells the bot to stop a VM based on the ID")
async def stop_vm(ctx, vmid):
    try:
        if await Check_whiteList(ctx):
            server = ctx.message.guild
            async with ctx.typing():
                vmData = await c2.prox_instances.get_status_name(vmid)
            await ctx.send("stopping vm " + str(vmid) + " name: " + str(vmData[0]) +" status: "+ str(vmData[1]))
            await c2.prox_instances.stop_vm(vmid)
            async with ctx.typing():
                await c2.prox_instances.wait_till_Stopped(vmid)
            await ctx.send("VM " + str(vmid) + " has now been stopped")
            logging.info(str('vm ' + str(vmid))+' was stopped  by ' + str(ctx.author.display_name))
    except:
        await ctx.send("vm could not be stopped")
        logging.error('vm could not be stopped ' + str(vmid) + " by " + ctx.author.display_name)

@bot.command(name="shutdown_vm", help="tells the bot to stop a VM based on the ID")
async def shutdown_vm(ctx, vmid):
    try:
        if await Check_whiteList(ctx):
            server = ctx.message.guild
            async with ctx.typing():
                vmData = await c2.prox_instances.get_status_name(vmid)
            await ctx.send("shutting down vm " + str(vmid) + " name: " + str(vmData[0]) +" status: "+ str(vmData[1]))
            await c2.prox_instances.shutdown_vm(vmid)
            async with ctx.typing():
                await c2.prox_instances.wait_till_Stopped(vmid)
            await ctx.send("VM " + str(vmid) + ' has now been shut down by ' + str(ctx.author.display_name))
            logging.info('vm was shutdown ' + str(vmid) + " by " + ctx.author.display_name)
    except:
        await ctx.send("vm could not be shutdown")
        logging.error('vm could not be shutdown ' + str(vmid) + " by "+ ctx.author.display_name)


@bot.command(name="vm_status", help="tells the bot to stop a VM based on the ID")
async def vm_status(ctx):
    statuslist = c2.prox_instances.get_vm_status()
    for vmStatus in statuslist:
        await ctx.send(vmStatus)

async def Check_whiteList(ctx):
    logging.info("whitelist Check: "+ ctx.author.display_name)
    if ctx.author.display_name in c2.prox_instances.WHITELIST:
        #print("yo do the thing")
        await ctx.send("Access Granted.")
        return True
    else: 
        await ctx.send("Im sorry, I cant let you do that.")
        return False