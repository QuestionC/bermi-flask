import feedparser
import flask
import html

app = flask.Flask(__name__)

feeds = {
        'funny': 'https://9gag-rss.com/api/rss/get?code=9GAGFunnyNoGif&format=2',
        'hot': 'https://9gag-rss.com/api/rss/get?code=9GAGHotNoGif&format=2',
        'trending': 'https://9gag-rss.com/api/rss/get?code=9GAGNoGif&format=2',
        'awesome': 'https://9gag-rss.com/api/rss/get?code=9GAGAwesomeNoGif&format=2'
        }


@app.route('/')
def index():
    homepage = flask.render_template('index.html', feeds=feeds)
    return homepage

@app.route('/<F>/')
def feed(F):
    if not F in feeds:
        return flask.render_template('error.html')

    # Fix escaping, title was showing up as &rdquot;Pressure ?&ldquot; for https://9gag.com/gag/amBd1z2
    d = feedparser.parse(feeds[F])
    d.feed.title = html.unescape(d.feed.title)
    for entry in d.entries:
        entry.title = html.unescape(entry.title)

    return flask.render_template('feed.html', feed=d)

