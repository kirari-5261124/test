from PIL import Image, ImageDraw, ImageFont

def create_sample_image(text):
    img = Image.new('RGB', (300, 200), color=(255, 255, 255))
    d = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()

    # 修正ポイント：textsize → textbbox
    bbox = d.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]

    d.text(((300 - w) / 2, (200 - h) / 2), text, fill=(0, 0, 0), font=font)
    return img

# サンプル画像の生成
sample_images = [
    create_sample_image("Sample 1"),
    create_sample_image("Sample 2"),
    create_sample_image("Sample 3")
]
