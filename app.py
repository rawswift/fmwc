import datetime
from flask import Flask, render_template, jsonify
from mpd import MPDClient

app = Flask(__name__)

@app.route("/")
def index():
    client = MPDClient()
    client.connect("localhost", 6600)

    # Get song(s) in the playlist
    playlist = client.playlistinfo()

    # Get current song
    current = client.currentsong()

    # Get status
    status = client.status()

    client.close()
    client.disconnect()

    # Create empty (playlist) list
    pl = []

    for song in playlist:
            s = {}

            # Format time 00:00:00
            s["time"] = str(datetime.timedelta(seconds=float(song["time"])))

            if song.has_key("title") and not song["title"] is None:
                s["title"] = song["title"]
            else:
                s["title"] = "Unknown"

            if song.has_key("artist") and not song["artist"] is None:
                s["artist"] = song["artist"]
            else:
                s["artist"] = "Unknown"

            if song.has_key("album") and not song["album"] is None:
                s["album"] = song["album"]
            else:
                s["album"] = "Unknown"
            
            pl.append(s)

            progress = 0
            if current.has_key("time") and status.has_key("elapsed"):
                time = int(current['time']);
                elapsed = float(status['elapsed'])
                progress = (elapsed/time)*100


    return render_template("index.html", playlist=pl, current=current, status=status, progress=progress)

@app.route("/dev")
def dev():
    client = MPDClient()
    client.connect("localhost", 6600)

    # Get song(s) in the playlist
    playlist = client.playlistinfo()

    # Get current song
    current = client.currentsong()

    # Get status
    status = client.status()

    # Get stats
    stats = client.stats()

    client.close()
    client.disconnect()

    # Create empty (playlist) list
    pl = []

    for song in playlist:
            s = {}

            # Format time 00:00:00
            s["time"] = str(datetime.timedelta(seconds=float(song["time"])))

            if song.has_key("title") and not song["title"] is None:
                s["title"] = song["title"]
            else:
                s["title"] = "Unknown"

            if song.has_key("artist") and not song["artist"] is None:
                s["artist"] = song["artist"]
            else:
                s["artist"] = "Unknown"

            if song.has_key("album") and not song["album"] is None:
                s["album"] = song["album"]
            else:
                s["album"] = "Unknown"
            
            pl.append(s)

    return render_template("dev.html", playlist=pl, current=current, status=status, stats=stats)

@app.route("/play")
def play():
    client = MPDClient()
    client.connect("localhost", 6600)

    # Play track
    client.play()

    client.close()
    client.disconnect()

    return jsonify(ok=True)

@app.route("/pause")
def pause():
    client = MPDClient()
    client.connect("localhost", 6600)

    # Pause track
    client.pause()

    client.close()
    client.disconnect()

    return jsonify(ok=True)    

@app.route("/next")
def next():
    client = MPDClient()
    client.connect("localhost", 6600)

    # Next track
    client.next()

    client.close()
    client.disconnect()

    return jsonify(ok=True)

@app.route("/previous")
def previous():
    client = MPDClient()
    client.connect("localhost", 6600)

    # Previous track
    client.previous()

    client.close()
    client.disconnect()

    return jsonify(ok=True)

@app.route("/stop")
def stop():
    client = MPDClient()
    client.connect("localhost", 6600)

    # Stop track
    client.stop()

    client.close()
    client.disconnect()

    return jsonify(ok=True)

@app.route("/togglerepeat")
def togglerepeat():
    client = MPDClient()
    client.connect("localhost", 6600)

    # Get status
    status = client.status()

    repeat = int(status['repeat'])
    if repeat == 1:
        client.repeat(0)
    else:
        client.repeat(1)

    client.close()
    client.disconnect()

    return jsonify(ok=True)

@app.route("/togglerandom")
def togglerandom():
    client = MPDClient()
    client.connect("localhost", 6600)

    # Get status
    status = client.status()

    random = int(status['random'])
    if random == 1:
        client.random(0)
    else:
        client.random(1)

    client.close()
    client.disconnect()

    return jsonify(ok=True)

@app.route("/poll")
def poll():
    client = MPDClient()
    client.connect("localhost", 6600)

    # Get current song
    current = client.currentsong()

    # Get status
    status = client.status()
    elapsed = float(status['elapsed'])

    client.close()
    client.disconnect()

    return jsonify(artist=current['artist'], title=current['title'], time=current['time'], elapsed=elapsed, repeat=status['repeat'], random=status['random'], volume=status['volume'])

@app.route("/volume/<value>")
def volume(value):
    client = MPDClient()
    client.connect("localhost", 6600)

    client.setvol(value)

    client.close()
    client.disconnect()

    return jsonify(ok=True, value=value)

if __name__ == "__main__":
    app.debug = True
    app.run()
