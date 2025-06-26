from flask import Flask, render_template, request
from models import db, Workstation

app = Flask(__name__)
import os
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        workstation = Workstation(**form_data)
        db.session.add(workstation)
        db.session.commit()
        return "✅ Submitted Successfully"
    return render_template('lab-equip.html')

@app.route('/records')
def view_records():
    all_records = Workstation.query.all()
    return render_template('records.html', records=all_records)

if __name__ == '__main__':
    app.run(debug=True, port=5009)
