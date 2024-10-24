import asyncio

import aiohttp


async def send_transcription_request():
    async with aiohttp.ClientSession() as session:
        url = "http://127.0.0.1:5000/transcribe"  # Адрес вашего Flask-сервера
        data = {"path": "audio.mp3"}  # Путь к аудиофайлу
        async with session.post(url, json=data) as response:
            if response.status == 200:
                response_data = await response.json()
                print("Request sent successfully")
                print("Received data:", response_data)
            else:
                print("Failed to send request", response.status)


async def main():
    await send_transcription_request()


if __name__ == "__main__":
    asyncio.run(main())
