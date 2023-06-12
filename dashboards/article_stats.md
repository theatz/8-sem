## Статистика по количетсву статей в день

![Количество статей в день](images/article_stats.png)

```{
  "aggs": {
    "0": {
      "date_histogram": {
        "field": "date",
        "calendar_interval": "1d",
        "time_zone": "Europe/Moscow"
      },
      "aggs": {
        "1": {
          "cardinality": {
            "field": "md5"
          }
        }
      }
    }
  },
  "size": 0,
  "script_fields": {},
  "stored_fields": [
    "*"
  ],
  "runtime_mappings": {},
  "query": {
    "bool": {
      "must": [],
      "filter": [
        {
          "range": {
            "date": {
              "format": "strict_date_optional_time",
              "gte": "now-6mon"
            }
          }
        }
      ],
      "should": [],
      "must_not": []
    }
  }
}```