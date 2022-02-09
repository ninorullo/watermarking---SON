import json
import os
from flask import Flask, render_template, url_for, redirect, request, flash, session
from forms import ImageForm, ExtractForm
from werkzeug.utils import secure_filename

from watermarking.signature_maker import generate_signature
from watermarking.blind_watermark import embed_fixed_key,extract_fixed_key

app = Flask(__name__)

app.config['SECRET_KEY'] = 'f4286ba8a843ed868fe446d85e536dbc'

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/embed", methods=['GET', 'POST'])
def embed():
    form = ImageForm()

    if form.validate_on_submit():
        s = form.signature.data
        wm_path = os.path.join('static', 'utils', 'watermark.png')
        generate_signature(s, wm_path)
        f = form.image.data
        filename = secure_filename(f.filename)
        filename_path = os.path.join('static', 'images', filename)
        f.save(filename_path)

        out_path = os.path.join('static', 'images', "wm_"+filename)
        embed_fixed_key(filename_path, wm_path, out_path)
        
        flash('Image watermarked successfully!', 'success')
        messages = json.dumps({"filename": "wm_"+filename})
        session['messages'] = messages
        return redirect(url_for('result', messages=messages))

    return render_template('embed.html', title='Embed', form=form)


@app.route("/extract", methods=['GET', 'POST'])
def extract():
    form = ExtractForm()

    if form.validate_on_submit():
        #s = form.signature_len.data
        wm_path = os.path.join('static', 'utils', 'reference.png')
        #generate_signature('A'*s, wm_path)
        
        f = form.image.data
        filename = secure_filename(f.filename)
        filename_path = os.path.join('static', 'images', filename)
        f.save(filename_path)

        out_path = os.path.join('static', 'images', "extracted_"+filename)
        extract_fixed_key(filename_path, wm_path, out_path)
        
        flash('Watermarked extracted successfully!', 'success')
        messages = json.dumps({"filename": "extracted_"+filename})
        session['messages'] = messages
        return redirect(url_for('result', messages=messages))

    return render_template('extract.html', title='Extract', form=form)


@app.route("/result")
def result():
    messages = request.args['messages']
    messages = session['messages']
    return render_template('result.html', title='Result', messages=json.loads(messages))


if __name__ == '__main__':
    app.run(debug=True)
