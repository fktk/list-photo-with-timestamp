import json
import matplotlib.pyplot as plt
import japanize_matplotlib
from datetime import datetime
from pathlib import Path
from PIL import Image

convert_image = {
    # そのまま
    1: lambda img: img,
    # 左右反転
    2: lambda img: img.transpose(Image.FLIP_LEFT_RIGHT),
    # 180度回転
    3: lambda img: img.transpose(Image.ROTATE_180),
    # 上下反転
    4: lambda img: img.transpose(Image.FLIP_TOP_BOTTOM),
    # 左右反転＆反時計回りに90度回転
    5: lambda img: img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_90),
    # 反時計回りに270度回転
    6: lambda img: img.transpose(Image.ROTATE_270),
    # 左右反転＆反時計回りに270度回転
    7: lambda img: img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_270),
    # 反時計回りに90度回転
    8: lambda img: img.transpose(Image.ROTATE_90),
}


def get_data(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data


def trim_image(image):
    exif = image._getexif()
    orientation = exif.get(0x112, 1)
    thumbnail_img = convert_image[orientation](image)
    thumbnail_img = expand2square(thumbnail_img, (255, 255, 255))
    return thumbnail_img


def expand2square(pil_img, background_color):
    width, height = pil_img.size
    if width == height:
        return pil_img
    elif width > height:
        result = Image.new(pil_img.mode, (width, width), background_color)
        result.paste(pil_img, (0, (width - height) // 2))
        return result
    else:
        result = Image.new(pil_img.mode, (height, height), background_color)
        result.paste(pil_img, ((height - width) // 2, 0))
        return result


def main():

    years = [2011, 2012, 2013, 2014]
    for year in years:
        data = get_data(f'./data_{year}.json')
        indices = (len(data)-1) // 20
        print(year)
        print(len(data))
        for index in range(indices+1):
            save_image(data[index*20: (index+1)*20], year, index)


def save_image(data, year, index):
    plt.figure(figsize=(8.27, 11.69), dpi=450)
    plt.subplots_adjust(
        wspace=0.1, hspace=0.3, left=0.03, right=0.98, top=0.9, bottom=0.1
    )
    for i, d in enumerate(data):
        file = Path(d['path'])
        image = Image.open(file)
        image = trim_image(image)
        date = datetime.strptime(d['date'], '%Y:%m:%d %H:%M:%S')
        plt.subplot(5, 4, i+1)
        plt.tick_params(labelbottom=False)
        plt.tick_params(labelleft=False)
        plt.tick_params(bottom=False)
        plt.tick_params(left=False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        plt.title(
            f"{date.year}年{date.month}月{date.day}日 {date.hour}時{date.minute}分",
            y=-0.15,
            fontsize=8
        )
        plt.imshow(image)
    plt.savefig(f'{year}_{index}.png')


if __name__ == '__main__':
    main()
