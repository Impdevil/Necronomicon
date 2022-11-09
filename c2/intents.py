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
DISCORD_TOKEN = os.getenv("discord_token_Eris")
intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot=commands.Bot(command_prefix="$", intents=intents)

def start_bot():
    return bot.start(DISCORD_TOKEN)

@bot.command(name="start_vm", help="tells the bot to start a VM based on the ID")
async def start_vm(ctx, vmid):
    try:
        server = ctx.message.guild
        async with ctx.typing():
            vmData = await c2.prox_instances.get_status_name(vmid)
        await ctx.send("starting vm " + str(vmid) + " name: " + str(vmData[0]) +" status: "+ str(vmData[1]))
        await c2.prox_instances.start_vm(vmid)
        async with ctx.typing():
            await c2.prox_instances.wait_till_running(vmid)
        await ctx.send("VM " + str(vmid) + " is now running")
    except:
        await ctx.send("vm could not be started")

@bot.command(name="stop_VM", help="tells the bot to stop a VM based on the ID")
async def stop_vm(ctx, vmid):
    try:
        server = ctx.message.guild
        async with ctx.typing():
            vmData = await c2.prox_instances.get_status_name(vmid)
        await ctx.send("stopping vm " + str(vmid) + " name: " + str(vmData[0]) +" status: "+ str(vmData[1]))
        await c2.prox_instances.stop_vm(vmid)
        async with ctx.typing():
            await c2.prox_instances.wait_till_Stopped(vmid)
        await ctx.send("VM " + str(vmid) + " has now been stopped")
    except:
        await ctx.send("vm could not be stopped")

@bot.command(name="shutdown_vm", help="tells the bot to stop a VM based on the ID")
async def stop_vm(ctx, vmid):
    try:
        server = ctx.message.guild
        async with ctx.typing():
            vmData = await c2.prox_instances.get_status_name(vmid)
        await ctx.send("shutting down vm " + str(vmid) + " name: " + str(vmData[0]) +" status: "+ str(vmData[1]))
        await c2.prox_instances.shutdown_vm(vmid)
        async with ctx.typing():
            await c2.prox_instances.wait_till_Stopped(vmid)
        await ctx.send("VM " + str(vmid) + " has now been shut down")
    except:
        await ctx.send("vm could not be shutdown")
