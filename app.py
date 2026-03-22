from flask import Flask, render_template, request
import qrcode
import os
import uuid
from PIL import Image
import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    img_path = None

    if request.method == 'POST':
        data = request.form.get('data')
        name = request.form.get('name')
        phone = request.form.get('phone')

        if phone:
            vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{name or 'Contact'}
TEL;TYPE=CELL:{phone}
END:VCARD"""
            qr_data = vcard
        elif data:
            qr_data = data
        else:
            qr_data = None

        if qr_data:
            filename = f"qr_{uuid.uuid4().hex}.png"
            img_path = os.path.join('static', filename)

            fill_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            back_color = "#ffffff"

            qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=5
            )

            qr.add_data(qr_data)
            qr.make(fit=True)

            img = qr.make_image(fill_color=fill_color, back_color=back_color)
            
            logo_path = os.path.join('static', 'logo.png')
            if os.path.exists(logo_path):
                logo = Image.open(logo_path)
                qr_width, qr_height = img.size
                logo_size = int(qr_width * 0.2)
                logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
                pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
                img.paste(logo, pos, logo if logo.mode == 'RGBA' else None)
            
            img.save(img_path)

    return render_template('index.html', img_path=img_path)

if __name__ == '__main__':
    app.run(debug=True)