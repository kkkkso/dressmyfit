from PIL import Image


size = (960, 1280)

def resize_and_crop(image, size):
    # Crop to size ratio
    w, h = image.size
    target_w, target_h = size
    if w / h < target_w / target_h:
        new_w = w
        new_h = w * target_h // target_w
    else:
        new_h = h
        new_w = h * target_w // target_h
    image = image.crop(
        ((w - new_w) // 2, (h - new_h) // 2, (w + new_w) // 2, (h + new_h) // 2)
    )
    # resize
    image = image.resize(size, Image.LANCZOS)
    return image


def resize_and_padding(image, size):
    # Padding to size ratio
    w, h = image.size
    target_w, target_h = size
    if w / h < target_w / target_h:
        new_h = target_h
        new_w = w * target_h // h
    else:
        new_w = target_w
        new_h = h * target_w // w
    image = image.resize((new_w, new_h), Image.LANCZOS)
    # padding
    padding = Image.new("RGB", size, (255, 255, 255))
    padding.paste(image, ((target_w - new_w) // 2, (target_h - new_h) // 2))
    return padding

dress5 = Image.open(".\data\dress5.PNG")
dress6 = Image.open(".\data\dress6.PNG")
pants1 = Image.open(".\data\pants1.PNG")
pants2 = Image.open(".\data\pants2.PNG")
pants3 = Image.open(".\data\pants3.PNG")
pants4 = Image.open(".\data\pants4.PNG")
pants5 = Image.open(".\data\pants5.PNG")
pants6 = Image.open(".\data\pants6.PNG")

(resize_and_padding(dress5, size)).save("./data2/dress5.png", format="PNG")
(resize_and_padding(dress6, size)).save("./data2/dress6.png", format="PNG")
(resize_and_padding(pants1, size)).save("./data2/pants1.png", format="PNG")
(resize_and_padding(pants2, size)).save("./data2/pants2.png", format="PNG")
(resize_and_padding(pants3, size)).save("./data2/pants3.png", format="PNG")
(resize_and_padding(pants4, size)).save("./data2/pants4.png", format="PNG")
(resize_and_padding(pants5, size)).save("./data2/pants5.png", format="PNG")
(resize_and_padding(pants6, size)).save("./data2/pants6.png", format="PNG")

# source 이미지를 저장할 data 폴더와 , 결과 이미지를 저장할 data2 폴더 만들어서 코드 돌리기