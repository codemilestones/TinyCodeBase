import pandas as pd

splits = {'dev': 'data/dev-00000-of-00001.parquet', 'test': 'data/test-00000-of-00001.parquet', 'train': 'data/train-00000-of-00001.parquet'}
df = pd.read_parquet(splits["train"])

# df to json
df.to_json("swe_bench_train.jsonl", orient="records", lines=True)