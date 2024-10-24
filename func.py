import eventlet

eventlet.monkey_patch()

import asyncio
import logging

from faster_whisper import WhisperModel
from flask import Flask, jsonify, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, async_mode="eventlet")


@socketio.on("connect")
def handle_connect():
    print("Client connected")


@app.route("/transcribe", methods=["POST"])
def req():
    data = request.json["path"]
    asyncio.run(transcribe(data))
    return jsonify({"message": "Processing..."})


async def transcribe(path):
    model_size = "tiny"
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("faster_whisper")

    segments, info = model.transcribe(path, beam_size=5)
    res = ""
    done = 0

    for segment in segments:
        start_t = segment.start
        end_t = segment.end
        res += segment.text + "\n"
        done += end_t - start_t
        data = {"percentage": done / info.duration}
        print(data)
        await send(data)


async def send(data):
    print(data)
    socketio.emit("progress", data)


if __name__ == "__main__":
    import logging
    import os

    log = logging.getLogger("werkzeug")
    log.disabled = True
    os.environ["WERKZEUG_RUN_MAIN"] = "true"

    socketio.run(app, host="0.0.0.0", port=5000, debug=False)
