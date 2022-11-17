"""Logged-in page routes."""
import os
import urllib
import uuid
from flask import Blueprint, redirect, render_template, url_for, request
from flask_login import current_user, login_required, logout_user
from tensorflow.keras.preprocessing.image import load_img , img_to_array
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import cv2

# Blueprint Configuration
main_bp = Blueprint(
    "main_bp", __name__, template_folder="templates", static_folder="static"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = load_model(os.path.join(BASE_DIR , 'CNN_MNIST_v1.h5'))


ALLOWED_EXT = set(['jpg' , 'jpeg' , 'png' , 'jfif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT

classes = ['0','1', '2' , '3' , '4' ,'5' ,'6', '7' ,'8' ,'9']


def predict(filename , model):
    print(filename)
    img = Image.open(filename).convert('L')
    img_array = cv2.imread(filename)
    new_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
    new_array = cv2.resize(new_array, (28,28))
    img=new_array.reshape(1,28,28,1)
    # img = load_img(filename , target_size = (28 , 28))
    # img = img_to_array(img)
    # img = img.reshape(-1 , 28 ,28 ,1)

    # img = img.astype('float32')
    # img = img/255
    result = model.predict(img)
    final_pred = classes[np.argmax(result)]

    classes_text=["Zero","One","Two","Three","Four","Five","Six","Seven","Eight","Nine"]
    return_value=str(final_pred)+" ["+classes_text[int(final_pred)]+"]"
    print(type(final_pred))
    # dict_result = {}
    # for i in range(10):
    #     dict_result[result[0][i]] = classes[i]

    # res = result[0]
    # res.sort()
    # res = res[::-1]
    # prob = res[:3]
    
    # prob_result = []
    # class_result = []
    # for i in range(3):
    #     prob_result.append((prob[i]*100).round(2))
    #     class_result.append(dict_result[prob[i]])

    return return_value

@main_bp.route("/", methods=["GET"])
@login_required
def dashboard():
    """Logged-in User Dashboard."""
    # error=session['messages']
    return render_template(
        "dashboard.jinja2",
        title="Dashboard",
        template="dashboard-template",
        current_user=current_user,
        body="Handwritten Digit Recognition - Prediction Page"
    )

@main_bp.route('/success' , methods = ['GET' , 'POST'])
@login_required
def success():
    error = ''
    # session['messages']=""
    target_img = os.path.join(os.getcwd() , 'user_login\\static\\images')
    if request.method == 'POST':
        if(request.form):
            link = request.form.get('link')
            try :
                resource = urllib.request.urlopen(link)
                unique_filename = str(uuid.uuid4())
                filename = unique_filename+".jpg"
                img_path = os.path.join(target_img , filename)
                output = open(img_path , "wb")
                output.write(resource.read())
                output.close()
                img = filename

                # class_result , prob_result = predict(img_path , model)

                # predictions = {
                #       "class1":class_result[0],
                #         "class2":class_result[1],
                #         "class3":class_result[2],
                #         "prob1": prob_result[0],
                #         "prob2": prob_result[1],
                #         "prob3": prob_result[2],
                # }
                result = predict(img_path,model)

            except Exception as e : 
                print(str(e))
                error = 'This image from this site is not accesible or inappropriate input'

            if(len(error) == 0):
                # return  render_template('success.html' , img  = img , predictions = predictions)

                return render_template("success.jinja2",title="Prediction Page",
                                    template="dashboard-template",
                                    current_user=current_user,
                                    body="Handwritten Digit Recognition - Prediction Page",
                                    img  = img , predictions = result)
            else:
                # session['messages'] = error
                return redirect("/")
                # render_template("dashboard.jinja2" , title="",template="dashboard-template",current_user=current_user,body="Handwritten Digit Recognition - Prediction Page" ,error = error) 

            
        elif (request.files):
            file = request.files['file']
            if file and allowed_file(file.filename):
                print(target_img)
                print(file.filename)
                file.save(os.path.join(target_img , file.filename))
                img_path = os.path.join(target_img , file.filename)
                img = file.filename

                # class_result , prob_result = predict(img_path , model)
                result = predict(img_path,model)

                # predictions = {
                #       "class1":class_result[0],
                #         "class2":class_result[1],
                #         "class3":class_result[2],
                #         "prob1": prob_result[0],
                #         "prob2": prob_result[1],
                #         "prob3": prob_result[2],
                # }

            else:
                error = "Please upload images of jpg , jpeg and png extension only"

            if(len(error) == 0):
                return  render_template('success.jinja2' , title="Prediction Page", img  = img , predictions = result)
            else:
                return redirect("/")
                # render_template("dashboard.jinja2" , title="Dashboard",template="dashboard-template",current_user=current_user,body="Handwritten Digit Recognition - Prediction Page" ,error = error) 

    # else:
    #     return render_template('index.html')


@main_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for("auth_bp.login"))
