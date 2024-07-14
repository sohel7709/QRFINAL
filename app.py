from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import qrcode
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY',
                                'default_secret_key')  # Replace 'default_secret_key' with a strong key or set an environment variable


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form['url']

        try:
            # Generate QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)

            img = qr.make_image(fill='black', back_color='white')  # Set QR code color and background color
            img_filename = f"qr_code_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            img_path = os.path.join('static', img_filename)
            img.save(img_path)

            return render_template('result.html', img_filename=img_filename)
        except Exception as e:
            flash(f"An error occurred: {str(e)}")
            return redirect(url_for('home'))
    return render_template('index.html')


@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join('static', filename), as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
