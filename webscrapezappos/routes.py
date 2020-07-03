from flask import render_template, request, redirect, url_for, flash
from webscrapezappos import app, CLASSIFIER, SCALER, PCA, ENCODER 
from werkzeug.utils import secure_filename
from webscrapezappos.helper import allowed_file
import os 
import cv2

@app.route('/', methods=['GET', 'POST'])
@app.route('/upload', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Check if post request has file part
        if 'photo' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['photo']

        # Check submit empty file
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('classify', filename=filename))
    return render_template('home.html')

@app.route('/classify')
def classify():
    filename = request.args.get('filename')
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img = cv2.imread(file_path, 0)
    img_resize = cv2.resize(img, (510,250), cv2.INTER_AREA)
    img_resize_flatten = img_resize.reshape((1,-1)) 
    img_resize_flatten_scaled = SCALER.transform(img_resize_flatten)
    img_resize_flatten_scaled_reduced = PCA.transform(img_resize_flatten_scaled)
    predictions = CLASSIFIER.predict_proba(img_resize_flatten_scaled_reduced).flatten().tolist()
    predictions = [round(predictions[i], 5) for i in range(len(predictions))] # Round the predictions to 5 decimal 
    predictions_label = list(ENCODER.inverse_transform([0,1,2,3,4]))
    result = list(zip(predictions_label, predictions))
    result.sort(key = lambda x: x[1], reverse=True)
    img_src = url_for('static', filename=f'images/{filename}')
    # return {
    #     "brandPredictions": []
    # }
    return render_template('classify.html', posts=result, img_src=img_src, title='Classify')
