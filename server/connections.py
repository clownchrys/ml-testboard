import os
from typing import List, Dict, Any
from pyhive import presto


class PrestoConnection:
    conn = presto.connect(
        host=os.environ["PRESTO_HOST"],
        port=int(os.environ["PRESTO_PORT"]),
        catalog=os.environ["PRESTO_CATALOG"],
        schema=os.environ["PRESTO_SCHEMA"]
    )

    def __enter__(self):
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()

    @classmethod
    def disconnect(cls):
        cls.conn.close()


class PrestoExecutor:
    @classmethod
    def execute(cls, query: str, include_rowid: bool = False) -> List[Dict[str, Any]]:
        with PrestoConnection() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            data = map(lambda row: dict(zip(columns, row)), cursor.fetchall())
        if include_rowid:
            data = map(lambda index_row: dict(rowid=index_row[0], **index_row[1]), enumerate(data, 1))
        return list(data)

