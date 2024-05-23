from shige import fetch_poem_details

if __name__ == '__main__':
    url = input(
        "Please enter the single poem URL(example:https://so.gushiwen.cn/shiwenv_45c396367f59.aspx): "
    )
    details = fetch_poem_details(url)
    print(details)
