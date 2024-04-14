from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from group_data import WeekData

days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
cabinets = [str(i) for i in range(1, 26)]
cabinets.insert(0, "биб.")
cabinets.insert(0, "зал.")


def toImage(week:WeekData, pairs:list[str], teachers:list[str]) -> BytesIO:
    global days

    offX = 16
    sizeY = 220
    sizey = 50

    img = Image.new("RGB", (562 + offX * 2, sizeY*6), (200, 200, 200))
    imgDraw = ImageDraw.Draw(img, "RGB")
    font = ImageFont.truetype("times.ttf", 20)

    for i in range(6):
        day = week[i]
        offY = sizey / 4 + sizeY * i
        imgDraw.rectangle((offX, 0 + offY, 562 + offX, 48 + offY), None, (100, 100, 100), 4)


        imgDraw.rectangle((offX, 48 + offY, 562 + offX, 48 + sizey * 3 + offY), None, (100, 100, 100), 4)
        imgDraw.line((offX, 48 + sizey + offY, 562 + offX, 48 + sizey + offY), (100, 100, 100), 4)
        imgDraw.line((offX, 48 + sizey * 2 + offY, 562 + offX, 48 + sizey * 2 + offY), (100, 100, 100), 4)
        imgDraw.line((300 + offX, 48 + offY, 300 + offX, 48 + sizey * 3 + offY), (100, 100, 100), 4)
        imgDraw.line((500 + offX, 48 + offY, 500 + offX, 48 + sizey * 3 + offY), (100, 100, 100), 4)

        topText = days[i]
        if day[0] != -1:
            topText += f" | Приходить к {day[0]+1}-й паре"

            for pair in [day[1], day[2], day[3]]:
                if min(pair) == -1:
                    continue
                imgDraw.text((6 + offX, 65 + sizey * i + offY), pairs[pair[0]], (0, 0, 0), font=font)
                imgDraw.text((306 + offX, 65 + sizey * i + offY), teachers[pair[1]], (0, 0, 0), font=font)
                imgDraw.text((531 + offX - font.getlength(cabinets[pair[2]])/2, 65 + sizey * i + offY), cabinets[pair[2]], (0, 0, 0), font=font)

        imgDraw.text((281 - font.getlength(topText) / 2 + offX, 10 + offY), topText, (0, 0, 0), font=font)

    output = BytesIO()
    img.save(output, format='PNG')
    return output
