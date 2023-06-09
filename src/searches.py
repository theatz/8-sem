from typing import Any


def match_query(field: str, value: Any) -> dict:
    return {
        "query": {
            "match": {
                field: value
            }
        }
    }


def find_duplicates(field: str) -> dict:
    return {
        "size": 0,
        "aggs": {
            f"duplicate_{field}": {
                "terms": {
                    "field": field,
                    "min_doc_count": 2,
                    "size": 10
                },
                "aggs": {
                    "duplicate_docs": {
                        "top_hits": {
                            "size": 10
                        }
                    }
                }
            }
        }
    }
