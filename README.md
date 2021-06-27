# mongoengine-poc
Flask and MongoEngine in Python.

---
GET
http://127.0.0.1:5000/movies

---
GET
http://127.0.0.1:5000/movies/60d692d5c1c993c704a2d4f3

---
POST
http://127.0.0.1:5000/movies

Body: {"title": "John Wick", "year": 2014, "rated": "5"}

---
POST
http://127.0.0.1:5000/movies-embed

---
POST
http://127.0.0.1:5000/directors

Body: {"name": "James Cameron", "age": 57}

---
PUT
http://127.0.0.1:5000/movies/60d692d5c1c993c704a2d4f3

Body: {"year": 2016}

---
PUT
http://127.0.0.1:5000/movies-many/2016

Body: {"year": 2010}


