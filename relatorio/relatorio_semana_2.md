# Justificativa de cada decisão — Semana 2

## 1. Dados preparados — 283.726 transações; `Class` separada do clustering

**Por quê:**

Repetimos a remoção de 1.081 duplicatas da Semana 1 para não agrupar transações idênticas mais de uma vez — duplicatas distorceriam tamanho e perfil dos clusters.

`Class` não entra no clustering porque é a variável que queremos avaliar depois, não explicar antes. Se usássemos `Class` no treino, seria vazamento de informação: o algoritmo “saberia” quem é fraude antes de formar os grupos, invalidando a análise de padrões não supervisionados.

## 2. Atributos selecionados — 30 features: `V1`–`V28` + `Time` + `Amount`

**Por quê:**

`V1`–`V28`: são as features principais da base (resultado de PCA). Concentram a variação do comportamento da transação; sem elas, o agrupamento perderia quase todo o sinal.

`Amount`: única feature financeira interpretável — valor alto ou atípico pode indicar risco.

`Time`: segundos desde a primeira transação; captura padrão temporal (horários, sequências de ataques).

`Class` excluída (ver item 1).

Baseline da Semana 2: usar todas as features numéricas disponíveis, exceto o alvo.

## 3. Justificativa — PCA concentra o sinal; `Amount` e `Time` trazem risco financeiro e temporal

**Por quê:**

PCA (`V1`–`V28`): o dataset original foi anonimizado; essas componentes são o que restou de informação útil. Agrupar só por `Amount`/`Time` seria insuficiente — a fraude aparece sobretudo nos padrões multivariados (`V1`–`V28`).

`Amount`: na Semana 1, fraudes e legítimas têm distribuições diferentes de valor; mantê-la dá ao cluster um eixo interpretável de “volume da transação”.

`Time`: a base cobre ~2 dias; ainda assim, janelas temporais podem separar comportamentos (ex.: rajadas de transações suspeitas).

Não testamos subconjuntos nesta fase — o objetivo era um baseline completo antes de refinar na Semana 3.

## 4. Padronização — `StandardScaler` (média 0, desvio 1)

**Por quê:**

K-Means usa distância euclidiana: soma diferenças ao quadrado entre atributos.

`Amount` vai até ~25.000 e `Time` até ~172.000; `V1`–`V28` ficam em torno de 0 com desvio ~1–2.

Sem padronização, `Amount` e `Time` dominiriam a distância e os clusters seriam quase “grupos por valor/tempo”, ignorando o restante.

`StandardScaler` coloca todas as features na mesma escala, para cada uma contribuir de forma equilibrada.

## 5. Distância — Euclidiana (padrão do K-Means)

**Por quê:**

K-Means minimiza a soma das distâncias ao quadrado dos pontos aos centróides — isso é distância euclidiana no espaço das features padronizadas.

É a escolha padrão e esperada para baseline: simples, rápida e adequada quando os clusters são aproximadamente esféricos e comparáveis em escala (por isso a padronização antes).

Alternativas (Manhattan, cosseno) ficam para comparação futura; na Semana 2 o foco é primeiro algoritmo funcionando.

## 6. K-Means — `k` de 2 a 10; `k = 6` (maior Silhouette)

**Por quê:**

`k` muito baixo (2–3): clusters genéricos demais; mistura perfis distintos.

`k` muito alto (9–10): fragmenta os dados; clusters pequenos e instáveis; Silhouette não melhora de forma consistente.

Usamos dois critérios:

- Elbow (inércia): onde o ganho de reduzir inércia começa a diminuir.
- Silhouette: mede se pontos estão coesos no próprio cluster e afastados dos outros — quanto maior, melhor.

`k = 6` teve o maior Silhouette (0,0863) na amostra testada → escolha data-driven, não arbitrária.

Silhouette foi calculado em amostra de 20.000 pontos por custo computacional (O(n²)), mas o K-Means final foi treinado na base completa.

## 7. Visualizações — Elbow, Silhouette, fraude por cluster, `Amount` por cluster

**Por quê:**

Elbow + Silhouette: justificam visualmente a escolha de `k` (requisito acadêmico + transparência).

Taxa de fraude por cluster: é o insight central do projeto — ver se algum grupo concentra mais fraudes que 0,17%.

`Amount` por cluster: liga agrupamento a interpretação de negócio (ex.: cluster 3 com `Amount` médio ~US$ 1.550 vs. cluster 5 ~US$ 40).

Atendem ao requisito de “pelo menos uma visualização” e apoiam a análise escrita.

## 8. Análise dos clusters — taxa de fraude vs. média global (0,17%)

**Por quê:**

Clustering é não supervisionado — não otimiza fraude diretamente.

A única forma honesta de avaliar utilidade nesta fase é cruzar cluster (gerado sem `Class`) com `Class` depois:

- Se todos os clusters tivessem ~0,17%, o agrupamento não ajudaria na detecção.
- Clusters 3, 4 e 5 acima da média (até 3,9× no cluster 5) indicam que o baseline já separa sinal de risco — argumento para usar cluster como feature na Semana 4.

## 9. Problemas identificados — Silhouette 0,0863; K-Means esférico; fraudes raras se diluem

**Por quê registrar isso:**

Silhouette 0,0863 (perto de 0): clusters sobrepostos, fronteiras pouco nítidas — agrupamento “funciona”, mas não é excelente em separação geométrica.

K-Means assume clusters esféricos e tamanhos parecidos: fraudes são anomalias raras (0,17%) — tendem a ficar dentro de clusters grandes de transações legítimas, não formar bolhas próprias.

Fraudes se diluem: ex.: cluster 2 tem 44,6% das transações e taxa de fraude abaixo da média — o algoritmo agrupa “comportamento normal em massa”, não “fraude isolada”.

Isso não invalida o baseline; explica limitações e motiva a Semana 3 (DBSCAN) para anomalias e comparação de algoritmos.
