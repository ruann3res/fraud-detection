# Scripts

Pasta com pipelines reprodutíveis e geradores auxiliares dos notebooks.

## Pipelines principais

| Semana | Script | Finalidade |
|--------|--------|------------|
| Semana 4 | `semana_4_modelo_ic.py` | Random Forest com e sem clusters na amostra da Semana 3 |
| Semana 6 | `semana_6_modelo_mlp.py` | MLP, Regressao Logistica, calibracao, limiar e comparacao com RF |

## Geradores auxiliares

| Script | Finalidade |
|--------|------------|
| `_gen_semana5.py` | Gera os notebooks reprodutíveis da Semana 5 |
| `_gen_semana6.py` | Gera o notebook didático da Semana 6 |

## Execução

```bash
python scripts/semana_4_modelo_ic.py
python -u scripts/semana_6_modelo_mlp.py
```

O script da Semana 6 espera `resultados/semana_5_clusters_base_completa.csv` e gera:

- metricas iniciais (`semana_6_metricas_mlp.csv`) com MLPs e Regressao Logistica;
- metricas ajustadas (`semana_6_metricas_ajustadas.csv`) com calibracao e limiar otimizado;
- comparacao com Random Forest e resumo de referencia (`semana_6_resumo_referencia_rf.csv`).
