from flask import Flask, render_template, request,  redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime, timedelta
import os
import random
import pandas as pd

app = Flask(__name__, static_url_path='/static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phonobot.db'
app.config['SECRET_KEY'] = b'p  093092iygf46t[pm,/z.sfeto498qd'

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    minerva_reaction = db.Column(db.String(200))
    spotify_representation = db.Column(db.String(200))

    def __repr__(self):
	    return "<Category(id={0}, minerva_reaction={1}, spotify_representation={2})>".format(self.id, self.minerva_reaction, self.spotify_representation)

class Reaction(db.Model):
    __tablename__ = 'reactions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __repr__(self):
	    return "<Reaction(id={0}, timestamp={1}, reaction_number={2})>".format(self.id, self.timestamp, self.reaction_number)

class OriginalArt(db.Model):
    __tablename__ = 'original_arts'
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(200))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __repr__(self):
	    return "<OriginalArt(id={0}, link={1}, category={2})>".format(self.id, self.link, self.category)

class Art(db.Model):
    __tablename__ = 'arts'
    id = db.Column(db.Integer, primary_key=True)
    base_name = db.Column(db.String(200))
    link = db.Column(db.String(200))

    def __repr__(self):
	    return "<Art(id={0}, timestamp={1}, link_background={2}, link_preview={3}, calculation={4}, singer={5}, track_name={6})>".format(self.id, self.timestamp, self.link_background, self.link_preview, self.calculation, self.singer, self.track_name)

class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
    link_preview = db.Column(db.String(200))
    singer = db.Column(db.String(200))
    track_name = db.Column(db.String(200))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __repr__(self):
	    return "<Song(id={0}, link_preview={1}, singer={2}, track_name={3}, category_id={4})>".format(self.id, self.link_preview, self.singer, self.link_preview, self.track_name, self.category_id)

class Dance(db.Model):
    __tablename__ = 'dances'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))
    link = db.Column(db.String(200))
    category = db.Column(db.String(200))

    def __repr__(self):
	    return "<Dance(id={0}, name={1}, link={2}, category={3})>".format(self.id, self.name, self.link, self.category)

class Character(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))
    link = db.Column(db.String(200))

    def __repr__(self):
	    return "<Character(id={0}, name={1}, link={2})>".format(self.id, self.name, self.link)

class Final(db.Model):
    __tablename__ = 'finals'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    art_id = db.Column(db.Integer, db.ForeignKey('arts.id'))
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __repr__(self):
	    return "<Final(id={0}, timestamp={1}, art={2}, song={3}, category={4})>".format(self.id, self.timestamp, self.art, self.song, self.category)


class ReactionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = Reaction

class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = Category

class OriginalArtSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = OriginalArt

class ArtSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = Art

class SongSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = Song

class DanceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = Dance

class CharacterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = Character

class FinalSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = Final


#filenames = os.listdir('static/src/moviments')

@app.route('/getsongs')
def getsongs():
    songs = Song.query.all()
    song_schema = SongSchema(many=True)
    output = song_schema.dump(songs)
    return jsonify(output)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/react')
def react():
    return render_template("reactions.html")

@app.route('/react/insert', methods = ['POST'])
def insertReaction():
    category_id = request.form['category_id']

    reaction = Reaction(category_id = category_id)

    db.session.add(reaction)
    db.session.commit()

    return 'ok'

@app.route('/getreactions', methods = ['GET'])
def getreactions():
    # count the last emojis, 25 seconds ago max
    date = datetime.now() - timedelta(seconds=25) - timedelta(hours=1)
    emojis = {'like': len(Reaction.query.filter(Reaction.timestamp >= date).filter_by(category_id=1).all()),
            'dislike': len(Reaction.query.filter(Reaction.timestamp >= date).filter_by(category_id=2).all()), 
            'agree': len(Reaction.query.filter(Reaction.timestamp >= date).filter_by(category_id=3).all()), 
            'disagree': len(Reaction.query.filter(Reaction.timestamp >= date).filter_by(category_id=4).all()), 
            'laugh': len(Reaction.query.filter(Reaction.timestamp >= date).filter_by(category_id=5).all()), 
            'wow': len(Reaction.query.filter(Reaction.timestamp >= date).filter_by(category_id=6).all())}
    return jsonify(emojis)


@app.route('/getfinal', methods = ['GET'])
def getfinal():
    # define a category
    category_id = findcategory()

    # define song
    song = random.choice(Song.query.filter_by(category_id=category_id).all())
    song_schema = SongSchema()
    output = song_schema.dump(song)
    return jsonify(output)

def findcategory():
    date = datetime.now() - timedelta(seconds=25) - timedelta(hours=1)
    emojis = [len(Reaction.query.filter(Reaction.timestamp >= date).filter_by(category_id=1).all()),
    len(Reaction.query.filter(Reaction.timestamp >= date).filter_by(category_id=2).all()), 
    len(Reaction.query.filter(Reaction.timestamp >= date).filter_by(category_id=3).all()), 
    len(Reaction.query.filter(Reaction.timestamp >= date).filter_by(category_id=4).all()), 
    len(Reaction.query.filter(Reaction.timestamp >= date).filter_by(category_id=5).all()), 
    len(Reaction.query.filter(Reaction.timestamp >= date).filter_by(category_id=6).all())]

    max = 0
    max_category = 0

    for i in range(len(emojis)):
        if emojis[i] > max:
            max = emojis[i]
            max_category = i+1

    if max>0:
        return max_category
    else:
        return random.randint(1, 6)


if __name__ == '__main__':
    app.run(debug=True)