from abc import ABC

class Singleton(ABC):
    _instance = None
    
    @classmethod
    def __call__(_class, *args, **kwargs): 
        return object.__call__(_class, *args, **kwargs) if not _class._instance else _class._instance
