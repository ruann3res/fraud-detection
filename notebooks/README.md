# Notebooks

Esta pasta concentra os notebooks executáveis do projeto.

## Ordem Recomendada

| Semana | Notebook | Finalidade |
|--------|----------|------------|
| Semana 1 | `Semana_1_EDA_e_Preparacao.ipynb` | Análise exploratória, limpeza e preparação inicial |
| Semana 2 | `semana_2_clustering_baseline.ipynb` | K-Means, padronização, distância euclidiana e baseline |
| Semana 3 | `semana_3_comparacao.ipynb` | Comparação K-Means vs. DBSCAN, métricas e interpretação |
| Semana 4 | `semana_4_modelo_ic.ipynb` | Random Forest supervisionado na amostra com clusters |
| Semana 5 | `semana_5_validacao_completa_kmeans_dbscan.ipynb` | Random Forest na base completa com K-Means + DBSCAN |
| Semana 5 | `semana_5_validacao_completa_dbscan.ipynb` | Random Forest na base completa isolando DBSCAN |
| Semana 6 | `semana_6_modelo_mlp.ipynb` | MLP + Regressao Logistica, calibracao, limiar e comparacao com RF |

## Observações

- A base esperada é `../dados/creditcard.csv` quando o notebook é executado a partir desta pasta.
- A coluna `Class` deve ser usada apenas para análise externa dos clusters, não como entrada do agrupamento.
- A Semana 6 reutiliza `../resultados/semana_5_clusters_base_completa.csv`; execute a Semana 5 antes caso esse arquivo não exista.
