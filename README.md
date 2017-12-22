# Cinemas
This script parse information about movies in Moscow cinemas.<br>
It's collect movie name, rating (kinopoisk.ru), amount of votes, cinemas in which this film is shown.

# How to install
```bash
$pip install -r requirements.txt 
```

# How to use
```bash
$python cinemas.py
```

### Output 
```bash
Load afisha...
Parsing movies from afisha...
Getting full movies info...
Тайна Коко
Рейтинг фильма(кинопоиск): 8.889
Проголосовало: 12713
Идет в 29 кинотеатрах
------------------------------
Ван Гог. С любовью, Винсент
Рейтинг фильма(кинопоиск): 8.513
Проголосовало: 3350
Идет в 7 кинотеатрах
........
```
#### Script options
optional arguments:
*  --movies_count MOVIES_COUNT<br>
                        Amount of movies that will be print(default is 10)
*  --min_in MIN_IN  <br>     Minimum amount of cinemas where movie show(default is
                        None)


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
