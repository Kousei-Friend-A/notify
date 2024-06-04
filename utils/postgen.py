from utils.screenshot import get_screenshot


def get_post(ep, title):
    id, ep_num = ep.split("-episode-")
    url = f"https://animeotakunet.vercel.app/episode?anime={id}&episode={ep_num}"
    img = get_screenshot(id, ep_num)

    text = f"""
📌 **New Release**
**{title} - Episode {ep_num}**

➤ **Watch Now :** {url}
"""
    return img, text
