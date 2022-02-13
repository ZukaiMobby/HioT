from sqlalchemy import create_engine
from sqlalchemy.orm import registry, sessionmaker, Session
from HioT.Plugins.get_config import global_config
from HioT.Plugins.get_logger import logger
import os.path

with logger:
    logger.debug("数据库程序执行路径："+os.path.abspath("__file__"))
    database_path = "sqlite:///./" + \
        global_config['database_file_path']+'/' + \
        global_config['database_file_name']+'?check_same_thread=False'

    logger.debug(f"数据库完整路径: {database_path}")

    engine = create_engine(database_path)
    mapper_registry = registry()
    OrmBase = mapper_registry.generate_base()
    Sessioned = sessionmaker(bind=engine, autocommit=False, autoflush=False,)
    session:Session = Sessioned()
    logger.debug(f"ORM Session instance created: {session}")

    