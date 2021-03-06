from flask import Flask, make_response, render_template, request
from generator import generate
from random import randint
from re import match
import os
import psycopg2
import urlparse


# set up database
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])
conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
cur = conn.cursor()

app = Flask(__name__)


@app.route('/')
def homepage():
    default_seed = match(r'^0x([0-9a-f]+)L?$', hex(randint(0, 2**63))).group(1)
    return render_template('main.html', default_seed=default_seed)


@app.route('/randomize')
def randomize():
    seed = request.args.get('seed')

    if (match(r'^[0-9a-f]+$', seed) is None):
        return ("Bad Request", 400, [])

    cur.execute("SELECT bin FROM seeds WHERE seed = %s", (seed,))
    row = cur.fetchone()
    if (row is None):
        filename = generate(seed)
        file = open(filename, 'rb').read()
        cur.execute("""INSERT INTO
                       seeds(seed, downloads, created_at, last_download, bin)
                       VALUES(%s, 1, now(), now(), %s)""",
                    (seed, psycopg2.Binary(file)))
    else:
        file = row[0]
        cur.execute("""UPDATE seeds
                       SET downloads = downloads + 1,
                           last_download = now()
                       WHERE seed = %s""", (seed,))

    conn.commit()

    response = make_response(str(file))
    response.headers['Content-Disposition'] = "attachment; filename=metroid-{0}.nes".format(seed)
    response.headers['Content-Type'] = 'vnd.nintendo.nes.rom'
    return response


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
