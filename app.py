from flask import Flask, app, request, render_template, redirect, url_for
from database import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

app = create_app()


"""
sample of expected calendar data:

class | end_date/time | description 

["CS306", "2024-12-15 23:59", "Reading chapter 1"]
"""

def capture_calendar_data(data):
    pass

@app.route("/")
def hello_world():
    return redirect(url_for("schedule"))

@app.route("/schedule")
def schedule():
    from models.event import Event
    events = Event.query.order_by(Event.status == 'completed', Event.end_datetime.asc()).all()
    class_names = {e.class_name for e in events}
    return render_template("schedule.html", items=events, classes=class_names)


@app.route("/postevent", methods=['POST'])
def post_calendar():
    from models.event import Event
    data = request.form.to_dict()
    print(data)
    new_event = Event(
        class_name=data['class_name'],
        end_datetime=data['end_datetime'],
        description=data['description'],
        status="not started"
    )

    db.session.add(new_event)
    db.session.commit()
    
    return redirect(url_for("schedule"))

@app.route("/change_status", methods=['POST'])
def change_status():
    from models.event import Event
    data = request.form.to_dict()
    event_id = int(data['event_id'])
    new_status = data['new_status']

    event = Event.query.get(event_id)
    if event:
        event.status = new_status
        db.session.commit()

    return redirect(url_for("schedule"))

@app.route("/delete/<int:event_id>")
def delete_event(event_id):
    from models.event import Event
    event = Event.query.get(event_id)
    if event:
        db.session.delete(event)
        db.session.commit()
    
    return redirect(url_for("schedule"))

if __name__ == "__main__":
    app.run(debug=True)