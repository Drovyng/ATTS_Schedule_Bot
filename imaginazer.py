from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from group_data import WeekData, DayData, WeekDataTeacher, DayDataTeacher

days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
cabinets = [str(i) for i in range(1, 26)]
cabinets.insert(0, "биб.")
cabinets.insert(0, "сп.зал")
cabinets.append("кл.мк.")
cabinets.append("")

def getScreenshot() -> BytesIO:
    import pyautogui
    output = BytesIO()
    pyautogui.screenshot().save(output, format='PNG')
    return output

def toImage(week:WeekData, getPairs:list[str], getTeachers:list[str]) -> BytesIO:
    
    global days
    pairs = getPairs[:]
    pairs.append("")
    teachers = getTeachers[:]
    teachers.append("")

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

        topText = days[i]
        if day[0] == -1:
            day[0] = 0
        topText += f" | Приходить к {day[0]+1}-й паре"
        j = -1
        for pair in [day[1], day[2], day[3]]:
            j += 1
            if min(pair) == -1:
                continue
            imgDraw.text((s6 + offX, s65 + sizey * j + offY), pairs[pair[0]], (0, 0, 0), font=font)
            imgDraw.rectangle((s300 + offX, s65 + sizey * j + offY, sizeX + offX * 2, s65 + sizey * (j+1) + offY), (200, 200, 200))
            imgDraw.text((s306 + offX, s65 + sizey * j + offY), teachers[pair[1]], (0, 0, 0), font=font)
            imgDraw.text((s532 + offX - font.getlength(cabinets[pair[2]])/2, s65 + sizey * j + offY), cabinets[pair[2]], (0, 0, 0), font=font)
            
        imgDraw.text((int(sizeX/2 - font.getlength(topText) / 2) + offX, s10 + offY), topText, (0, 0, 0), font=font)
        
        
        imgDraw.rectangle((offX, offY, sizeX + offX, s48 + offY), None, (100, 100, 100), width)

        imgDraw.rectangle((offX, s48 + offY, sizeX + offX, s48 + sizey * 3 + offY), None, (100, 100, 100), width)
        imgDraw.line((offX, s48 + sizey + offY, sizeX + offX, s48 + sizey + offY), (100, 100, 100), width)
        imgDraw.line((offX, s48 + sizey * 2 + offY, sizeX + offX, s48 + sizey * 2 + offY), (100, 100, 100), width)
        imgDraw.line((s300 + offX, s48 + offY, s300 + offX, s48 + sizey * 3 + offY), (100, 100, 100), width)
        imgDraw.line((s500 + offX, s48 + offY, s500 + offX, s48 + sizey * 3 + offY), (100, 100, 100), width)

    output = BytesIO()
    img.save(output, format='PNG')
    return output


def toImageTeacher(week:WeekDataTeacher, getPairs:list[str], getGroups:list[str]) -> BytesIO:
    
    global days
    pairs = getPairs[:]
    pairs.append("")
    groups = getGroups[:]
    groups.append("")

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

    img = Image.new("RGB", (sizeX * 2 + offX * 3, sizeY*6), (200, 200, 200))
    imgDraw = ImageDraw.Draw(img, "RGB")
    font = ImageFont.truetype("times.ttf", int(20 * scale))

    for i in range(6):
        day = week[i]
        offY = sizey / 4 + sizeY * i
        j = -1
        for pair in [day[0], day[1], day[2]]:
            j += 1
            if min(pair) == -1:
                continue
            imgDraw.text((s6 + offX, s65 + sizey * j + offY), pairs[pair[0]], (0, 0, 0), font=font)
            imgDraw.rectangle((s300 + offX, s65 + sizey * j + offY, sizeX + offX * 2, s65 + sizey * (j+1) + offY), (200, 200, 200))
            imgDraw.text((s306 + offX, s65 + sizey * j + offY), groups[pair[1]], (0, 0, 0), font=font)
            imgDraw.text((s532 + offX - font.getlength(cabinets[pair[2]])/2, s65 + sizey * j + offY), cabinets[pair[2]], (0, 0, 0), font=font)
        
        offXAdd = sizeX + offX
        j = -1
        for pair in [day[3], day[4], day[5]]:
            j += 1
            if min(pair) == -1:
                continue
            imgDraw.text((offXAdd + s6 + offX, s65 + sizey * j + offY), pairs[pair[0]], (0, 0, 0), font=font)
            imgDraw.rectangle((offXAdd + s300 + offX, s65 + sizey * j + offY, offXAdd + sizeX + offX * 2, s65 + sizey * (j+1) + offY), (200, 200, 200))
            imgDraw.text((offXAdd + s306 + offX, s65 + sizey * j + offY), groups[pair[1]], (0, 0, 0), font=font)
            imgDraw.text((offXAdd + s532 + offX - font.getlength(cabinets[pair[2]])/2, s65 + sizey * j + offY), cabinets[pair[2]], (0, 0, 0), font=font)
            
        dayText = days[i] + " | 1-я смена"
        imgDraw.text((int(sizeX/2 - font.getlength(dayText) / 2) + offX, s10 + offY), dayText, (0, 0, 0), font=font)
        dayText = days[i] + " | 2-я смена"
        imgDraw.text((int(sizeX/2 - font.getlength(dayText) / 2) + offX + offXAdd, s10 + offY), dayText, (0, 0, 0), font=font)
        
        
        imgDraw.rectangle((offX, offY, sizeX + offX, s48 + offY), None, (100, 100, 100), width)
        imgDraw.rectangle((offX, s48 + offY, sizeX + offX, s48 + sizey * 3 + offY), None, (100, 100, 100), width)
        imgDraw.line((offX, s48 + sizey + offY, sizeX + offX, s48 + sizey + offY), (100, 100, 100), width)
        imgDraw.line((offX, s48 + sizey * 2 + offY, sizeX + offX, s48 + sizey * 2 + offY), (100, 100, 100), width)
        imgDraw.line((s300 + offX, s48 + offY, s300 + offX, s48 + sizey * 3 + offY), (100, 100, 100), width)
        imgDraw.line((s500 + offX, s48 + offY, s500 + offX, s48 + sizey * 3 + offY), (100, 100, 100), width)
        
        
        imgDraw.rectangle((offXAdd + offX, offY, offXAdd + sizeX + offX, s48 + offY), None, (100, 100, 100), width)
        imgDraw.rectangle((offXAdd + offX, s48 + offY, offXAdd + sizeX + offX, s48 + sizey * 3 + offY), None, (100, 100, 100), width)
        imgDraw.line((offXAdd + offX, s48 + sizey + offY, offXAdd + sizeX + offX, s48 + sizey + offY), (100, 100, 100), width)
        imgDraw.line((offXAdd + offX, s48 + sizey * 2 + offY, offXAdd + sizeX + offX, s48 + sizey * 2 + offY), (100, 100, 100), width)
        imgDraw.line((offXAdd + s300 + offX, s48 + offY, offXAdd + s300 + offX, s48 + sizey * 3 + offY), (100, 100, 100), width)
        imgDraw.line((offXAdd + s500 + offX, s48 + offY, offXAdd + s500 + offX, s48 + sizey * 3 + offY), (100, 100, 100), width)

    output = BytesIO()
    img.save(output, format='PNG')
    return output


def toImageDay(day:DayData, dayText:str, getPairs:list[str], getTeachers:list[str]) -> BytesIO:
    global days
    pairs = getPairs[:]
    pairs.append("")
    teachers = getTeachers[:]
    teachers.append("")

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

    img = Image.new("RGB", (sizeX + offX * 2, sizeY), (200, 200, 200))
    imgDraw = ImageDraw.Draw(img, "RGB")
    font = ImageFont.truetype("times.ttf", int(20 * scale))

    offY = sizey / 4

    if day[0] == -1:
        day[0] = 0
    dayText += f" | Приходить к {day[0]+1}-й паре"
    j = -1
    for pair in [day[1], day[2], day[3]]:
        j += 1
        if min(pair) == -1:
            continue
        imgDraw.text((s6 + offX, s65 + sizey * j + offY), pairs[pair[0]], (0, 0, 0), font=font)
        imgDraw.rectangle((s300 + offX, s65 + sizey * j + offY, sizeX + offX * 2, s65 + sizey * (j+1) + offY), (200, 200, 200))
        imgDraw.text((s306 + offX, s65 + sizey * j + offY), teachers[pair[1]], (0, 0, 0), font=font)
        imgDraw.text((s532 + offX - font.getlength(cabinets[pair[2]])/2, s65 + sizey * j + offY), cabinets[pair[2]], (0, 0, 0), font=font)
        
    imgDraw.text((int(sizeX/2 - font.getlength(dayText) / 2) + offX, s10 + offY), dayText, (0, 0, 0), font=font)
    
    
    imgDraw.rectangle((offX, offY, sizeX + offX, s48 + offY), None, (100, 100, 100), width)

    imgDraw.rectangle((offX, s48 + offY, sizeX + offX, s48 + sizey * 3 + offY), None, (100, 100, 100), width)
    imgDraw.line((offX, s48 + sizey + offY, sizeX + offX, s48 + sizey + offY), (100, 100, 100), width)
    imgDraw.line((offX, s48 + sizey * 2 + offY, sizeX + offX, s48 + sizey * 2 + offY), (100, 100, 100), width)
    imgDraw.line((s300 + offX, s48 + offY, s300 + offX, s48 + sizey * 3 + offY), (100, 100, 100), width)
    imgDraw.line((s500 + offX, s48 + offY, s500 + offX, s48 + sizey * 3 + offY), (100, 100, 100), width)

    output = BytesIO()
    img.save(output, format='PNG')
    return output




def toImageDayTeacher(day:DayDataTeacher, dayText:str, getPairs:list[str], getGroups:list[str]) -> BytesIO:
    
    global days
    pairs = getPairs[:]
    pairs.append("")
    groups = getGroups[:]
    groups.append("")

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

    img = Image.new("RGB", (sizeX * 2 + offX * 3, sizeY*2), (200, 200, 200))
    imgDraw = ImageDraw.Draw(img, "RGB")
    font = ImageFont.truetype("times.ttf", int(20 * scale))

    day = week[i]
    offY = sizey / 4
    j = -1
    for pair in [day[0], day[1], day[2]]:
        j += 1
        if min(pair) == -1:
            continue
        imgDraw.text((s6 + offX, s65 + sizey * j + offY), pairs[pair[0]], (0, 0, 0), font=font)
        imgDraw.rectangle((s300 + offX, s65 + sizey * j + offY, sizeX + offX * 2, s65 + sizey * (j+1) + offY), (200, 200, 200))
        imgDraw.text((s306 + offX, s65 + sizey * j + offY), groups[pair[1]], (0, 0, 0), font=font)
        imgDraw.text((s532 + offX - font.getlength(cabinets[pair[2]])/2, s65 + sizey * j + offY), cabinets[pair[2]], (0, 0, 0), font=font)
        
    offY = sizey / 4 + sizey

    j = -1
    for pair in [day[3], day[4], day[5]]:
        j += 1
        if min(pair) == -1:
            continue
        imgDraw.text((s6 + offX, s65 + sizey * j + offY), pairs[pair[0]], (0, 0, 0), font=font)
        imgDraw.rectangle((s300 + offX, s65 + sizey * j + offY, sizeX + offX * 2, s65 + sizey * (j+1) + offY), (200, 200, 200))
        imgDraw.text((s306 + offX, s65 + sizey * j + offY), groups[pair[1]], (0, 0, 0), font=font)
        imgDraw.text((s532 + offX - font.getlength(cabinets[pair[2]])/2, s65 + sizey * j + offY), cabinets[pair[2]], (0, 0, 0), font=font)
            
    dayText = days[i] + " | 1-я смена"
    imgDraw.text((int(sizeX/2 - font.getlength(dayText) / 2) + offX, s10 + offY - sizey), dayText, (0, 0, 0), font=font)
    dayText = days[i] + " | 2-я смена"
    imgDraw.text((int(sizeX/2 - font.getlength(dayText) / 2) + offX, s10 + offY), dayText, (0, 0, 0), font=font)
        
        
    imgDraw.rectangle((offX, offY, sizeX + offX, s48 + offY), None, (100, 100, 100), width)
    imgDraw.rectangle((offX, s48 + offY, sizeX + offX, s48 + sizey * 3 + offY), None, (100, 100, 100), width)
    imgDraw.line((offX, s48 + sizey + offY, sizeX + offX, s48 + sizey + offY), (100, 100, 100), width)
    imgDraw.line((offX, s48 + sizey * 2 + offY, sizeX + offX, s48 + sizey * 2 + offY), (100, 100, 100), width)
    imgDraw.line((s300 + offX, s48 + offY, s300 + offX, s48 + sizey * 3 + offY), (100, 100, 100), width)
    imgDraw.line((s500 + offX, s48 + offY, s500 + offX, s48 + sizey * 3 + offY), (100, 100, 100), width)
        
        
    imgDraw.rectangle((offXAdd + offX, offY, offXAdd + sizeX + offX, s48 + offY), None, (100, 100, 100), width)
    imgDraw.rectangle((offXAdd + offX, s48 + offY, offXAdd + sizeX + offX, s48 + sizey * 3 + offY), None, (100, 100, 100), width)
    imgDraw.line((offXAdd + offX, s48 + sizey + offY, offXAdd + sizeX + offX, s48 + sizey + offY), (100, 100, 100), width)
    imgDraw.line((offXAdd + offX, s48 + sizey * 2 + offY, offXAdd + sizeX + offX, s48 + sizey * 2 + offY), (100, 100, 100), width)
    imgDraw.line((offXAdd + s300 + offX, s48 + offY, offXAdd + s300 + offX, s48 + sizey * 3 + offY), (100, 100, 100), width)
    imgDraw.line((offXAdd + s500 + offX, s48 + offY, offXAdd + s500 + offX, s48 + sizey * 3 + offY), (100, 100, 100), width)

    output = BytesIO()
    img.save(output, format='PNG')
    return output
