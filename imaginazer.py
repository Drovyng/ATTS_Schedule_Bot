from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from group_data import WeekData, DayData

days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
cabinets = [str(i) for i in range(1, 26)]
cabinets.insert(0, "биб.")
cabinets.insert(0, "сп.зал")


def toImage(week:WeekData, pairs:list[str], teachers:list[str]) -> BytesIO:
    
    import pip
    pip.main(['install', "pyautogui"])
    
    global days

    scale = 32.0 / 20.0

    offX = int(16 * scale)
    sizeY = int(220 * scale)
    sizey = int(50 * scale)
    sizeX = int(565 * scale)

    width = int(4 * scale)

    s48 = int(48 * scale)
    s300 = int(300 * scale)
    s500 = int(500 * scale)
    s6 = int(6 * scale)
    s65 = int(65 * scale)
    s306 = int(306 * scale)
    s532 = int(532 * scale)
    s10 = int(10 * scale)

    img = Image.new("RGB", (sizeX + offX * 2, sizeY*6), (200, 200, 200))
    imgDraw = ImageDraw.Draw(img, "RGB")
    font = ImageFont.truetype("times.ttf", int(20 * scale))

    for i in range(6):
        day = week[i]
        offY = sizey / 4 + sizeY * i
        imgDraw.rectangle((offX, offY, sizeX + offX, s48 + offY), None, (100, 100, 100), width)

        imgDraw.rectangle((offX, s48 + offY, sizeX + offX, s48 + sizey * 3 + offY), None, (100, 100, 100), width)
        imgDraw.line((offX, s48 + sizey + offY, sizeX + offX, s48 + sizey + offY), (100, 100, 100), width)
        imgDraw.line((offX, s48 + sizey * 2 + offY, sizeX + offX, s48 + sizey * 2 + offY), (100, 100, 100), width)
        imgDraw.line((s300 + offX, s48 + offY, s300 + offX, s48 + sizey * 3 + offY), (100, 100, 100), width)
        imgDraw.line((s500 + offX, s48 + offY, s500 + offX, s48 + sizey * 3 + offY), (100, 100, 100), width)

        topText = days[i]
        if day[0] != -1:
            topText += f" | Приходить к {day[0]+1}-й паре"
            j = -1
            for pair in [day[1], day[2], day[3]]:
                j += 1
                if min(pair) == -1:
                    continue
                imgDraw.text((s6 + offX, s65 + sizey * j + offY), pairs[pair[0]], (0, 0, 0), font=font)
                imgDraw.text((s306 + offX, s65 + sizey * j + offY), teachers[pair[1]], (0, 0, 0), font=font)
                imgDraw.text((s532 + offX - font.getlength(cabinets[pair[2]])/2, s65 + sizey * j + offY), cabinets[pair[2]], (0, 0, 0), font=font)

        imgDraw.text((int(sizeX/2 - font.getlength(topText) / 2) + offX, s10 + offY), topText, (0, 0, 0), font=font)

    output = BytesIO()
    img.save(output, format='PNG')
    return output



def toImageDay(day:DayData, dayText:str, pairs:list[str], teachers:list[str]) -> BytesIO:
    global days

    scale = 32.0 / 20.0

    offX = int(16 * scale)
    sizeY = int(220 * scale)
    sizey = int(50 * scale)
    sizeX = int(565 * scale)

    width = int(4 * scale)

    s48 = int(48 * scale)
    s300 = int(300 * scale)
    s500 = int(500 * scale)
    s6 = int(6 * scale)
    s65 = int(65 * scale)
    s306 = int(306 * scale)
    s532 = int(532 * scale)
    s10 = int(10 * scale)

    img = Image.new("RGB", (sizeX + offX * 2, sizeY + 500), (200, 200, 200))
    imgDraw = ImageDraw.Draw(img, "RGB")
    font = ImageFont.truetype("times.ttf", int(20 * scale))

    offY = sizey / 4
    imgDraw.rectangle((offX, offY, sizeX + offX, s48 + offY), None, (100, 100, 100), width)

    imgDraw.rectangle((offX, s48 + offY, sizeX + offX, s48 + sizey * 3 + offY), None, (100, 100, 100), width)
    imgDraw.line((offX, s48 + sizey + offY, sizeX + offX, s48 + sizey + offY), (100, 100, 100), width)
    imgDraw.line((offX, s48 + sizey * 2 + offY, sizeX + offX, s48 + sizey * 2 + offY), (100, 100, 100), width)
    imgDraw.line((s300 + offX, s48 + offY, s300 + offX, s48 + sizey * 3 + offY), (100, 100, 100), width)
    imgDraw.line((s500 + offX, s48 + offY, s500 + offX, s48 + sizey * 3 + offY), (100, 100, 100), width)

    if day[0] != -1:
        dayText += f" | Приходить к {day[0]+1}-й паре"
        j = -1
        for pair in [day[1], day[2], day[3]]:
            j += 1
            if min(pair) == -1:
                continue
            imgDraw.text((s6 + offX, s65 + sizey * j + offY), pairs[pair[0]], (0, 0, 0), font=font)
            imgDraw.text((s306 + offX, s65 + sizey * j + offY), teachers[pair[1]], (0, 0, 0), font=font)
            imgDraw.text((s532 + offX - font.getlength(cabinets[pair[2]])/2, s65 + sizey * j + offY), cabinets[pair[2]], (0, 0, 0), font=font)

    imgDraw.text((int(sizeX/2 - font.getlength(dayText) / 2) + offX, s10 + offY), dayText, (0, 0, 0), font=font)

    output = BytesIO()
    img.save(output, format='PNG')
    return output
