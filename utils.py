import yaml
from sqlalchemy import create_engine


def load_configuration(file_path: str) -> dict:
    try:
        with open(file_path, "r") as f:
            return yaml.safe_load(f)
    except Exception as exc:
        raise Exception(f"Failed to load configuration from {file_path}: {exc}")


def init_engine():
    try:
        conf = load_configuration("./config.yaml")
        mysql_conf = conf["mysql"]

        dsn = (
            f"mysql+mysqlconnector://{mysql_conf['user']}:{mysql_conf['password']}@"
            f"{mysql_conf['host']}:{mysql_conf['port']}/{mysql_conf['database']}"
        )

        engine = create_engine(dsn, pool_recycle=3600, future=True)
        return engine
    except Exception as e:
        print(f"Error occurred while initializing the engine: {e}")
        return None
