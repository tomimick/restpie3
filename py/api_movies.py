#!/usr/bin/python
# -*- coding: utf-8 -*-

# api.py: REST API for movies
#   - this module is just demonstrating how to handle basic CRUD
#   - GET operations are available for visitors, editing requires login

# Author: Tomi.Mickelsson@iki.fi

from flask import request, jsonify, g
from playhouse.shortcuts import dict_to_model, update_model_from_dict

import db
import util
from webutil import app, login_required, get_myself

import logging
log = logging.getLogger("api.movies")


@app.route('/api/movies/', methods = ['GET'])
def movie_query():
    """Returns list of movies that match the given search criteria: page, limit,
    search, creator."""

    input = request.args
    page = input.get("page")
    limit = input.get("limit")
    s = input.get("search")
    u = input.get("creator")

    movielist = db.query_movies(search=s, creator=u, page=page, limit=limit)

    return jsonify(movielist), 200


@app.route('/api/movies/<id>', methods = ['GET'])
def movie_get(id):
    """Returns a single movie, or 404."""

    m = db.get_movie(id)
    return jsonify(m), 200


@app.route('/api/movies/', methods = ['POST'])
@login_required(role='editor')
def movie_create():
    """Creates a movie and returns it."""

    input = request.json
    input.pop("id", 0) # ignore id if given, is set by db

    m = dict_to_model(db.Movie, input)
    m.modified = m.created = util.utcnow()
    m.creator = get_myself()
    m.save()

    return jsonify(m), 201


@app.route('/api/movies/<id>', methods = ['PUT'])
@login_required(role='editor')
def movie_update(id):
    """Updates a movie and returns it."""

    input = request.json
    # don't update created/creator-fields
    input.pop("created", 0)
    input.pop("creator", 0)

    m = db.get_movie(id)
    update_model_from_dict(m, input)
    m.modified = util.utcnow()
    m.save()

    return jsonify(m), 200


@app.route('/api/movies/<id>', methods = ['DELETE'])
@login_required(role='editor')
def movie_delete(id):
    """Deletes a movie."""

    m = db.get_movie(id)
    m.delete_instance()

    return jsonify(m), 200

