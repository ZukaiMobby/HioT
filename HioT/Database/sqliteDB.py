from sqlalchemy import create_engine
from sqlalchemy.orm import registry, sessionmaker, Session
from HioT.Plugins.get_config import global_config
from HioT.Plugins.get_logger import logger

database_path = "sqlite:///./" + \
    global_config['database_file_path']+'/' + \
    global_config['database_file_name']


engine = create_engine(database_path,connect_args={"check_same_thread": False})
mapper_registry = registry()
OrmBase = mapper_registry.generate_base()
Sessioned = sessionmaker(bind=engine, autocommit=False, autoflush=False,)
session:Session = Sessioned()

    