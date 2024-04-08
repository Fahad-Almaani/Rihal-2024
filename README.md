### This project build with:

    - Python 3.10.11
    - Django 5.0.3
    - database Elephantsql

# How to Run

    1 - Configure Python Environment
    2 - Install requirements.txt `pip install -r requirements.txt`
    3 - Run makemigrations `python .\manage.py makemigrations`
    4 - Run migration `python .\manage.py migrate` Note: In this step all the data from `https://cinema.stag.rihal.tech/` will be add to the database if it is not already exist

## Now the Server is running on port `8000`

    - First Register a username and password with this Url `/auth/users`
    - Next Login with this url `/auth/jwt/create` It will return access Token and refresh token you only need the access token
    - Now each time you try to access the other endpoints you need to add the access token in the headers of the request as Bearer token with Bearer as prefix like this `Authorization: Bearer <token>`

### API Endpoints

| Name              | URL                              | params and body                         |
| ----------------- | -------------------------------- | --------------------------------------- |
| Register new user | /auth/users                      | body[username,password]                 |
| login:            | /auth/jwt/create                 | body[username,password]                 |
| rate movie        | /<movie_id>/rate/                | url: movie id                           |
| all movies        | /all                             | None                                    |
| movie details     | <movie_id>/details/              | url: movie id                           |
| search for movie  | /movies/search/?search=<keyword> | url: params search keyword              |
| top 5 rated       | /top-rated-movies/               | None                                    |
| create new memory | /memory/create-memory/           | body [movie_id,title,data,story,photos] |
| all my memories   | /memory/my-memories/             | None                                    |
| memory details    | /memory/<memory id>/             | url: memory id                          |
| memory photo      | /memory/<memory_id>/photo        | url: memory id                          |
| update memory     | /memory/update/<int:pk>/         | url: memory id                          |
| delete memory     | /memory/delete/<int:pk>/         | url: memory id                          |
| top 5 words       | /memory/top-words/               | None                                    |
| urls form story   | /memory/<int:memory_id>/urls     | url: memory id                          |
| guess movie name  | /guess-movie/?query=<keyword>    | url: query                              |
| compare rating    | /rating/compare                  | None                                    |
| minimum starts    | /min-stars/                      | body[list of movies ids]                |
