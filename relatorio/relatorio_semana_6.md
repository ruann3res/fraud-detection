# Relatorio Semana 6 - Inteligencia Computacional I

## 1. Definicao da tarefa de Inteligencia Computacional

A tarefa da Semana 6 foi testar um classificador supervisionado baseado em rede neural
MLP (Multi-Layer Perceptron) para detectar transacoes fraudulentas na populacao completa
de `dados/creditcard.csv`, comparando-o com o Random Forest da Semana 5 e com uma
**Regressao Logistica balanceada** como baseline linear escalonado.

O alvo continua sendo a coluna `Class`:

- `0`: transacao legitima;
- `1`: transacao fraudulenta.

A base foi carregada sem amostragem e deduplicada, mantendo o mesmo protocolo da Semana 5:

- 283.726 transacoes;
- 473 fraudes;
- taxa de fraude de 0,1667%;
- split estratificado 80/20 com `random_state=42`;
- validacao cruzada estratificada com 5 folds (modelos iniciais).

Como a base e altamente desbalanceada, a acuracia nao foi usada como metrica principal.
As metricas adotadas foram AUC-ROC, Average Precision, Recall, Precision, F1-Score e
matriz de confusao.

**Criterio de referencia:** o Random Forest da Semana 5 permanece o modelo principal ate
que outro algoritmo supere **Average Precision e F1 de forma consistente** (teste e CV).

## 2. Escolha justificada da tecnica

Foram testados tres familias de modelos:

| Familia | Papel |
|---|---|
| **Random Forest** (Semana 5) | Referencia principal |
| **MLP** (`MLPClassifier`) | Alternativa neural nao linear |
| **Regressao Logistica** | Baseline linear escalonado |

O MLP foi encapsulado em `Pipeline([StandardScaler(), MLPClassifier(...)])`, pois redes
neurais dependem de escalonamento — diferente das arvores do RF.

Ponderacao de classes no MLP: `sample_weight='balanced'` (a versao local do scikit-learn
nao expoe `class_weight` em `MLPClassifier`). Na Regressao Logistica, usou-se
`class_weight='balanced'`.

## 3. Preparacao dos dados para o modelo

Foram utilizados:

- `dados/creditcard.csv`: base completa de transacoes;
- `resultados/semana_5_clusters_base_completa.csv`: rotulos de K-Means e DBSCAN.

O clustering nao foi recalculado. As matrizes de atributos seguiram o protocolo da
Semana 5:

| Modelo | Features | n_features |
|---|---|---:|
| MLP / LR baseline | `Time`, `Amount`, `V1`-`V28` | 30 |
| MLP K-Means + DBSCAN | baseline + one-hot de clusters | 38 |
| MLP apenas DBSCAN | baseline + `dbscan_ruido` | 32 |

## 4. Construcao dos modelos

### 4.1 Modelos iniciais (limiar 0,5)

Tres variantes de MLP e uma Regressao Logistica, todas avaliadas com limiar padrao 0,5
e validacao cruzada de 5 folds.

### 4.2 Ajustes aplicados

Apos os resultados iniciais — MLP e LR com **Recall alto e Precision muito baixa** —
foram aplicados tres ajustes:

1. **Calibracao de probabilidades** com `CalibratedClassifierCV` + `FrozenEstimator`
   (metodo sigmoid), treinada em subconjunto de validacao interna (20% do treino).
2. **Ajuste de limiar** na curva Precision-Recall da validacao interna, buscando
   **maximizar Precision com Recall >= 72%** (referencia do RF baseline no teste).
3. **Regularizacao e arquiteturas menores** para reduzir falsos positivos:

| Configuracao | `hidden_layer_sizes` | `alpha` |
|---|---|---|
| MLP padrao | (64, 32) | 1e-4 |
| MLP medio | (32, 16) | 1e-3 |
| MLP compacto | (32,) | 1e-3 |
| MLP minimo | (16,) | 1e-2 |

Entregaveis reprodutiveis:

```text
scripts/semana_6_modelo_mlp.py
notebooks/semana_6_modelo_mlp.ipynb
```

Saidas geradas:

```text
resultados/semana_6_metricas_mlp.csv
resultados/semana_6_metricas_ajustadas.csv
resultados/semana_6_comparacao_rf_vs_mlp.csv
resultados/semana_6_comparacao_modelos_ajustada.csv
resultados/semana_6_resumo_referencia_rf.csv
resultados/preds/mlp_*.csv
resultados/preds/lr_baseline.csv
resultados/preds/*_tuned.csv
resultados/figuras/semana_6_*.png
```

## 5. Treinamento e execucao da tecnica

```bash
python -u scripts/semana_6_modelo_mlp.py
```

O script executa:

1. treino dos MLPs iniciais (com CV) e da Regressao Logistica;
2. calibracao + ajuste de limiar para LR e quatro variantes de MLP;
3. comparacao com os Random Forests da Semana 5;
4. verificacao se algum desafiante supera o RF em AP e F1 de forma consistente;
5. geracao de metricas, predicoes e figuras.

## 6. Avaliacao dos modelos iniciais (limiar 0,5)

### 6.1 Resultados no conjunto de teste

| Modelo | AUC-ROC | Average Precision | Recall | Precision | F1 | FP |
|---|---:|---:|---:|---:|---:|---:|
| MLP baseline | 0,9549 | 0,7325 | 0,8421 | 0,1770 | 0,2925 | 372 |
| MLP K-Means + DBSCAN | 0,9697 | 0,7130 | 0,8737 | 0,0967 | 0,1742 | 775 |
| MLP apenas DBSCAN | 0,9639 | 0,7475 | 0,8632 | 0,0994 | 0,1783 | 743 |
| Regressao Logistica | 0,9657 | 0,6719 | 0,8737 | 0,0564 | 0,1059 | 1389 |

Os MLPs e a Regressao Logistica encontraram mais fraudes que o RF (69-83 vs. 69-80 TP),
mas com **centenas a milhares de falsos positivos**, derrubando Precision e F1.

### 6.2 Validacao cruzada (modelos iniciais)

| Modelo | AUC-ROC media | AP media | F1 medio |
|---|---:|---:|---:|
| MLP baseline | 0,9669 | 0,7665 | 0,2869 |
| MLP apenas DBSCAN | 0,9654 | 0,7703 | 0,3542 |
| Regressao Logistica | 0,9784 | 0,7125 | 0,1142 |

Nenhum modelo inicial superou o RF em AP(CV) ou F1(CV).

## 7. Avaliacao apos calibracao e ajuste de limiar

### 7.1 Resultados no conjunto de teste (calibrado + limiar otimizado)

| Modelo | Limiar | AUC-ROC | AP | Recall | Precision | F1 | FP |
|---|---:|---:|---:|---:|---:|---:|---:|
| Regressao Logistica | 0,529 | 0,9617 | 0,6988 | 0,6526 | 0,8732 | 0,7470 | 9 |
| MLP (64,32) | 0,416 | 0,9449 | 0,7558 | 0,6842 | 0,8228 | 0,7471 | 14 |
| MLP (32,16) | 0,575 | 0,9603 | 0,7185 | 0,6000 | 0,8769 | 0,7125 | 8 |
| MLP (32,) | 0,657 | 0,9625 | 0,7308 | 0,7158 | 0,8947 | 0,7953 | 8 |
| MLP (16,) | 0,595 | 0,9519 | 0,7200 | 0,7368 | 0,8750 | 0,8000 | 10 |

**Efeito dos ajustes:** a calibracao + limiar reduziu falsos positivos de **372-1389 para 8-14**,
elevando Precision para **0,82-0,89**. O melhor MLP ajustado foi `MLP (32,) alpha=1e-3`
(F1=0,7953) e o melhor F1 geral entre desafiantes foi `MLP (16,) alpha=1e-2` (F1=0,8000).

### 7.2 Comparacao com Random Forest (referencia principal)

| Modelo | AP (teste) | F1 (teste) | AP (CV) | F1 (CV) |
|---|---:|---:|---:|---:|
| **RF baseline** | **0,8241** | **0,8263** | **0,8371** | **0,8407** |
| **RF apenas DBSCAN** | 0,8083 | **0,8313** | **0,8386** | **0,8423** |
| MLP (32,) ajustado | 0,7308 | 0,7953 | — | — |
| MLP (16,) ajustado | 0,7200 | 0,8000 | — | — |
| Regressao Logistica ajustada | 0,6988 | 0,7470 | — | — |

**Veredito:** nenhum modelo (MLP ou Regressao Logistica) superou o Random Forest de forma
consistente em **AP e F1**. O RF permanece referencia principal.

O melhor desafiante em F1 no teste foi `MLP (16,) alpha=1e-2` (0,8000 vs. 0,8313 do RF),
mas com AP inferior (0,7200 vs. 0,8083). Em AP(CV), o RF lidera com folga (~0,8386).

## 8. Respostas as perguntas da Semana 6

**O MLP supera o Random Forest na base completa?**
Nao. Mesmo apos calibracao e ajuste de limiar, o melhor MLP ficou abaixo do RF em
Average Precision e F1 no teste, e nenhum desafiante superou o RF em AP(CV) e F1(CV).

**Os clusters agregam mais valor ao MLP do que ao RF?**
Nao. Na configuracao inicial (limiar 0,5), K-Means + DBSCAN piorou Precision do MLP.
O melhor MLP ajustado usou apenas features originais (sem clusters).

**Qual variavel de cluster contribui mais no MLP?**
Na avaliacao inicial, `dbscan_ruido` teve AP(CV) ligeiramente superior ao baseline
neural, mas os ajustes focaram em arquiteturas sobre as 30 features originais, onde o
ganho foi maior.

**A Regressao Logistica e competitiva?**
Como baseline linear, a LR teve AUC-ROC alto (0,9617 apos calibracao), mas AP e F1
ficaram abaixo do RF. O limiar ajustado melhorou muito a Precision (0,8732), porem com
Recall menor (0,6526).

**Os ajustes de limiar e calibracao funcionaram?**
Sim, de forma expressiva. Precision subiu de ~0,10 para ~0,87-0,89 e falsos positivos
caíram de centenas para menos de 15. Porem, isso nao foi suficiente para superar o RF
em AP — indicando que o problema nao era apenas o limiar, mas a qualidade do ranking
de probabilidades do MLP/LR neste protocolo.

## 9. Produto esperado

Entregaveis produzidos na Semana 6:

- script reprodutivel com modelos iniciais e ajustados;
- notebook didatico `notebooks/semana_6_modelo_mlp.ipynb`;
- metricas iniciais e ajustadas em CSV;
- comparacao RF vs MLP vs LR;
- resumo de referencia RF em `semana_6_resumo_referencia_rf.csv`;
- figuras em `resultados/figuras/` (iniciais e ajustadas);
- este relatorio.

## 10. Limitacoes e proximos passos

**Limitacoes:**

- calibracao e limiar foram ajustados em subconjunto de validacao interna (20% do treino);
- modelos ajustados nao passaram por CV completa (custo computacional);
- MLP continua menos explicavel que o Random Forest;
- clusters nao foram reavaliados nesta etapa de ajuste.

**Proximos passos recomendados:**

- manter Random Forest como modelo principal ate superacao consistente em AP e F1;
- explorar XGBoost ou outras tecnicas de ensemble como desafiantes;
- testar SMOTE apenas no treino (experimento controlado);
- avaliar stacking com sinal de cluster como segundo estagio;
- considerar Autoencoder como complemento nao supervisionado (previsto em `TECNICAS_IC.md`).

**Conclusao geral da Semana 6:** o MLP e a Regressao Logistica sao funcionais e
responderam bem aos ajustes de calibracao e limiar, mas **nao superaram o Random Forest**.
O RF da Semana 5 permanece o classificador de referencia do projeto. Os clusters
continuam com ganho marginal; o foco desta semana foi validar alternativas supervisionadas
e refinar o protocolo de avaliacao para modelos baseados em probabilidade.
