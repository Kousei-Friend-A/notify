import requests
import random
import cv2


def get_json(url):
    print("Getting json", url)
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


def convertToScreenshot(url):
    host = "/".join(url.split("/")[:-1]) + "/"
    r = requests.get(url)
    lines = r.text.split("\n")
    m3u8 = []
    for line in lines:
        line = line.strip(" \n")
        if line.endswith(".m3u8"):
            m3u8.append(host + line)
    print("Total m3u8 files: ", len(m3u8))
    url = m3u8[-1]

    host = "/".join(url.split("/")[:-1]) + "/"
    r = requests.get(url)
    lines = r.text.split("\n")

    ts = []
    for line in lines:
        line = line.strip(" \n")
        if line.endswith(".ts"):
            ts.append(host + line)

    total = len(ts)
    print("Total ts files: ", total)

    x = total // 4
    ts = ts[x : x * 3]
    print("Total ts files: ", len(ts))

    file = random.choice(ts)
    print("Random ts file: ", file)

    print("Downloading ts file...")
    r = requests.get(file)
    with open("tmp.ts", "wb") as f:
        f.write(r.content)

    print("Getting screenshot...")
    cam = cv2.VideoCapture("./tmp.ts")
    length = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_no = length // 2
    currentframe = 0

    while True:
        # reading from frame
        ret, frame = cam.read()

        if ret:
            if currentframe == frame_no:
                cv2.imwrite("./ss.jpg", frame)
                break
            currentframe += 1
        else:
            break

    cam.release()
    cv2.destroyAllWindows()
    print("Screenshot saved!")
    return "./ss.jpg"


def get_screenshot(id, ep):
    url = f"https://api.peaceful-wolf.workers.dev/episode/{id}-episode-{ep}"
    data = get_json(url)
    url = data["results"]["stream"]["sources"][0]["file"]
    return convertToScreenshot(url)
