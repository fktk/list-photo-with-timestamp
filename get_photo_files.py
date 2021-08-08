import json
from datetime import datetime
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS

BASE_DIR = './../'
YEARS = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]


def main():
    for year in YEARS:
        data = []
        dir = Path(f'{BASE_DIR}/{str(year)}')
        files = dir.glob('*.J*')
        for file in files:
            image = Image.open(file)
            shot_date = get_shot_date(image)
            data.append({
                'path': str(file),
                'comment': '',
                'date': shot_date
            })
            data = sorted(data, key=lambda x: datetime.strptime(
                x['date'], '%Y:%m:%d %H:%M:%S'
            ))

        with open(f'./data_{year}.json', 'w') as f:
            json.dump(data, f, indent=2)


def get_shot_date(img):
    exif = img._getexif()
    try:
        for id, val in exif.items():
            tg = TAGS.get(id, id)
            if tg == "DateTimeOriginal":
                return val
    except AttributeError:
        return "None"

    return "None"


if __name__ == '__main__':
    main()
