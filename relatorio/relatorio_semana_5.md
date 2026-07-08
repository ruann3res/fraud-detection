# Relatorio Semana 5 - Inteligencia Computacional I

## 1. Definicao da tarefa de Inteligencia Computacional

A tarefa da Semana 5 foi validar, na **populacao completa** de transacoes, se os agrupamentos obtidos com K-Means e DBSCAN agregam valor consistente ao classificador supervisionado de fraude construido na Semana 4.

Na Semana 4, o Random Forest foi treinado sobre uma amostra estratificada de 15.000 registros (25 fraudes), usando rotulos de cluster gerados na Semana 3 sobre a mesma amostra. A conclusao preliminar foi de que os clusters eram informativos do ponto de vista exploratorio, mas ainda nao comprovavam ganho estavel no classificador — hipotese limitada pela baixa quantidade de fraudes na amostra.

A Semana 5 responde a essa limitacao ao:

- gerar os rotulos de K-Means e DBSCAN sobre **toda a base** (`dados/creditcard.csv`);
- treinar e avaliar Random Forest com a mesma configuracao da Semana 4;
- isolar o efeito do DBSCAN (sem K-Means) em um segundo experimento;
- comparar os resultados com o baseline da Semana 4 (15k) e com o baseline supervisionado na base completa.

O alvo continua sendo a coluna `Class` (`0` = legitima, `1` = fraude). A acuracia nao foi usada como metrica principal. Foram adotadas AUC-ROC, Average Precision, Recall, Precision, F1-Score, matriz de confusao e validacao cruzada estratificada com 5 folds.

## 2. Escolha justificada da tecnica

Manteve-se o **Random Forest** como tecnica supervisionada, com os mesmos hiperparametros da Semana 4:

```python
RandomForestClassifier(
    n_estimators=200,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1,
)
```

A escolha se mantem adequada porque:

- permite comparar modelos com e sem clusters de forma direta e reprodutivel;
- lida bem com relacoes nao lineares entre `V1`-`V28`, `Time` e `Amount`;
- trata o desbalanceamento via `class_weight='balanced'`;
- expoe a importancia das features, incluindo variaveis derivadas de cluster.

Para o agrupamento nao supervisionado, reutilizaram-se K-Means (`k=6`, `StandardScaler`) e DBSCAN (`RobustScaler`, `min_samples=60`), conforme Semanas 2 e 3, com recalibracao do `eps` do DBSCAN para viabilidade computacional na base completa.

## 3. Preparacao dos dados para o modelo

### 3.1 Base utilizada

Foi carregado `dados/creditcard.csv` **sem amostragem**. Apos remocao de 1.081 duplicatas (mesma decisao das Semanas 1 e 2), a populacao final ficou com:

- **283.726** transacoes;
- **473** fraudes;
- taxa de fraude de **0,1667%**.

Isso representa um aumento de ~19 vezes no numero de fraudes disponiveis em relacao a amostra de 15.000 da Semana 4 (25 fraudes) e um conjunto de teste estratificado com **95 fraudes** (20% de 473), muito mais robusto que as 5 fraudes do teste da Semana 4.

### 3.2 Clustering na base completa

As 30 features de agrupamento foram `V1`-`V28`, `Time` e `Amount`. A coluna `Class` ficou **fora** do treino dos algoritmos de clustering.

| Algoritmo | Escalonamento | Parametros | Resultado |
|---|---|---|---|
| K-Means | `StandardScaler` | `k=6`, `n_init=10`, `random_state=42` | 6 clusters; ajuste em ~1,3s |
| DBSCAN | `RobustScaler` | `eps=2,5`, `min_samples=60` | 17 clusters densos; 75.217 pontos de ruido (26,51%) |

**Recalibracao do DBSCAN.** O `eps=8,3063` da Semana 3 (calibrado na amostra de 15.000) tornou-se inviavel na base completa: a vizinhanca media de cada ponto passou a ~210.000 registros, estourando a memoria do algoritmo. Foi recalculada a curva k-distance (60o vizinho) sobre as 283.726 transacoes e adotado `eps=2,5`, valor que manteve o DBSCAN executavel (~28s) preservando sinal de anomalia.

Concentracao de fraude no ruido DBSCAN (`cluster_dbscan == -1`):

- **440 de 473** fraudes (93,02%) aparecem como ruido;
- taxa de fraude na regiao de ruido: **0,585%** (vs. 0,1667% na base);
- a regiao de ruido contem centenas de milhares de transacoes legitimas, limitando a precisao isolada do sinal.

### 3.3 Features de cluster para o Random Forest

**Notebook 1 (K-Means + DBSCAN):**

- `cluster_kmeans`: categorica, one-hot (6 grupos);
- `dbscan_ruido`: binaria (`1` = ruido/anomalia).

**Notebook 2 (apenas DBSCAN):**

Foram comparadas duas representacoes:

| Representacao | AP media (CV) | AUC-ROC media (CV) | n features |
|---|---:|---:|---:|
| `dbscan_ruido` (binaria) | **0,8386** | 0,9587 | 32 |
| `cluster_dbscan` (categorica one-hot) | 0,8370 | 0,9545 | 48 |

Escolheu-se **`dbscan_ruido` (binaria)** por melhor Average Precision na validacao cruzada, com menos features.

As variaveis originais do modelo foram `Time`, `Amount` e `V1`-`V28`. Split estratificado 80/20 (`random_state=42`) e validacao cruzada estratificada de 5 folds.

## 4. Construcao dos modelos

Foram construidos e comparados **tres modelos** na base completa, alem dos dois da Semana 4 na amostra de 15k:

| Modelo | Features | Objetivo |
|---|---|---|
| Random Forest sem clusters | 30 originais | Baseline supervisionado na base completa |
| Random Forest K-Means + DBSCAN | 30 originais + one-hot de cluster | Modelo hibrido (Notebook 1) |
| Random Forest apenas DBSCAN | 30 originais + `dbscan_ruido` | Isolar efeito do DBSCAN (Notebook 2) |

Entregaveis reprodutiveis:

```text
notebooks/semana_5_validacao_completa_kmeans_dbscan.ipynb
notebooks/semana_5_validacao_completa_dbscan.ipynb
scripts/_gen_semana5.py
```

Saidas geradas:

```text
resultados/semana_5_clusters_base_completa.csv
resultados/semana_5_metricas_completa.csv
resultados/semana_5_metricas_dbscan_only.csv
resultados/preds/full_baseline.csv
resultados/preds/full_kmeans_dbscan.csv
resultados/preds/full_dbscan_only.csv
resultados/figuras/semana_5_*.png
```

## 5. Treinamento e execucao da tecnica

Os notebooks foram executados com:

```powershell
jupyter nbconvert --to notebook --execute notebooks/semana_5_validacao_completa_kmeans_dbscan.ipynb
jupyter nbconvert --to notebook --execute notebooks/semana_5_validacao_completa_dbscan.ipynb
```

Pipeline executado:

1. carregar e deduplicar a base completa;
2. aplicar K-Means e DBSCAN (Notebook 1) ou reutilizar rotulos salvos (Notebook 2);
3. construir matrizes de atributos com e sem clusters;
4. treinar Random Forest com split estratificado 80/20;
5. calcular metricas no teste e validacao cruzada estratificada (5 folds);
6. gerar visualizacoes (matriz de confusao, curvas PR/ROC, importancia de features, comparacoes entre modelos);
7. salvar metricas, predicoes e rotulos de cluster em CSV.

Tempo de execucao observado: ~7 min (Notebook 1) e ~6 min (Notebook 2), dominado pelo Random Forest com validacao cruzada sobre 283.726 registros.

## 6. Avaliacao na base completa

### 6.1 Resultados no conjunto de teste (base completa, 95 fraudes)

| Modelo | AUC-ROC | Average Precision | Recall | Precision | F1 | TN | FP | FN | TP |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| RF sem clusters | 0,9491 | 0,8241 | 0,7263 | 0,9583 | 0,8263 | 56648 | 3 | 26 | 69 |
| RF K-Means + DBSCAN | 0,9490 | 0,8122 | 0,7263 | 0,9583 | 0,8263 | 56648 | 3 | 26 | 69 |
| RF apenas DBSCAN | 0,9329 | 0,8083 | 0,7263 | 0,9718 | 0,8313 | 56649 | 2 | 26 | 69 |

Os tres modelos identificaram **69 de 95** fraudes no teste, com 2-3 falsos positivos. Recall, Precision e F1 foram identicos ou muito proximos entre baseline e K-Means+DBSCAN. O modelo apenas DBSCAN teve AUC-ROC ligeiramente inferior, mas Precision marginalmente superior (0,9718).

### 6.2 Resultados medios da validacao cruzada estratificada (base completa)

| Modelo | AUC-ROC media | Average Precision media | Recall medio | Precision media | F1 medio |
|---|---:|---:|---:|---:|---:|
| RF sem clusters | 0,9587 | **0,8371** | 0,7673 | 0,9312 | 0,8407 |
| RF K-Means + DBSCAN | **0,9611** | 0,8366 | 0,7694 | 0,9439 | 0,8470 |
| RF apenas DBSCAN | 0,9587 | 0,8386 | 0,7652 | 0,9384 | 0,8423 |

Na validacao cruzada — metrica mais estavel para este problema — **nenhum modelo com clusters superou o baseline de forma relevante**. O ganho maximo de Average Precision foi de **+0,0015** (apenas DBSCAN vs. baseline), dentro da variacao observada entre folds (desvio padrao ~0,02).

### 6.3 Importancia das features de cluster

No modelo K-Means + DBSCAN, a importancia somada das features de cluster foi **0,0512** (5,1% do total). As componentes `V*` (`V14`, `V4`, `V10`, `V12`, etc.) continuaram dominando. Entre as variaveis de cluster, **`dbscan_ruido_1`** foi a mais relevante (0,0274), acima dos grupos do K-Means — coerente com a maior concentracao de fraude na regiao de ruido.

## 7. Comparacao com a Semana 4 (amostra de 15k) e entre modelos

### 7.1 Amostra de 15k vs. base completa

| Contexto | Modelo | AP (teste) | AP media (CV) |
|---|---|---:|---:|
| Amostra 15k (Semana 4) | Sem clusters | 0,6058 | 0,8545 |
| Amostra 15k (Semana 4) | Com clusters | 0,6536 | 0,8155 |
| Base completa (Semana 5) | Sem clusters | 0,8241 | 0,8371 |
| Base completa (Semana 5) | K-Means + DBSCAN | 0,8122 | 0,8366 |
| Base completa (Semana 5) | Apenas DBSCAN | 0,8083 | 0,8386 |

Observacoes:

- na amostra de 15k, os clusters **melhoravam AP no teste** mas **pioravam AP na CV** — sinal instavel, possivelmente inflado pelo conjunto de teste com apenas 5 fraudes;
- na base completa, com 473 fraudes e teste de 95 positivos, o efeito dos clusters **nao se sustenta**: AP (CV) do baseline e dos modelos com cluster ficam praticamente empatados (~0,837);
- o ganho exploratorio visto na amostra reduzida **desaparece** quando avaliado sobre toda a populacao.

### 7.2 Respostas as perguntas de conclusao

**Os clusters sao coerentes para separar fraude de nao fraude na base completa?**
Parcialmente, do ponto de vista exploratorio. O DBSCAN concentra 93% das fraudes na regiao de ruido, mas com precisao muito baixa (0,585% de fraude entre os rotulados como ruido). O K-Means descreve perfis de transacao, nao separadores limpos de fraude.

**O ganho observado na amostra de 15k se mantem, melhora ou desaparece?**
**Desaparece.** Na base completa, o baseline supervisionado ja e forte e os clusters nao agregam ganho estavel em Average Precision ou AUC-ROC na validacao cruzada.

**Qual variavel de cluster contribui mais?**
O **`dbscan_ruido`** (sinal binario de anomalia) e mais util que os grupos do K-Means, tanto na escolha de representacao (Notebook 2) quanto na importancia de features (Notebook 1). Combinar K-Means + DBSCAN nao superou usar apenas o sinal de ruido do DBSCAN.

## 8. Produto esperado

Entregaveis produzidos na Semana 5:

- dois notebooks Jupyter reprodutiveis com markdown explicativo em cada etapa;
- rotulos de cluster da base completa (`semana_5_clusters_base_completa.csv`);
- metricas dos tres modelos e comparacao com a Semana 4;
- visualizacoes em `resultados/figuras/`:
  - `semana_5_kdistance_dbscan.png` — calibracao do `eps`;
  - `semana_5_nb1_matriz_confusao.png`, `semana_5_nb1_pr_curve.png`, `semana_5_nb1_importancia.png`;
  - `semana_5_nb1_comparacao_barras.png`, `semana_5_nb1_15k_vs_completa.png`;
  - `semana_5_comparacao_barras_3_modelos.png`, `semana_5_pr_curves_3_modelos.png`, `semana_5_roc_curves_3_modelos.png`;
  - `semana_5_15k_vs_completa_3_modelos.png`, `semana_5_nb2_diagnosticos.png`, `semana_5_nb2_importancia.png`;
- tabelas comparativas finais e conclusoes interpretadas nos notebooks e neste relatorio.

## 9. Limitacoes e proximos passos

**Limitacoes desta etapa:**

- o `eps` do DBSCAN precisou ser recalibrado (`2,5` em vez de `8,3063`), o que impede comparacao direta dos rotulos DBSCAN entre amostra de 15k e base completa;
- apesar de 473 fraudes, a taxa de fraude continua extremamente baixa (0,17%), mantendo sensibilidade das metricas a limiar de decisao;
- o Random Forest nao teve ajuste fino de hiperparametros nem otimizacao de limiar (fixo em 0,5).

**Proximos passos recomendados:**

- ajustar limiar de decisao com base na curva Precision-Recall (priorizar Recall ou Precision conforme custo de negocio);
- testar outras tecnicas supervisionadas (XGBoost, Logistic Regression com regularizacao);
- explorar features de cluster como entrada de um segundo estagio (stacking) em vez de concatenacao direta;
- considerar tecnicas de amostragem ou ponderacao alternativas a `class_weight='balanced'`;
- consolidar achados no relatorio tecnico final e slides de apresentacao.

**Conclusao geral da Semana 5:** os agrupamentos K-Means e DBSCAN permanecem uteis para **analise exploratoria** e identificacao de anomalias, mas **nao comprovaram melhora estavel** no classificador Random Forest quando avaliados sobre a populacao completa. O baseline supervisionado com as variaveis originais (`Time`, `Amount`, `V1`-`V28`) e suficiente para esta configuracao inicial de modelo.
