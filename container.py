from dependency_injector import containers, providers
from services import LdesService
from services import PageFragmentation
from storage import PostgresDB, PostgresStorageProvider
from tools.ldes_cache import LdesCache

class Container(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["config.yml"])
    db = providers.Singleton(PostgresDB, db_url=config.db.postgres_url)
    
    storage_provider = providers.Factory(
        PostgresStorageProvider,
        session_factory=db.provided.session,
    )

    ldes_service = providers.Factory(
        LdesService,
        storage_provider = storage_provider,
        base_uri = config.ldes.base_uri
    )

    page_fragmentation = providers.Factory(
        PageFragmentation,
        storage_provider = storage_provider
    )

    ldes_cache = providers.Singleton(
        LdesCache,
        max_entries = config.cache.max_entries, 
        cache_dir = config.cache.directory
    )

    