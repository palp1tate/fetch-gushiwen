import os
from shige import fetch_poem_details

file_path = "poems.csv"

if __name__ == "__main__":
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(
                "name,author,dynasty,content,trans,annotation,appreciation,background\n"
            )
    url = input(
        "Please enter the URL(example:https://so.gushiwen.cn/gushi/tangshi.aspx): "
    )

    details = fetch_poem_details(url)
    with open(file_path, "a", encoding="utf-8") as f:
        print(f"Writing details for poem: {details['name']}")
        for key in details:
            details[key] = details[key].replace("\xa0", "")
        f.write(
            f"{details['name']},{details['author']},{details['dynasty']},{details['content']},{details['trans']},{details['annotation']},{details['appreciation']},{details['background']}\n"
        )
