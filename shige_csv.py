import os
from shige import fetch_html, extract_poem_urls, fetch_poem_details

if __name__ == "__main__":
    if not os.path.exists("poem.csv"):
        with open("poem.csv", "w", encoding="utf-8") as f:
            f.write(
                "name,author,dynasty,content,trans,annotation,appreciation,background\n"
            )
    url = input(
        "Please enter the URL(example:https://so.gushiwen.cn/gushi/tangshi.aspx): "
    )
    poem_urls = []
    html_content = fetch_html(url)
    if html_content:
        poem_urls.extend(extract_poem_urls(html_content))
    else:
        print("Failed to fetch or parse HTML content.")

    for url in poem_urls:
        details = fetch_poem_details(url)
        with open("poem.csv", "a", encoding="utf-8") as f:
            print(f"Writing details for poem: {details['name']}")
            for key in details:
                details[key] = details[key].replace("\xa0", "")
            f.write(
                f"{details['name']},{details['author']},{details['dynasty']},{details['content']},{details['trans']},{details['annotation']},{details['appreciation']},{details['background']}\n"
            )
