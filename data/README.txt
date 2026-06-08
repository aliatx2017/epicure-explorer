Epicure embeddings -- supplementary bundle

This archive contains the three trained Epicure embeddings (Cooc, Core,
Chem), each a 300-dimensional ingredient embedding over a shared
canonical vocabulary of 1,790 ingredients.

Files
-----
  epicure_cooc.csv   1,790 rows; columns: node_id, name, dim_0 ... dim_299
  epicure_core.csv   1,790 rows; columns: node_id, name, dim_0 ... dim_299
  epicure_chem.csv   1,790 rows; columns: node_id, name, dim_0 ... dim_299
  vocab.csv          1,790 rows; columns: name, node_id_cooc, node_id_core, node_id_chem
  README.txt         this file

Notes
-----
- All three embeddings share the same canonical ingredient vocabulary
  (1,790 names) but the internal node_id differs across runs because
  the training-graph numbering is model-specific.  Use vocab.csv to
  cross-reference an ingredient name to each model's node_id, or join
  the three CSVs on the `name` column.
- The original training runs also produced compound-node embeddings
  (Core/Chem) used internally by the typed metapath2vec walks; those
  are not part of the paper's analytical scope and are omitted from
  this bundle.  Available from the authors on request.
- Embeddings are L2-normalised in all reported analyses, but the CSV
  values here are the raw skip-gram outputs; apply your own
  normalisation as needed.
- Float values are written with 6 decimal places.
- See paper/supplement.tex (Reproducibility appendix) and the
  paper/supplement/csv/README.md for the rest of the supplementary
  data bundle.

Quick load (pandas):
    >>> import pandas as pd
    >>> df = pd.read_csv('epicure_core.csv')
    >>> X = df[[f'dim_{i}' for i in range(300)]].to_numpy()
    >>> names = df['name'].tolist()
