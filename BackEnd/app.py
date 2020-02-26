# Set up virtual environment
# Set up Flask boilerplate code
# Set up SQLAlchemy class tables
# Set up Flask routes for each class table

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku

from secs import hello


app = Flask(__name__)
CORS(app)
heroku = Heroku(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

app.config["SQLALCHEMY_DATABASE_URI"] = hello

class CalendarInput(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(), nullable=False)
    date = db.Column(db.Integer, nullable=False)
    month = db.Column(db.String(), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __init__(self, content, date, month, year):
        self.content = content
        self.date = date
        self.month = month
        self.year = year


class CalendarInputSchema(ma.Schema):
    class Meta:
        fields = ("id", "content", "date", "month", "year")

calendar_input_schema = CalendarInputSchema()
calendar_inputs_schema = CalendarInputSchema(many=True)


@app.route("/calendar-input/post", methods=["POST"])
def add_calendar_input():
    if request.content_type == "application/json":
        post_data = request.get_json()
        content = post_data.get("content")
        date = post_data.get("date")
        month = post_data.get("month")
        year = post_data.get("year")

        record = CalendarInput(content, date, month, year)
        db.session.add(record)
        db.session.commit()

        return jsonify("Data Posted")

    return jsonify("Error: requests must be sent as JSON data.")


@app.route("/calendar-inputs", methods=["GET"])
def get_all_calendar_inputs():
    # all_inputs = db.session.query(CalendarInput.id, CalendarInput.content, CalendarInput.date, CalendarInput.month, CalendarInput.year).all()
    # all_inputs = db.session.query(CalendarInput).all()
    # return jsonify(all_inputs)
    # marshmallow below,
    all_inputs = CalendarInput.query.all()
    return jsonify(calendar_inputs_schema.dump(all_inputs))


@app.route("/calendar-inputs/<date>/<month>/<year>/", methods=["GET"])
def get_one_calendar_input(date, month, year):
    # one_input = db.session.query(CalendarInput.id, CalendarInput.content, CalendarInput.date, CalendarInput.month, CalendarInput.year).filter(CalendarInput.date == date, CalendarInput.month == month, CalendarInput.year == year).first()
    # return jsonify(one_input)
    # marshmallow below,
    one_input = db.session.query(CalendarInput).filter(CalendarInput.date == date, CalendarInput.month == month, CalendarInput.year == year).first()
    return jsonify(calendar_input_schema.dump(one_input))


@app.route("/calendar-inputs/update/<id>", methods=["PUT"])
def update_calendar_input(id):
    if request.content_type == "application/json":
        put_data = request.get_json()
        content = put_data.get("content")

        calendar_input = db.session.query(CalendarInput).filter(CalendarInput.id == id).first()
        calendar_input.content = content
        db.session.commit()

        return jsonify("Data Updated")

    return jsonify("Error: data must be sent as JSON data.")


@app.route("/calendar-inputs/delete/<id>", methods=["DELETE"])
def delete_calendar_input(id):
    calendar_input = db.session.query(CalendarInput).filter(CalendarInput.id == id).first()
    db.session.delete(calendar_input)
    db.session.commit()

    return jsonify("Data Deleted")


if __name__ == "__main__":
    app.debug = True
    app.run()
