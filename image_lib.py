import binascii, base64, io
from PIL import Image

def get_image(img):
    global image_max_width
    max_width = int(image_max_width)
    imageExt = img.format.lower()
    imgFormat = img.format
    imWidth = img.width
    if imWidth > max_width:
        imHeight = img.height
        k = imWidth/imHeight
        h = round(max_width/k)
        img = img.resize((max_width,h))
    with io.BytesIO() as output:
        img.save(output, format=imgFormat)
        contents = output.getvalue()

    base64_bytes = base64.b64encode(contents)
    base64_message = base64_bytes.decode('ascii')
    imageURL = f'<img src="data:image/{imageExt};base64,{base64_message}"/>'
    return imageURL

image_max_width = "none"