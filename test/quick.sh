#!/bin/bash

# a quick test for the API: do signup and create a new movie

curl --cookie-jar ./.mycookies -d '{"fname":"tester", "lname":"boy", "email":"testing@localhost.org", "password":"aA12345678"}' -H "Content-Type: application/json" -X POST http://localhost:8100/api/signup

curl --cookie ./.mycookies -d '{"title":"My great movie"}' -H "Content-Type: application/json" -X POST http://localhost:8100/api/movies/

