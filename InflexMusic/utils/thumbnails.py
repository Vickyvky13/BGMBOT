import os
import re
import random
import aiofiles
import aiohttp
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps, ImageFont
from unidecode import unidecode
from youtubesearchpython.__future__ import VideosSearch

from InflexMusic import app
from config import YOUTUBE_IMG_URL

def make_col():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


def clear(text):
    list = text.split(" ")
    title = ""
    for i in list:
        if len(title) + len(i) < 60:
            title += " " + i
    return title.strip()


async def get_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown Mins"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                views = result["viewCount"]["short"]
            except:
                views = "Unknown Views"
            try:
                channel = result["channel"]["name"]
            except:
                channel = "Unknown Channel"

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()

        youtube = Image.open(f"cache/thumb{videoid}.png")
        image1 = changeImageSize(1280, 720, youtube)
        sex = changeImageSize(900, 380, youtube)
        image2 = image1.convert("RGBA")
        background = image2.filter(filter=ImageFilter.BoxBlur(40))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.5)
        logo = ImageOps.expand(sex, border=10, fill="white")
        # changing logo color
        im = logo
        im = im.convert('RGBA')
        color = make_col()

        data = np.array(im)
        red, green, blue, alpha = data.T

        white_areas = (red == 255) & (blue == 255) & (green == 255)
        data[..., :-1][white_areas.T] = color

        im2 = Image.fromarray(data)
        logo = im2
        background.paste(logo, (177, 120))
        draw = ImageDraw.Draw(background)
        arial = ImageFont.truetype("InflexMusic/assets/font2.ttf", 30)
        font = ImageFont.truetype("InflexMusic/assets/font.ttf", 30)
        line_length = 580  
        text_x_position = 565
    
        red_length = int(line_length * 0.6)
        white_length = line_length - red_length

    
        start_point_red = (text_x_position, 380)
        end_point_red = (text_x_position + red_length, 380)
        draw.line([start_point_red, end_point_red], fill="red", width=9)

    
        start_point_white = (text_x_position + red_length, 380)
        end_point_white = (text_x_position + line_length, 380)
        draw.line([start_point_white, end_point_white], fill="white", width=8)

    
        circle_radius = 10 
        circle_position = (end_point_red[0], end_point_red[1])
        draw.ellipse([circle_position[0] - circle_radius, circle_position[1] - circle_radius,
                      circle_position[0] + circle_radius, circle_position[1] + circle_radius], fill="red")
        draw.text((1110, 8), unidecode(app.name), fill="white", font=arial)
        draw.text(
            (55, 560),
            f"{channel} | {views[:23]}",
            (255, 255, 255),
            font=arial,
        )
        draw.text(
            (57, 600),
            clear(title),
            (255, 255, 255),
            font=font,
        )
        draw.line(
            [(55, 660), (1220, 660)],
            fill="white",
            width=5,
            joint="curve",
        )
        draw.text(
            (36, 685),
            "00:00",
            (255, 255, 255),
            font=arial,
        )
        draw.text(
            (1185, 685),
            f"{duration[:23]}",
            (255, 255, 255),
            font=arial,
        )
        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass
        background.save(f"cache/{videoid}.png")
        return f"cache/{videoid}.png"
    except Exception as e:
        print(e)
        return YOUTUBE_IMG_URL
