from io import BytesIO

from flask import Flask, jsonify, request
from flask_mongoengine import MongoEngine
from flask.helpers import send_file

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/moviesdb'
}

db = MongoEngine(app)


class Imdb(db.EmbeddedDocument):
    imdb_id = db.StringField()
    rating = db.DecimalField()
    votes = db.IntField()


class Director(db.DynamicDocument):
    pass


class Cast(db.DynamicEmbeddedDocument):
    pass


class Movie(db.Document):
    title = db.StringField(required=True)
    year = db.IntField()
    rated = db.StringField()
    director = db.ReferenceField(Director)
    cast = db.EmbeddedDocumentListField(Cast)
    poster = db.FileField()
    imdb = db.EmbeddedDocumentField(Imdb)


@app.route('/movies')
def get_movies():
    # Get all objects.
    # movies = Movie.objects()
    # Get paginated objects.
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    movies = Movie.objects.paginate(page=page, per_page=limit)
    return jsonify([movie.to_dict() for movie in movies.items]), 200


@app.route('/movies/<id>')
def get_one_movie(id: str):
    movie = Movie.objects.first_or_404(id=id)
    return jsonify(movie), 200


@app.route('/movies/', methods=['POST'])
def add_movie():
    body = request.get_json()
    movie = Movie(**body).save()
    return jsonify(movie), 201


@app.route('/movies-embed/', methods=['POST'])
def add_movie_embed():
    # Created Imdb object.
    imdb = Imdb(imdb_id='1234mov', rating=4.2, votes=7.9)
    body = request.get_json()
    # Add object to mivie and save.
    movie = Movie(imdb=imdb, **body).save()
    return jsonify(movie), 201


@app.route('/director/', methods=['POST'])
def add_dir():
    body = request.get_json()
    director = Director(**body).save()
    return jsonify(director), 201


@app.route('/movies/<id>', methods=['PUT'])
def update_movie(id):
    body = request.get_json()
    movie = Movie.objects.get_or_404(id=id)
    movie.update(**body)
    return jsonify(str(movie.id)), 200


@app.route('/movies-many/<year>', methods=['PUT'])
def update_movie_many(year):
    body = request.get_json()
    movies = Movie.objects(year=year)
    movies.updates(**body)
    return jsonify([str(movie.id) for movie in movies]), 200


@app.route('/movies/<id>', methods=['DELETE'])
def delete_movie(id):
    movie = Movie.objects.get_or_404(id=id)
    movie.delete()
    return jsonify(str(movie.id)), 200


@app.route('/movies/delete-by-year/<year>')
def delete_movie_by_year(year):
    movies = Movie.objects(year=year)
    movies.delete()
    return jsonify([str(movie.id) for movie in movies]), 200


@app.route('/movies-with-poster', methods=['POST'])
def add_movie_with_image():
    image = request.files['file']
    movie = Movie(title='Movie with poster', year=2021)
    movie.poster.put(image, filename=image.filename)
    movie.save()
    return jsonify(movie), 201


@app.route('/movies-with-poster/<id>', methods=['GET'])
def get_movie_image(id):
    movie = Movie.objects.get_or_404(id=id)

    image = movie.poster.read()
    content_type = movie.poster.content_type
    filename = movie.poster.filename

    return send_file(
        BytesIO(image),
        attachment_filename=filename,
        mimetype=content_type
    ), 200


@app.route('/movies-with-poster/<id>', methods=['DELETE'])
def delete_movie_image(id):
    movie = Movie.objects.get_or_404(id=id)
    movie.poster.delete()
    movie.delete()
    response = jsonify({
        'message': 'Movie with poster deleted: ' + id,
        'status': 204
    })
    return response, 204


if __name__ == '__main__':
    app.run(debug=True)
