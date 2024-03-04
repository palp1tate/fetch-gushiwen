import requests
import re
from bs4 import BeautifulSoup


def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching HTML content: {e}")
        return None


def extract_poem_urls(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    poem_urls = []

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith("/shiwenv_"):
            full_url = f"https://so.gushiwen.cn{href}"
            poem_urls.append(full_url)

    return poem_urls


def fetch_poem_details(url):
    poem_details = {
        "name": "",
        "author": "",
        "dynasty": "",
        "content": "",
        "trans": "",
        "annotation": "",
        "appreciation": "",
        "background": ""
    }

    soup = BeautifulSoup(fetch_html(url), 'html.parser')
    title_tag = soup.find('h1')
    if title_tag:
        poem_details["name"] = title_tag.text.strip().replace("\n", "")

    source_tag = soup.find('p', class_='source')
    if source_tag:
        source_info = source_tag.find_all('a')
        if len(source_info) > 0:
            poem_details["author"] = source_info[0].text.strip().replace("\n", "")
            poem_details["dynasty"] = source_info[1].text.strip().replace("\n", "").replace("〔", "").replace("〕",
                                                                                                             "")

    content_tag = soup.find('div', class_='contson')
    if content_tag:
        poem_details["content"] = content_tag.get_text().strip().replace("\n", "")

    trans_annotation_tag = soup.find('div', class_='contyishang')
    if trans_annotation_tag:
        p_tags = trans_annotation_tag.find_all('p')
        for p_tag in p_tags:
            if '译文' in p_tag.text:
                poem_details["trans"] = p_tag.get_text().strip().replace("译文", "").replace("\n", "").replace(
                    "展开阅读全文 ∨", "")
            elif '注释' in p_tag.text:
                annotation_text = p_tag.get_text().strip().replace("注释", "").replace("\n", "")
                if "展开阅读全文 ∨" in annotation_text:
                    read_more_div = p_tag.find('a', text="展开阅读全文 ∨")
                    if read_more_div:
                        href_attr = read_more_div.get('href')
                        match = re.search(r"fanyiShow\((\d+),'([A-Z0-9]+)'\)", href_attr)
                        if match:
                            number = match.group(1)
                            string = match.group(2)
                            full_text_url = f"https://so.gushiwen.cn/nocdn/ajaxfanyi.aspx?id={number}&idjm={string}"
                            soup_ = BeautifulSoup(fetch_html(full_text_url), 'html.parser')
                            paragraphs = soup_.find('div', class_='contyishang').find_all('p')
                            full_text = "".join(p.get_text().strip() for p in paragraphs).replace(
                                "\n",
                                "").replace(
                                "▲", "")
                            match = re.compile(r"^译文(.*?)注释(.*)$", re.S).search(full_text)
                            if match:
                                poem_details["trans"] = match.group(1).strip()
                                annotation_text = match.group(2).strip()
                            else:
                                match = re.compile(r"^韵译(.*?)意译(.*?)注释(.*)$", re.S).search(full_text)
                                if match:
                                    poem_details["trans"] = "韵译:" + match.group(
                                        1).strip() + "意译:" + match.group(2).strip()
                                    annotation_text = match.group(3).strip()
                poem_details["annotation"] = annotation_text

    appreciation_divs = soup.find_all('div', class_='contyishang')
    for div in appreciation_divs:
        if div.find('h2') and ('赏析' in div.find('h2').text or '鉴赏' in div.find('h2').text):
            appreciation_paragraphs = div.find_all('p')
            appreciation_text = "".join(p.get_text().strip() for p in appreciation_paragraphs).replace("\n", "")
            if "展开阅读全文 ∨" in appreciation_text:
                read_more_div = div.find('a', text="展开阅读全文 ∨")
                if read_more_div:
                    href_attr = read_more_div.get('href')
                    match = re.search(r"shangxiShow\((\d+),'([A-Z0-9]+)'\)", href_attr)
                    if match:
                        number = match.group(1)
                        string = match.group(2)
                        full_text_url = f"https://so.gushiwen.cn/nocdn/ajaxshangxi.aspx?id={number}&idjm={string}"
                        soup_ = BeautifulSoup(fetch_html(full_text_url), 'html.parser')
                        paragraphs = soup_.find('div', class_='contyishang').find_all('p')
                        appreciation_text = "".join(p.get_text().strip() for p in paragraphs).replace("\n",
                                                                                                      "").replace(
                            "▲", "")
            poem_details["appreciation"] += appreciation_text

    background_divs = soup.find_all('div', class_='contyishang')
    for div in background_divs:
        if div.find('h2') and '创作背景' in div.find('h2').text:
            background_paragraphs = div.find_all('p')
            background_text = "".join(p.get_text().strip() for p in background_paragraphs).replace("\n",
                                                                                                   "")
            poem_details["background"] = background_text

    return poem_details


if __name__ == "__main__":
    url = input("Please enter the URL(example:https://so.gushiwen.cn/gushi/tangshi.aspx): ")
    poem_urls = []
    html_content = fetch_html(url)
    if html_content:
        poem_urls.extend(extract_poem_urls(html_content))
    else:
        print("Failed to fetch or parse HTML content.")

    for url in poem_urls:
        details = fetch_poem_details(url)
        print(details)
