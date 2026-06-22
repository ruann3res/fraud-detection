# Justificativa de cada decisão — Semana 3

## 1. Objetivo da Semana 3 — comparar, validar e interpretar agrupamentos

**Por quê:**

A Semana 2 entregou um baseline funcional com K-Means. Na Semana 3, o objetivo foi avançar de “primeiro modelo funcionando” para uma comparação metodológica entre algoritmos, incluindo validação por métricas, análise de parâmetros, interpretação dos grupos e definição de uso dos clusters na etapa de Inteligência Computacional.

A entrega foi organizada no notebook `notebooks/semana_3_comparacao.ipynb`, usando a mesma base `dados/creditcard.csv` e mantendo o princípio metodológico mais importante: `Class` não entra no treinamento dos agrupamentos.

## 2. Dados utilizados — base completa carregada; `Class` apenas para análise externa

**Por quê:**

A base carregada possui 284.807 transações e 31 colunas. As colunas correspondem a `Time`, `V1`–`V28`, `Amount` e `Class`.

`Class` foi separada da matriz de agrupamento porque representa o rótulo real de fraude. Usá-la no treinamento do K-Means ou DBSCAN causaria vazamento de informação e invalidaria a proposta de agrupamento não supervisionado.

Mesmo assim, `Class` foi mantida no dataframe para análise posterior. Isso permite responder a pergunta central da Semana 3: os clusters formados sem saber quem é fraude concentram fraudes acima da média?

## 3. Atributos selecionados — 30 features: `V1`–`V28` + `Time` + `Amount`

**Por quê:**

A única variável excluída da matriz de agrupamento foi `Class`. Portanto, foram usadas 30 features numéricas:

- `V1`–`V28`: componentes PCA anonimizadas, que concentram a maior parte do sinal comportamental da transação.
- `Time`: segundos desde a primeira transação, útil para capturar padrões temporais, horários e possíveis sequências suspeitas.
- `Amount`: valor financeiro da transação, principal variável interpretável do ponto de vista de negócio.

Manter `Time` foi uma decisão importante porque a variável pode ser útil na etapa de Inteligência Computacional. Além disso, usar as mesmas features do baseline da Semana 2 torna a comparação mais coerente.

## 4. Escalonamento — `StandardScaler` para K-Means e `RobustScaler` para DBSCAN

**Por quê:**

K-Means depende diretamente de distância euclidiana. Por isso, foi usado `StandardScaler`, que coloca as variáveis na mesma escala, com média 0 e desvio padrão 1.

DBSCAN também depende de distância, mas é mais sensível à definição de vizinhança (`eps`) e à presença de valores extremos. Por isso, foi usado `RobustScaler`, que é mais resistente a outliers por trabalhar com mediana e intervalo interquartil.

Essa diferença de escalonamento foi adotada porque os algoritmos têm comportamentos diferentes:

- K-Means precisa de escala equilibrada para formar centróides.
- DBSCAN precisa reduzir a influência de valores extremos para detectar regiões densas e ruído.

## 5. Amostra de comparação — 15.000 registros

**Por quê:**

Algumas etapas da Semana 3 têm custo computacional alto, especialmente DBSCAN e Silhouette Score. Por isso, foi usada uma amostra de 15.000 registros para comparação.

Quando possível, a amostra preserva a presença da classe minoritária, evitando que as fraudes desapareçam da análise. Isso é importante porque a base é extremamente desbalanceada: 284.315 transações legítimas e 492 fraudes.

A amostra permite comparar algoritmos com tempo de execução viável, sem abandonar a análise crítica da concentração de fraudes por cluster.

## 6. Primeiro algoritmo — K-Means com `k = 6`

**Por quê:**

O K-Means foi reconstruído na Semana 3 como referência de comparação com o segundo algoritmo. O valor `k = 6` foi mantido porque já havia sido escolhido na Semana 2 com base no melhor Silhouette dentro dos testes realizados.

Na Semana 3, o K-Means formou 6 clusters avaliáveis e obteve:

| Métrica | Valor |
|---------|-------|
| Silhouette | 0,0838 |
| Davies-Bouldin | 2,4227 |
| Calinski-Harabasz | 617,44 |
| Taxa de ruído | 0,00% |

O Silhouette baixo indica que os clusters possuem sobreposição e fronteiras pouco nítidas. Ainda assim, o K-Means foi o único algoritmo que gerou múltiplos clusters avaliáveis pelas métricas internas.

## 7. Segundo algoritmo — DBSCAN

**Por quê:**

DBSCAN foi escolhido como segundo algoritmo porque trabalha com densidade e consegue marcar pontos como ruído (`-1`). Isso é relevante para fraude, pois transações fraudulentas podem aparecer como comportamento atípico, não necessariamente como um cluster grande e bem separado.

Os parâmetros principais foram:

- `min_samples = 60`
- `eps = 8,3063`

`min_samples` foi definido como `2 * número_de_features`. Como a matriz possui 30 atributos, o valor escolhido foi 60. Essa regra torna a formação de regiões densas mais conservadora em alta dimensionalidade.

O `eps` preliminar foi estimado pela curva de distância ao 60º vizinho mais próximo, usando o percentil 95 das distâncias. Assim, o valor não foi escolhido arbitrariamente.

## 8. Teste de parâmetros do DBSCAN — `eps` menor, base e maior

**Por quê:**

Foram testados três valores de `eps`:

| `eps` | `min_samples` | Clusters sem ruído | Taxa de ruído |
|-------|---------------|--------------------|---------------|
| 6,2297 | 60 | 1 | 5,13% |
| 8,3063 | 60 | 1 | 2,57% |
| 10,3829 | 60 | 1 | 1,53% |

O comportamento foi consistente: quanto maior o `eps`, menor a taxa de ruído, porque mais pontos passam a ser considerados vizinhos.

Mesmo assim, o DBSCAN formou apenas um cluster principal em todos os testes. Por isso, as métricas Silhouette, Davies-Bouldin e Calinski-Harabasz ficaram como `NaN`: elas exigem pelo menos dois clusters válidos para medir separação.

Essa limitação não inutiliza o DBSCAN; ela muda sua interpretação. No contexto desta base, com esses parâmetros, ele funcionou melhor como detector de anomalias do que como segmentador de múltiplos perfis.

## 9. Comparação entre algoritmos — K-Means segmenta; DBSCAN identifica anomalia

**Por quê:**

A comparação final mostrou:

| Algoritmo | Parâmetros | Clusters avaliados | Silhouette | Davies-Bouldin | Calinski-Harabasz | Taxa de ruído |
|-----------|------------|--------------------|------------|----------------|-------------------|---------------|
| K-Means | `k=6`, `StandardScaler` | 6 | 0,0838 | 2,4227 | 617,44 | 0,00% |
| DBSCAN | `eps=8,3063`, `min_samples=60`, `RobustScaler` | 1 | NaN | NaN | NaN | 2,57% |

Pelas métricas internas, o K-Means é superior porque gera múltiplos clusters comparáveis. Porém, a análise de fraude mostra que o DBSCAN agrega uma informação diferente: o grupo de ruído concentrou uma proporção de fraude muito acima da média.

Assim, a conclusão não é “um algoritmo substitui o outro”, mas sim que eles são complementares:

- K-Means é melhor para segmentar perfis.
- DBSCAN é melhor para sinalizar comportamento atípico.

## 10. Interpretação dos clusters K-Means

**Por quê:**

A interpretação cruzou os clusters gerados sem `Class` com a variável `Class` após o agrupamento. Isso permite medir se os grupos formados concentram fraudes.

Resultados principais do K-Means:

| Cluster | Quantidade | Fraudes | Taxa de fraude | Interpretação |
|---------|------------|---------|----------------|---------------|
| 4 | 6.175 | 4 | 0,0648% | Perfil predominante de baixo risco |
| 1 | 5.330 | 6 | 0,1126% | Perfil predominante de baixo/moderado risco |
| 5 | 2.155 | 0 | 0,0000% | Perfil sem fraude observada na amostra |
| 0 | 1.059 | 3 | 0,2833% | Perfil de risco acima da média |
| 3 | 268 | 0 | 0,0000% | Perfil de transações de alto valor |
| 2 | 13 | 12 | 92,3077% | Perfil crítico de fraude concentrada |

O cluster 2 é o principal achado do K-Means. Apesar de possuir apenas 13 transações, concentrou 12 fraudes, com taxa de fraude de 92,31%.

O cluster 3 também é relevante para interpretação de negócio: possui `Amount` médio alto, aproximadamente US$ 1.355,74, mas não apresentou fraudes na amostra. Isso reforça que valor alto sozinho não é sinônimo de fraude.

## 11. Interpretação dos clusters DBSCAN

**Por quê:**

O DBSCAN gerou dois rótulos:

- `0`: cluster principal.
- `-1`: ruído/anomalia.

Resultados:

| Cluster DBSCAN | Quantidade | Fraudes | Taxa de fraude | Interpretação |
|----------------|------------|---------|----------------|---------------|
| 0 | 14.614 | 2 | 0,0137% | Comportamento transacional dominante |
| -1 | 386 | 23 | 5,9585% | Ruído/anomalia com alta concentração de fraude |

O grupo `-1` é o principal achado do DBSCAN. Ele representa apenas 386 transações da amostra, mas concentrou 23 fraudes, alcançando taxa de fraude de 5,96%.

Isso confirma que, mesmo não formando vários clusters, o DBSCAN foi útil para separar um grupo atípico com risco muito superior ao comportamento dominante.

## 12. Nomeação dos perfis encontrados

**Por quê:**

Nomear os clusters facilita a comunicação dos resultados e prepara a integração com a etapa de Inteligência Computacional.

Perfis K-Means:

- Cluster 2: **Perfil crítico de fraude concentrada**.
- Cluster 0: **Perfil de risco acima da média**.
- Cluster 3: **Perfil de transações de alto valor financeiro**.
- Clusters 1 e 4: **Perfis transacionais predominantes de baixo risco**.
- Cluster 5: **Perfil transacional sem fraude observada na amostra**.

Perfis DBSCAN:

- Cluster 0: **Comportamento transacional dominante**.
- Cluster -1: **Ruído/anomalia com alta concentração de fraude**.

Essa nomeação é preliminar, mas suficiente para orientar a etapa seguinte do projeto.

## 13. Estrutura de saída do agrupamento

**Por quê:**

A Semana 3 também precisa gerar uma variável ou estrutura de saída para uso futuro. A estrutura definida foi:

- `cluster_kmeans_semana3`: rótulo categórico do perfil K-Means.
- `perfil_kmeans`: nome interpretável do perfil K-Means.
- `cluster_dbscan_semana3`: rótulo do DBSCAN.
- `perfil_dbscan`: nome interpretável do perfil DBSCAN.
- `dbscan_ruido`: indicador binário, com valor 1 quando `cluster_dbscan_semana3 == -1`.

Essa estrutura pode ser exportada como `dados/saida_clusters_semana3.csv` e integrada ao dataset supervisionado das Semanas 4 e 5.

## 14. Definição de uso na Inteligência Computacional

**Por quê:**

A decisão para a etapa de IC é usar os agrupamentos como novas features, sem substituir as variáveis originais.

Uso definido:

- `cluster_kmeans_semana3` como feature categórica de perfil.
- `dbscan_ruido` como indicador binário de anomalia.
- Comparar modelos supervisionados com e sem essas variáveis.

Essa estratégia permite testar, de forma objetiva, se o agrupamento melhora o desempenho do modelo supervisionado em métricas adequadas para fraude, como AUC-ROC, F1-Score, Recall e Precision.

## 15. Problemas e limitações identificados

**Por quê registrar isso:**

O K-Means apresentou Silhouette de 0,0838, valor próximo de 0. Isso indica clusters sobrepostos e separação geométrica fraca. Ainda assim, ele identificou um perfil crítico com alta concentração de fraude.

O DBSCAN, por sua vez, não conseguiu formar múltiplos clusters com os parâmetros testados. Ele criou um cluster dominante e um grupo de ruído. Portanto, suas métricas internas ficaram indisponíveis (`NaN`), mas seu ruído teve alta utilidade prática.

A principal limitação da Semana 3 é que os resultados foram avaliados em amostra de 15.000 registros, por custo computacional. A decisão final de uso em IC deve ser confirmada na Semana 4, comparando modelos supervisionados com e sem as variáveis de agrupamento.

## 16. Conclusão da Semana 3

**Por quê:**

A Semana 3 cumpriu os requisitos obrigatórios:

- aplicou um segundo algoritmo de agrupamento (`DBSCAN`);
- comparou DBSCAN com K-Means;
- usou métricas de avaliação;
- analisou os parâmetros utilizados;
- interpretou os clusters;
- nomeou os perfis encontrados;
- definiu como os clusters serão usados em Inteligência Computacional;
- gerou estrutura de saída para integração futura.

Conclusão geral: o K-Means deve ser mantido como estrutura principal de segmentação, e o DBSCAN deve ser usado como sinal complementar de anomalia. A combinação `cluster_kmeans_semana3` + `dbscan_ruido` é a proposta mais promissora para enriquecer a base da etapa de Inteligência Computacional.
