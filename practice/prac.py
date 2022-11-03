from crypt import methods
from flask import Flask, request
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tast.db'
db = SQLAlchemy(app)
SQLALCHEMY_TRACK_MODIFICATIONS = False

class Salon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employer = db.Column(db.String, nullable=False)
    styles = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"{self.id} - {self.employer} - {self.styles}"

@app.route('/')
@app.route('/salon')
def get():
    sal = Salon.query.all()
    output = []
    for i in sal:
        data = {'id': i.id, 'employer': i.employer, 'styles': i.styles}

        output.append(data)

    return {"salon": output}

@app.route('/salon/<int:id>')
def get_one(id):
    sal = Salon.query.get_or_404(id)

    return {"id":sal.id, "employer": sal.employer, "styles": sal.styles}
@app.route('/salon', methods=['POST'])
def add():
    data = request.get_json()
    i = data['id']
    e = data['employer']
    s = data['styles']

    sal = Salon(id=i, employer=e, styles=s)

    db.session.add(sal)
    db.session.commit()

    return {"employer": sal.employer}

@app.route('/salon/<int:id>', methods=['DELETE'])
def delete(id):
    sal = Salon.query.get(id)
    if sal is None:
        return {"error": "not found"}

    db.session.delete(sal)
    db.session.commit()

    return {"message deleted succesfuly": sal.id}

if __name__ == '__main__':
    app.run(debug=True)
