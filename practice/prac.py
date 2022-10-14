from flask import Flask,request,jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
db = SQLAlchemy(app)

class Salon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employer = db.Column(db.String(100), nullable=False )
    styles = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return f"{self.employer} - {self.styles}"

@app.route('/')
@app.route('/salon')
def salon():

    sal = Salon.query.all()

    output = []
    for i in sal:
        sal_dat = {'employer': i.employer, 'styles': i.styles}

        output.append(sal_dat)

    return {"salon": output}
@app.route('/salon/<id>')
def get(id):
    sal = Salon.query.get_or_404(id)

    return {"employer": sal.employer, "styles": sal.styles}

@app.route('/salon', methods=['POST'])
def add_salon():
    data = request.get_json()
    e = data['employer']
    s= data['styles']

    #validation
    if len(e) < 3:
        return {
            "message":"salon employer length must be more than 3"
        }
    sal = Salon(employer=e, styles=s)
    db.session.add(sal)
    db.session.commit()

    return {
        "id":"hhhhhhh"
    }
 




if __name__ == '__main__':
    app.run(debug=True)