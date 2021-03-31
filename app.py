from werkzeug.utils import secure_filename
from flask import Flask,render_template,request,url_for,redirect,Response,flash
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.secret_key = "dont tell anyone"

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "img.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db = SQLAlchemy(app)



class data(db.Model):
    id=db.Column(db.INTEGER, primary_key=True)
    email=db.Column(db.String(100))
    first_name=db.Column(db.String(100))
    last_name=db.Column(db.String(100))
    phone_number=db.Column(db.String(100))
    contact_address=db.Column(db.Text)
    office_hours=db.Column(db.Text)
    assigned_time=db.Column(db.Text)
    received_assigned_time=db.Column(db.Text)
    img = db.Column(db.LargeBinary, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)


@app.route('/',methods=['GET'])
def index():
    # flash("hello")
    db.create_all()
    return render_template('question.html')



@app.route('/upload', methods=['POST'])
def upload():
    email=request.form['email']
    first_name=request.form['first_name']
    last_name=request.form['last_name']
    phone_number=request.form['phone_number']
    contact_address=request.form['contact_address']
    office_hours=request.form['office_hours']
    assigned_time=request.form['assigned_time']
    received_assigned_time=request.form['received_assigned_time']
    pic = request.files['pic']
    if not pic:
        return 'No File selected!', 400

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return 'Bad upload!', 400

    img = data(email=email,first_name=first_name,last_name=last_name,phone_number=phone_number,contact_address=contact_address,office_hours=office_hours,assigned_time=assigned_time,received_assigned_time=received_assigned_time,img=pic.read(), name=filename, mimetype=mimetype)
    db.session.add(img)
    db.session.commit()
    # flash("Data inserted Successfully")
    return redirect(url_for('index'))


@app.route("/response")
def response():
    all_data=data.query.all()

    return render_template('response.html',Data=all_data)




@app.route('/view/<int:id>')
def get_data(id):
    img = data.query.filter_by(id=id).first()
    if not img:
        return 'File Not Found!', 404

    return Response(img.img,mimetype=img.mimetype)

@app.route('/delete/<int:id>/',methods=['GET','POST'])
def delete(id):
    my_data=data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash=('hello')
    return redirect(url_for('response'))


if __name__ == '__main__':
    app.run(debug=True)