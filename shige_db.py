from datetime import datetime

from sqlalchemy.orm import sessionmaker

from model import Poem
from shige import fetch_html, extract_poem_urls, fetch_poem_details
from utils import init_engine

if __name__ == "__main__":
    try:
        engine = init_engine()
        if engine is None:
            print("Failed to initialize the engine.")
            exit(1)

        url = input(
            "Please enter the URL(example:https://so.gushiwen.cn/gushi/tangshi.aspx): "
        )
        poem_urls = []
        html_content = fetch_html(url)
        if html_content:
            poem_urls.extend(extract_poem_urls(html_content))
        else:
            print("Failed to fetch or parse HTML content.")
            exit(1)

        for url in poem_urls:
            details = fetch_poem_details(url)
            new_session = sessionmaker(engine)
            with new_session() as session:
                try:
                    poem = Poem(
                        name=details["name"],
                        author=details["author"],
                        dynasty=details["dynasty"],
                        content=details["content"],
                        trans=details["trans"],
                        annotation=details["annotation"],
                        appreciation=details["appreciation"],
                        background=details["background"],
                        created_at=datetime.now(),
                    )
                    session.add(poem)
                    session.commit()
                    print(f"Saved details for poem: {details['name']}")
                except Exception as e:
                    session.rollback()
                    print(f"An error occurred while saving the poem: {e}")
        print("All poems saved successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
