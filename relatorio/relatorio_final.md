# Relatório Final — Detecção de Fraude em Transações Financeiras

**Trabalho Final Integrador**  
Disciplina: Tópicos Especiais 2 — Agrupamento de Dados e Inteligência Computacional

---

## 1. Título do projeto

**Detecção de Fraude em Transações Financeiras: integração de K-Means e DBSCAN com classificação supervisionada para identificação de transações fraudulentas em cartão de crédito.**

---

## 2. Integrantes e papéis exercidos


| Integrante | Papel                                | Contribuições principais                                                                                                                        |
| ---------- | ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **Ruan**   | Inteligência Computacional e Decisão | Escolha e implementação das técnicas de IC, métricas, tratamento de desbalanceamento, comparação com e sem clusters, relatórios das Semanas 4–6 |
| **Lucio**  | Dados, Pipeline e Integração         | Organização do repositório, documentação da base, EDA, integração dos entregáveis e consolidação do pipeline                                    |
| **Artur**  | Agrupamento                          | Pré-processamento, implementação de K-Means e DBSCAN, avaliação e interpretação dos clusters, geração de rótulos para a etapa de IC             |


---



## 3. Cenário atribuído

**Cenário 4 — Detecção de Fraude ou Transações Financeiras Suspeitas.**

Instituições financeiras processam milhões de transações diárias; apenas uma fração mínima (~0,17%) corresponde a fraudes, mas cada caso gera prejuízo direto ao cliente e à instituição. O desafio é identificar essas transações entre um volume massivo de operações legítimas, com alta precisão e em tempo hábil para revisão.

---



## 4. Descrição do problema

O problema consiste em **classificar transações de cartão de crédito como legítimas (**`Class = 0`**) ou fraudulentas (**`Class = 1`**)**, utilizando características anonimizadas das transações.

Características centrais do problema:

- **Desbalanceamento extremo:** ~99,83% de transações legítimas e ~0,17% de fraudes.
- **Features anonimizadas:** `V1`–`V28` são componentes PCA; apenas `Time` e `Amount` têm leitura direta de negócio.
- **Fraudes como anomalias:** transações fraudulentas tendem a se comportar de forma atípica em relação ao padrão dominante.
- **Custo assimétrico de erros:** falsos negativos (fraude não detectada) geram prejuízo financeiro; falsos positivos (alarmes indevidos) geram custo operacional de investigação.

**Pergunta central do projeto:** os agrupamentos K-Means e DBSCAN, aplicados de forma não supervisionada, agregam valor a um classificador supervisionado de fraude?

---



## 5. Justificativa comercial, educacional e institucional



### Comercial

- Reduz perdas por fraude e chargebacks.
- Diminui carga operacional ao priorizar transações de maior risco.
- Aumenta confiança do cliente na segurança do meio de pagamento.



### Educacional

- Integra **agrupamento não supervisionado** e **Inteligência Computacional supervisionada** em um pipeline completo.
- Exige escolha consciente de métricas (AUC-ROC, Average Precision, F1 — não acurácia) diante de classes desbalanceadas.
- Permite comparar algoritmos, interpretar limitações e documentar decisões metodológicas.



### Institucional

- Atende ao escopo do Trabalho Final Integrador da disciplina, cobrindo EDA, clustering, IC e avaliação crítica.
- Produz artefatos reprodutíveis (notebooks, scripts, CSVs, relatórios) alinhados ao plano de IC documentado em `instrucoes_IC/`.

---



## 6. Descrição da base de dados


| Atributo                | Descrição                                                                   |
| ----------------------- | --------------------------------------------------------------------------- |
| **Nome**                | Credit Card Fraud Detection                                                 |
| **Fonte**               | [Kaggle — MLG ULB](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) |
| **Período**             | 2 dias (setembro de 2013)                                                   |
| **Região**              | Transações europeias                                                        |
| **Registros originais** | 284.807 transações                                                          |
| **Após deduplicação**   | 283.726 transações (1.081 duplicatas removidas)                             |
| **Fraudes**             | 473 (0,1667% após deduplicação; 492 na base original)                       |
| **Features**            | `Time`, `Amount`, `V1`–`V28`, `Class`                                       |


**Variáveis:**

- `V1`**–**`V28`**:** componentes PCA anonimizadas; concentram o sinal comportamental.
- `Time`**:** segundos desde a primeira transação (~2 dias de janela).
- `Amount`**:** valor da transação em dólar (única feature financeira interpretável).
- `Class`**:** alvo binário (0 = legítima, 1 = fraude); usada apenas na avaliação dos clusters e no treino supervisionado.

---



## 7. Análise exploratória

A EDA foi conduzida no notebook `notebooks/Semana_1_EDA_e_Preparacao.ipynb`. Principais achados:

1. **Desbalanceamento confirmado:** taxa de fraude ~0,17%; acurácia seria métrica enganosa.
2. **Sem valores ausentes** nas colunas analisadas.
3. **Duplicatas:** 1.081 registros duplicados identificados e removidos nas etapas seguintes.
4. `Amount`**:** distribuição assimétrica, com valores extremos; outliers não foram removidos automaticamente (podem ser fraudes).
5. `V1`**–**`V28`**:** já centradas e escaladas por PCA; concentram padrões multivariados relevantes.
6. `Time`**:** cobre janela curta; ainda assim útil para capturar sequências e horários atípicos.
7. **Correlação com fraude:** algumas componentes PCA (`V14`, `V4`, `V10`, `V12`) aparecem entre as mais informativas nos modelos supervisionados posteriores.

Documentação complementar: `PROBLEMA.md`, `checklist_semanal/CHECKLIST_SEMANA_1.md`.

---



## 8. Pré-processamento


| Etapa                             | Decisão                                | Justificativa                                  |
| --------------------------------- | -------------------------------------- | ---------------------------------------------- |
| Remoção de duplicatas             | 1.081 registros                        | Evitar distorção de clusters e métricas        |
| Exclusão de `Class` do clustering | Sempre                                 | Evitar vazamento de informação                 |
| Features de clustering            | `V1`–`V28`, `Time`, `Amount` (30)      | Mesmo conjunto nas Semanas 2–5                 |
| K-Means                           | `StandardScaler`                       | K-Means depende de distância euclidiana        |
| DBSCAN                            | `RobustScaler`                         | Reduz impacto de outliers em `Amount`          |
| IC (Random Forest)                | Sem escalonamento                      | Árvores são invariantes à escala               |
| IC (MLP / Regressão Logística)    | `StandardScaler` no Pipeline           | Otimização por gradiente exige escala uniforme |
| Split supervisionado              | 80/20 estratificado, `random_state=42` | Preserva proporção de fraudes                  |
| Desbalanceamento (RF)             | `class_weight='balanced'`              | Penaliza erros na classe minoritária           |
| Desbalanceamento (MLP)            | `sample_weight='balanced'`             | Equivalente funcional no ambiente sklearn      |


---



## 9. Algoritmos de agrupamento utilizados



### 9.1 K-Means (Semanas 2 e 3; replicado na base completa — Semana 5)


| Parâmetro      | Valor                               |
| -------------- | ----------------------------------- |
| `k`            | 6 (melhor Silhouette entre k=2..10) |
| Escalonamento  | `StandardScaler`                    |
| `n_init`       | 10                                  |
| `random_state` | 42                                  |


**Papel:** segmentar perfis transacionais em grupos interpretáveis.

### 9.2 DBSCAN (Semana 3; replicado na base completa — Semana 5)


| Parâmetro     | Amostra 15k    | Base completa         |
| ------------- | -------------- | --------------------- |
| `min_samples` | 60             | 60                    |
| `eps`         | 8,3063         | **2,5** (recalibrado) |
| Escalonamento | `RobustScaler` | `RobustScaler`        |


**Recalibragem do** `eps`**:** na base completa, o `eps` da amostra (8,3) tornou o DBSCAN inviável (vizinhanças com centenas de milhares de pontos). A curva k-distance foi recalculada e adotou-se `eps=2,5`, mantendo o algoritmo executável (~28s) com sinal de anomalia.

**Papel:** identificar pontos de ruído (`-1`) como candidatos a comportamento atípico/anômalo.

---



## 10. Avaliação dos clusters



### 10.1 Métricas internas (amostra 15k — Semana 3)


| Algoritmo     | Silhouette | Davies-Bouldin | Calinski-Harabasz | Clusters          |
| ------------- | ---------- | -------------- | ----------------- | ----------------- |
| K-Means (k=6) | 0,0838     | 2,4227         | 617,44            | 6                 |
| DBSCAN        | —          | —              | —                 | 1 cluster + ruído |


Silhouette baixo no K-Means indica clusters sobrepostos, mas ainda úteis para segmentação. DBSCAN formou essencialmente um cluster principal + ruído; métricas internas clássicas ficaram limitadas.

### 10.2 Avaliação externa (concentração de fraude — `Class` usada apenas após clustering)

**K-Means (amostra 15k):**


| Cluster          | Destaque                               |
| ---------------- | -------------------------------------- |
| Cluster 2        | 92,31% de fraude (12 de 13 transações) |
| Clusters 3, 4, 5 | Taxa acima da média global (0,173%)    |


**DBSCAN (amostra 15k):**


| Grupo        | Taxa de fraude               |
| ------------ | ---------------------------- |
| Ruído (`-1`) | 5,96% (23 de 386 transações) |
| Demais       | Próximo de zero              |


**DBSCAN (base completa — Semana 5):**

- **93,02%** das fraudes (440 de 473) na região de ruído.
- Taxa de fraude no ruído: **0,585%** (acima da média, porém com muitos falsos positivos estruturais).
- 17 clusters densos; 26,51% da base marcada como ruído.

---



## 11. Interpretação dos grupos



### K-Means — perfis transacionais

- **Cluster 2 (amostra):** microgrupo com concentração extrema de fraude — útil para análise, instável por tamanho.
- **Clusters 3, 4, 5:** taxas de fraude entre 1,5× e 3,9× a média global — perfis de risco relativo.
- **Interpretação geral:** K-Means **nomeia perfis**, não separa fraude de forma limpa; fraude aparece diluída entre grupos.



### DBSCAN — anomalias

- Ruído (`-1`) funciona como **detector de comportamento atípico**.
- Concentra a maioria das fraudes, mas com **precisão baixa** (~0,58% no ruído na base completa).
- **Interpretação geral:** excelente para exploração e triagem; insuficiente sozinho como classificador.



### Síntese para IC

Foram definidas duas features derivadas:

- `cluster_kmeans` — perfil categórico (one-hot).
- `dbscan_ruido` — binário (1 = ponto de ruído/anomalia).

---



## 12. Técnica de Inteligência Computacional utilizada



### Técnica principal: Random Forest

Escolhida por robustez a desbalanceamento, capacidade não linear, interpretabilidade via importância de features e facilidade de comparação com/sem clusters.

```python
RandomForestClassifier(
    n_estimators=200,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1,
)
```



### Técnicas alternativas testadas (Semana 6)


| Técnica                            | Objetivo                          |
| ---------------------------------- | --------------------------------- |
| **MLP** (`MLPClassifier`)          | Testar rede neural supervisionada |
| **Regressão Logística balanceada** | Baseline linear escalonado        |


Ajustes na Semana 6: calibração de probabilidades (`CalibratedClassifierCV`), ajuste de limiar na curva PR e variantes de MLP com maior regularização.

**Resultado:** Random Forest permanece **referência principal** — nenhum desafiante superou AP e F1 de forma consistente.

---



## 13. Tarefa final

**Classificação binária (predição):** dado o vetor de features de uma transação (`Time`, `Amount`, `V1`–`V28`, opcionalmente features de cluster), **prever a probabilidade de fraude** e classificar como legítima ou fraudulenta.

Tipo de saída:

- **Classe predita** (`0` ou `1`) via limiar de decisão (padrão 0,5 no RF; otimizado na Semana 6 para MLP/LR).
- **Score de risco** (`predict_proba`) para fila de revisão manual.

Predições foram geradas no **conjunto de teste estratificado** (~56.746 transações, ~95 fraudes) e salvas em `resultados/preds/`.

---



## 14. Comparação dos resultados com e sem clusters



### 14.1 Random Forest — amostra 15k (Semana 4)


| Modelo          | AP (teste) | AP (CV)    | F1 (teste) |
| --------------- | ---------- | ---------- | ---------- |
| RF sem clusters | 0,6058     | **0,8545** | 0,8000     |
| RF com clusters | 0,6536     | 0,8155     | 0,8000     |


Efeito instável: clusters melhoraram AP no teste (5 fraudes), mas pioraram na CV.

### 14.2 Random Forest — base completa (Semana 5)


| Modelo              | AP (teste) | AP (CV)    | Recall | Precision | F1         |
| ------------------- | ---------- | ---------- | ------ | --------- | ---------- |
| RF sem clusters     | **0,8241** | **0,8371** | 0,7263 | 0,9583    | 0,8263     |
| RF K-Means + DBSCAN | 0,8122     | 0,8366     | 0,7263 | 0,9583    | 0,8263     |
| RF apenas DBSCAN    | 0,8083     | 0,8386     | 0,7263 | 0,9718    | **0,8313** |


**Conclusão:** diferença máxima de AP (CV) = **+0,0015** (marginal). Clusters **não superaram** o baseline. Importância das features de cluster: **5,1%** vs **94,9%** das variáveis PCA.

### 14.3 MLP e Regressão Logística (Semana 6)


| Modelo                        | F1 (teste) | Observação               |
| ----------------------------- | ---------- | ------------------------ |
| MLP (limiar 0,5)              | ~0,17–0,29 | Muitos falsos positivos  |
| MLP (16,) calibrado + limiar  | 0,8000     | Melhor desafiante neural |
| Regressão Logística calibrada | 0,7470     | Abaixo do RF             |
| **RF apenas DBSCAN**          | **0,8313** | **Referência**           |


---



## 15. Limitações da solução

1. **Janela temporal curta:** base cobre apenas 2 dias; padrões sazonais não capturados.
2. **Features anonimizadas:** `V1`–`V28` impedem explicação de negócio direta.
3. **Desbalanceamento extremo:** métricas sensíveis ao limiar; conjunto de teste com 95 fraudes ainda é pequeno em termos absolutos.
4. **DBSCAN não comparável entre amostra e base completa** (`eps` recalibrado).
5. **Clusters com ganho preditivo marginal** quando concatenados ao RF.
6. **Sem deploy em produção:** avaliação offline; sem latência, streaming ou feedback loop.
7. **Sem custo de negócio explícito** na otimização de limiar (trade-off FP vs FN não quantificado em R$).
8. **Sem SMOTE ou ensemble avançado** (XGBoost, stacking) na versão final do RF.

---



## 16. Possibilidades de melhoria


| Direção                       | Descrição                                                                           |
| ----------------------------- | ----------------------------------------------------------------------------------- |
| **Limiar de decisão**         | Otimizar pela curva PR conforme custo de FP vs FN                                   |
| **Modelos alternativos**      | XGBoost, LightGBM, ensemble com RF                                                  |
| **Stacking em dois estágios** | Usar `dbscan_ruido` como filtro de triagem, RF no segundo estágio                   |
| **Autoencoder**               | Detecção não supervisionada por erro de reconstrução (previsto em `TECNICAS_IC.md`) |
| **SMOTE / undersampling**     | Experimentos controlados no treino                                                  |
| **Busca de hiperparâmetros**  | Grid search no Random Forest                                                        |
| **Features temporais**        | Janelas rolling, velocidade de gasto por cartão                                     |
| **Base ampliada**             | Incorporar mais dias/semanas de transações                                          |
| **Explicabilidade**           | SHAP values para interpretar predições individuais                                  |


---



## 17. Conclusão

Este projeto implementou um **pipeline completo** de detecção de fraude em cartão de crédito, integrando:

1. **Análise exploratória e pré-processamento** de uma base altamente desbalanceada.
2. **Agrupamento não supervisionado** com K-Means (perfis) e DBSCAN (anomalias).
3. **Classificação supervisionada** com Random Forest, comparando modelos com e sem features de cluster.
4. **Validação rigorosa** na base completa (283.726 transações, 473 fraudes).
5. **Experimentos complementares** com MLP e Regressão Logística, incluindo calibração e ajuste de limiar.

**Sobre o agrupamento:** K-Means e DBSCAN cumpriram papel **exploratório e interpretativo** — o DBSCAN concentrou 93% das fraudes na região de ruído; o K-Means identificou perfis com risco relativo elevado. Porém, como **features adicionais ao Random Forest**, o ganho preditivo foi **marginal e estatisticamente fraco** (AP CV +0,0015 no melhor caso).

**Sobre a Inteligência Computacional:** o **Random Forest** com `class_weight='balanced'` obteve o melhor equilíbrio entre Precision (~~96%), Recall (~~73%) e F1 (~0,83) no conjunto de teste, com apenas 3 falsos positivos em ~56 mil transações. MLP e Regressão Logística **não superaram** o RF de forma consistente.

**Mensagem final:** *agrupamento explica; o Random Forest prediz* — neste dataset e protocolo, predizer bem **não exigiu** os clusters. O sinal mais promissor para evoluções futuras é o `dbscan_ruido`, possivelmente em arquiteturas de dois estágios ou detecção de anomalia, não como feature concatenada direta.

---



## 18. Referências e links das bases utilizadas

1. **Credit Card Fraud Detection (Kaggle — MLG ULB)**
  [https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
2. **Andrea Dal Pozzolo et al.** — *Calibrating Probability with Undersampling for Unbalanced Classification* (contexto do dataset).
3. **Documentação scikit-learn**
  [https://scikit-learn.org/stable/](https://scikit-learn.org/stable/)  
   (KMeans, DBSCAN, RandomForestClassifier, MLPClassifier, CalibratedClassifierCV, métricas)
4. **Material da disciplina**
  - `instrucoes_IC/PLANO_IC.md`  
  - `instrucoes_IC/TECNICAS_IC.md`  
  - `instrucoes_IC/Documentacao_Referencia_IC.pdf`
5. **Trabalho Final — enunciado**
  `Trabalho_Final_AgrupamentoDeDados_InteligênciaComputacional.docx (1).pdf`

---



## 19. Link para o repositório e arquivos do projeto

**Repositório GitHub:**  
[https://github.com/ruann3res/fraud-detection](https://github.com/ruann3res/fraud-detection)

### Estrutura principal de entregáveis


| Pasta / arquivo        | Conteúdo                                                                    |
| ---------------------- | --------------------------------------------------------------------------- |
| `notebooks/`           | Notebooks executáveis (Semanas 1–6)                                         |
| `scripts/`             | Pipelines reprodutíveis (`semana_4_modelo_ic.py`, `semana_6_modelo_mlp.py`) |
| `relatorio/`           | Relatórios semanais e este relatório final                                  |
| `resultados/`          | CSVs de métricas, clusters e predições                                      |
| `resultados/figuras/`  | Gráficos (matrizes de confusão, curvas PR/ROC, comparações)                 |
| `presentation/`        | Slides e roteiro de apresentação                                            |
| `dados/creditcard.csv` | Base de dados (não versionada — download via Kaggle)                        |




### Notebooks por etapa


| Semana | Notebook                                          |
| ------ | ------------------------------------------------- |
| 1      | `Semana_1_EDA_e_Preparacao.ipynb`                 |
| 2      | `semana_2_clustering_baseline.ipynb`              |
| 3      | `semana_3_comparacao.ipynb`                       |
| 4      | `semana_4_modelo_ic.ipynb`                        |
| 5      | `semana_5_validacao_completa_kmeans_dbscan.ipynb` |
| 5      | `semana_5_validacao_completa_dbscan.ipynb`        |
| 6      | `semana_6_modelo_mlp.ipynb`                       |




### Resultados numéricos principais


| Arquivo                                          | Descrição                           |
| ------------------------------------------------ | ----------------------------------- |
| `resultados/semana_4_metricas_modelo_ic.csv`     | RF amostra 15k                      |
| `resultados/semana_5_metricas_completa.csv`      | RF base completa                    |
| `resultados/semana_5_clusters_base_completa.csv` | Rótulos de cluster (283.726 linhas) |
| `resultados/semana_6_metricas_mlp.csv`           | MLP e LR iniciais                   |
| `resultados/semana_6_metricas_ajustadas.csv`     | MLP/LR calibrados + limiar          |
| `resultados/semana_6_resumo_referencia_rf.csv`   | Veredito RF vs desafiantes          |
| `resultados/preds/`                              | Predições no conjunto de teste      |


---

*Relatório consolidado em julho de 2026 — Tópicos Especiais 2, Agrupamento de Dados e Inteligência Computacional.*