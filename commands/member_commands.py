# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot.init import bot
from bot.logger.init import logger

@bot.command()
async def ping(ctx):
    """
    Description
        Responds with the bot's current latency (ping) when issued the !ping command.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.

    Returns:
        None
    """
    
    logger.info("'ping' command was issued by {ctx.author}")
    
    # Calculate the latency (ping)
    try: latency = round(bot.latency * 1000)  # Convert to milliseconds
    
    # Log any Errors
    except Exception as e: logger.error(e)

    # Send the latency as a message
    await ctx.send(f'Pong! Latency is {latency} ms')
