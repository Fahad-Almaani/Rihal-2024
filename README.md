server running on port 8000

| Name               | URL                              | params and body                         |
| ------------------ | -------------------------------- | --------------------------------------- |
| Register new user: | /auth/users                      | body[username,password]                 |
| login:             | /auth/jwt/create                 | body[username,password]                 |
| rate moview        | /<movie_id>/rate/                | url: moview id                          |
| all movies         | /all                             | None                                    |
| movie details      | <movie_id>/details/              | url: moview id                          |
| search for movie   | /movies/search/?search=<keyword> | url: parms search keyword               |
| top 5 rated        | /top-rated-movies/               | None                                    |
| create new memeory | /memory/create-memory/           | body [movie_id,title,data,story,photos] |
| all my memories    | /memory/my-memories/             | None                                    |
| memory details     | /memory/<memory id>/             | url: memory id                          |
| memory photo       | /memory/<memory_id>/photo        | url: memory id                          |
| update memeory     | /memory/update/<int:pk>/         | url: memory id                          |
| delete memeory     | /memory/delete/<int:pk>/         | url: memory id                          |
| top 5 words        | /memory/top-words/               | None                                    |
| urls form story    | /memory/<int:memory_id>/urls     | url: memory id                          |
| guess movie name   | /guess-movie/?query=<keyword>    | url: query                              |
| compare rating     | /rating/compare                  | None                                    |
| minmum starts      | /min-stars/                      | body[list of movies ids]                |