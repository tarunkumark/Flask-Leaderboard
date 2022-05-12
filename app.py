import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Teams(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    member1 = db.Column(db.String(100), nullable=True)
    member2 = db.Column(db.String(100), nullable=True)
    member3 = db.Column(db.String(100), nullable=True)
    member4 = db.Column(db.String(100), nullable=True)
    member5 = db.Column(db.String(100), nullable=True)
    current_stage = db.Column(db.Integer, default = 0)
    score = db.Column(db.Integer, nullable=True, default = 0)
    
keys = ['aaaaaa', 'bbbbbb', 'cccccc', 'dddddd', 'eeeeee', 'ffffff']
@app.route('/')
def index():
    teams = Teams.query.order_by(Teams.score.desc()).all()
    return render_template('index.html', teams=teams)

@app.route('/<int:team_id>/')
def team(team_id):
    team = Teams.query.get_or_404(team_id)
    return render_template('team.html', team=team)


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        member1 = request.form['member1']
        member2= request.form['member2']
        member3 = request.form['member3']
        member4 = request.form['member4']
        member5 = request.form['member5']
        team = Teams(name=name,
                          member1=member1,
                          member2=member2,
                          member3=member3,
                          member4=member4,
                          member5=member5,
                          current_stage=0,
                          score=0)
        db.session.add(team)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/<int:team_id>/edit/', methods=('GET', 'POST'))
def edit(team_id):
    team = Teams.query.get_or_404(team_id)

    if request.method == 'POST':
        name = request.form['name']
        member1 = request.form['member1']
        member2= request.form['member2']
        member3 = request.form['member3']
        member4 = request.form['member4']
        member5 = request.form['member5']
        team.name = name
        team.member1 = member1
        team.member2 = member2
        team.member3 = member3
        team.member4 = member4
        team.member5 = member5
        db.session.add(team)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit.html', team=team)


@app.post('/<int:team_id>/delete/')
def delete(team_id):
    team= Teams.query.get_or_404(team_id)
    db.session.delete(team)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/score/', methods=('GET', 'POST'))
def score():
    teams = Teams.query.all()
    if request.method == 'POST':
        name = request.form['team-name']
        key = request.form['key']
        team = Teams.query.filter_by(name=name).first()
        if key == keys[team.current_stage]:
            team.current_stage += 1
            team.score += 10
        db.session.add(team)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('key.html', teams=teams)
