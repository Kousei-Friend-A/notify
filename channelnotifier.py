from pyrogram import Client
import requests
import json
from utils.postgen import get_post


print("Starting Bot")

bot = Client(
    "bot",
    27332239,
    "2fed2c90672125f4c6f42316eed6a837",
    bot_token="7246024051:AAH5BVbCDlUQCysDLqcvbtVrK41ju03Rgco",
)
bot.start()

print("Bot started")


def send_message(x, admin=False):
    if admin:
        bot.send_message("Hashcatz", x, disable_web_page_preview=True)
    else:
        print("Sending message...")
        img, text = get_post(x[0], x[1])
        bot.send_photo("AiringAnime_Alerts", img, text)


def get_json(url):
    i = 0
    while i < 5:
        i += 1
        try:
            r = requests.get(url)
            data = r.json()
            return data
        except:
            print("Retrying", i, url)
            continue


def get_aired_ep(anime):
    print("Getting aired " + anime)

    url = "https://api.peaceful-wolf.workers.dev/anime/" + anime
    data = get_json(url)
    ep = data["results"]["episodes"][-1][1]
    print("Aired ep " + ep)
    return ep, data["results"]


def get_latest():
    url = "https://api.peaceful-wolf.workers.dev/recent/1"
    data = get_json(url)
    return data["results"]


def main():
    with open("data.json") as json_file:
        data = json.load(json_file)

    print("Getting latest anime...")
    latest: list = get_latest()
    latest.reverse()

    x = None

    for pos in range(len(latest)):
        try:
            anime = latest[pos]
            x = anime["id"].split("-episode-")
            anime_id = x[0]
            ep_id = anime["id"]
            print("Checking " + ep_id)

            if anime_id not in data["channel"]:
                data["channel"][anime_id] = ep_id
                send_message((ep_id, anime["title"]))
            else:
                if data["channel"][anime_id] != ep_id:
                    data["channel"][anime_id] = ep_id
                    send_message((ep_id, anime["title"]))
        except Exception as e:
            print(e)
            send_message(
                "channel " + str(e) + "\n\n" + str(anime) + "\n\n" + str(x), admin=True
            )
            continue

    with open("data.json", "w") as outfile:
        json.dump(data, outfile)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        send_message(str(e), admin=True)
