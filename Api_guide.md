
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