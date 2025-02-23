# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot import bot
from logger import logger

# Import Other Necessary Libraries
import aiohttp
import requests
import time
import math

# Import Necessary Local Files
from config import config

@bot.command()
async def metar(ctx, icao_code: str):
    """
    Command to fetch and display METAR information for a specified airport ICAO code.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        icao_code (str): The ICAO code of the airport for which METAR information is requested.

    Returns:
        None
    """
    try:
        # Perform Input Validation on the ICAO Airport Code
        if not icao_code.isalnum() or not (len(icao_code) == 4):
            await ctx.send("Invalid ICAO code format. It must 4 alphanumeric characters.")
            return

        # Get the METAR data from the API
        metar_data = await get_metar_info(icao_code)

        # Send Error Message and Exit Function if No Information was Retrieved
        if metar_data is None:
            await ctx.send(f"Unable to retrieve METAR info for {icao_code}")
            return

        # Create an embed
        embed = discord.Embed(
            title=f"METAR for {metar_data['icaoId']}",
            description=f"{metar_data['name']}",
            color=discord.Color.blue()
        )

        # Add Other Fields
        embed.add_field(name="Latitude", value=f"{metar_data['lat']}")
        embed.add_field(name="Longitude", value=f"{metar_data['lon']}")
        embed.add_field(name="Altitude", value=f"{metar_data['elev']}")
        embed.add_field(name="Temperature (°C)", value=f"{metar_data['temp']}°C")
        embed.add_field(name="Dew Point (°C)", value=f"{metar_data['dewp']}°C")
        embed.add_field(name="Wind Direction", value=f"{metar_data['wdir']}°")
        embed.add_field(name="Wind Speed (KT)", value=f"{metar_data['wspd']} KT")
        embed.add_field(name="Visibility", value=f"{metar_data['visib']}")
        embed.add_field(name="Altimeter (mb)", value=f"{metar_data['altim']} mb")
        embed.add_field(name="Sea Level Pressure (mb)", value=f"{metar_data['slp']} mb")
        embed.add_field(name="Report Time", value=f"{metar_data['reportTime']}")

        # Check if there are cloud cover data
        if 'clouds' in metar_data:
            clouds = metar_data['clouds']
            cloud_info = "\n".join([f"{cloud['cover']} Clouds at {cloud['base']} feet" for cloud in clouds])
            embed.add_field(name="Cloud Cover", value=cloud_info)

        # Add raw METAR Info to Embed
        embed.add_field(name="Raw METAR", value=f"{metar_data['rawOb']}")

        # Add airport picture as the thumbnail
        embed.set_thumbnail(url="https://media.istockphoto.com/id/537337166/photo/air-trafic-control-tower-and-airplance-at-paris-airport.jpg?b=1&s=612x612&w=0&k=20&c=kp14V8AXFNUh5jOy3xPQ_sxhOZLWXycdBL-eUGviMOQ=")

        # Set Embed Footer
        text = "Data Provided by Aviation Weather Center API."
        embed.set_footer(text=text)

        await ctx.send(embed=embed)

    except Exception as e: await logger.error(f"An error occurred in metar command: {e}")

    
async def get_metar_info(icao_code: str):
    """
    Description:
        Fetches METAR information for a specified airport ICAO code.

    Parameters:
        icao_code (str): The ICAO code of the airport for which METAR information is requested.

    Returns:
        dict: A dictionary containing METAR information, or None if the data couldn't be retrieved.

    Raises:
        ValueError: If the provided ICAO code is not valid (incorrect format).
        requests.RequestException: If there is an issue with the HTTP request.
    """
    # API URL for METAR info
    api_url = f"https://aviationweather.gov/cgi-bin/data/metar.php?ids={icao_code}&format=json"
    
    try:
        # Send a GET request to the API
        response = requests.get(api_url)

        # Return the response if the request was successful
        if response.status_code == 200: return response.json()[0]
        
        # If the request was unsuccessful, return nothing
        else: return None

    # Log any Errors
    except Exception as e:
        await logger.error(f"An error occurred in get_metar_info: {e}")
        return None

@bot.command()
async def atis(ctx, icao_code: str):
    """
    Command to fetch and display ATIS information for a specified airport ICAO code.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        icao_code (str): The ICAO code of the airport for which ATIS information is requested.

    Returns:
        None
    """
    try:
        # Perform Input Validation on the ICAO Airport Code
        if not icao_code.isalnum() or not (len(icao_code) == 4):
            await ctx.send("Invalid ICAO code format. It must be 4 alphanumeric characters.")
            return

        # Get the ATIS data from the API
        atis_data = await get_atis_info(icao_code)

        # Send Error Message and Exit Function if No Information was Retrieved
        if atis_data is None:
            await ctx.send(f"Unable to retrieve ATIS info for {icao_code}")
            return

        # Send the ATIS information as a simple message
        await ctx.send(atis_data['datis'])

    except Exception as e:
        await logger.error(f"An error occurred in atis command: {e}")

async def get_atis_info(icao_code: str):
    """
    Description:
        Fetches ATIS information for a specified airport ICAO code.

    Parameters:
        icao_code (str): The ICAO code of the airport for which ATIS information is requested.

    Returns:
        dict: A dictionary containing ATIS information, or None if the data couldn't be retrieved.

    Raises:
        requests.RequestException: If there is an issue with the HTTP request.
    """
    # API URL for ATIS info
    api_url = f"https://datis.clowd.io/api/{icao_code}"
    
    try:
        # Send a GET request to the API
        response = requests.get(api_url)

        # Return the response if the request was successful
        if response.status_code == 200:
            data = response.json()
            return data[0] if data else None
        
        # If the request was unsuccessful, return nothing
        else:
            return None

    # Log any Errors
    except Exception as e:
        await logger.error(f"An error occurred in get_atis_info: {e}")
        return None
