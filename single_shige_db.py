from datetime import datetime

from sqlalchemy.orm import sessionmaker

from model import Poem
from shige import fetch_poem_details
from utils import init_engine

if __name__ == "__main__":
    try:
        engine = init_engine()
        if engine is None:
            print("Failed to initialize the engine.")
            exit(1)

        url = input(
            "Please enter the single poem URL(example:https://so.gushiwen.cn/shiwenv_45c396367f59.aspx): "
        )
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
        print("Poem saved successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
