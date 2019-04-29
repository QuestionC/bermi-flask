import feedparser
import flask
import html
import time

app = flask.Flask(__name__)

feeds = { # Key: (URL, cache, timestamp)
        'funny': ('https://9gag-rss.com/api/rss/get?code=9GAGFunnyNoGif&format=2', None, None),
        'hot': ('https://9gag-rss.com/api/rss/get?code=9GAGHotNoGif&format=2', None, None),
        'trending': ('https://9gag-rss.com/api/rss/get?code=9GAGNoGif&format=2', None, None),
        'awesome': ('https://9gag-rss.com/api/rss/get?code=9GAGAwesomeNoGif&format=2', None, None)
        }


@app.route('/')
def index():
    homepage = flask.render_template('index.html', feeds=feeds)
    return homepage

@app.route('/<F>/')
def feed(F):
    if not F in feeds:
        return flask.render_template('index.html', feeds=feeds)


    url, cache, timestamp = feeds[F]
    now = time.time()

    # Recache
    if timestamp == None or now - timestamp > 10: # every 10 seconds
        # print("Cache Miss")
        d = feedparser.parse(url)

        # Fix escaping, title was showing up as &rdquot;Pressure ?&ldquot; for https://9gag.com/gag/amBd1z2
        d.feed.title = html.unescape(d.feed.title)
        for entry in d.entries:
            entry.title = html.unescape(entry.title)
    
        cache = flask.render_template('feed.html', feed=d)
        timestamp = now
        feeds[F] = (url, cache, timestamp)
    else:
        # print("Cache Hit")
        pass

    return cache
