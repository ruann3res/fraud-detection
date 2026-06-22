# Relatorio Semana 4 - Inteligencia Computacional I

## 1. Definicao da tarefa de Inteligencia Computacional

A tarefa definida para a Semana 4 foi a construcao de um modelo supervisionado de classificacao binaria para detectar transacoes fraudulentas.

O alvo do modelo e a coluna `Class`, em que:

- `0`: transacao legitima;
- `1`: transacao fraudulenta.

O problema e altamente desbalanceado. Na amostra enriquecida com clusters da Semana 3 foram usados 15.000 registros, sendo 14.975 transacoes legitimas e apenas 25 fraudes, o que representa taxa de fraude de 0,1667%.

Por esse motivo, a acuracia nao foi usada como criterio principal. As metricas escolhidas foram AUC-ROC, Average Precision, Recall, Precision, F1-Score e matriz de confusao.

## 2. Escolha justificada da tecnica

A tecnica escolhida foi Random Forest, conforme planejamento registrado em `instrucoes_IC/PLANO_IC.md` e `instrucoes_IC/TECNICAS_IC.md`.

A escolha e adequada ao contexto do projeto por quatro motivos principais:

- lida bem com relacoes nao lineares entre as variaveis `V1` a `V28`, `Time` e `Amount`;
- permite uso de `class_weight='balanced'`, penalizando mais os erros na classe minoritaria;
- e robusta como modelo inicial, sem exigir grande ajuste manual de hiperparametros;
- permite comparar modelos com e sem variaveis de cluster de forma direta.

O modelo inicial foi implementado com:

```python
RandomForestClassifier(
    n_estimators=200,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1,
)
```

## 3. Preparacao dos dados para o modelo

Foram utilizados dois arquivos:

- `dados/creditcard.csv`: base original de transacoes;
- `dados/saida_clusters_semana3.csv`: saida da Semana 3 com os rotulos de K-Means e DBSCAN.

Como a saida dos clusters possui a coluna `original_index`, a preparacao fez a juncao entre os clusters e a base original pelo indice da transacao. Isso garante que cada rotulo de cluster seja associado a transacao correta.

As features do modelo sem clusters foram:

- `Time`;
- `Amount`;
- `V1` a `V28`.

As features do modelo com clusters foram:

- `Time`;
- `Amount`;
- `V1` a `V28`;
- `cluster_kmeans_semana3`;
- `dbscan_ruido`.

As variaveis de cluster foram tratadas como categoricas e convertidas por one-hot encoding com `pd.get_dummies`. O Random Forest nao exigiu padronizacao das variaveis, pois modelos baseados em arvores nao dependem diretamente da escala euclidiana.

A divisao treino/teste foi estratificada, com 80% para treino e 20% para teste, preservando a proporcao de fraudes. Tambem foi usada validacao cruzada estratificada com 5 folds para avaliacao preliminar.

## 4. Construcao do modelo inicial

Foram construidos dois modelos:

| Modelo | Objetivo |
|---|---|
| Random Forest sem clusters | Baseline supervisionado usando apenas as variaveis originais |
| Random Forest com clusters | Modelo hibrido usando variaveis originais + K-Means + sinal de ruido do DBSCAN |

Essa estrutura segue a estrategia definida nas semanas anteriores: validar por contraste se os agrupamentos agregam valor ao modelo supervisionado.

O codigo reprodutivel foi salvo em:

```text
scripts/semana_4_modelo_ic.py
```

As metricas geradas foram salvas em:

```text
resultados/semana_4_metricas_modelo_ic.csv
```

## 5. Treinamento e execucao da tecnica

O treinamento foi executado com o comando:

```powershell
python scripts\semana_4_modelo_ic.py
```

O script executa as seguintes etapas:

- carrega a base original e a saida dos clusters;
- faz o merge pelo `original_index`;
- monta as matrizes de atributos com e sem clusters;
- divide os dados em treino e teste com estratificacao;
- treina os dois modelos Random Forest;
- calcula metricas no conjunto de teste;
- calcula validacao cruzada estratificada;
- salva os resultados em CSV.

## 6. Avaliacao preliminar

Resultados no conjunto de teste:

| Modelo | AUC-ROC | Average Precision | Recall | Precision | F1 | TN | FP | FN | TP |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Random Forest sem clusters | 0,9990 | 0,6058 | 0,8000 | 0,8000 | 0,8000 | 2994 | 1 | 1 | 4 |
| Random Forest com clusters | 0,9937 | 0,6536 | 0,8000 | 0,8000 | 0,8000 | 2994 | 1 | 1 | 4 |

Nos dois casos, o modelo encontrou 4 das 5 fraudes presentes no conjunto de teste e gerou apenas 1 falso positivo. O resultado e forte para uma versao inicial, mas deve ser interpretado com cautela porque o conjunto de teste possui apenas 5 fraudes.

Resultados medios da validacao cruzada estratificada:

| Modelo | AUC-ROC media | Average Precision media | Recall medio | Precision media | F1 medio |
|---|---:|---:|---:|---:|---:|
| Random Forest sem clusters | 0,9775 | 0,8545 | 0,7200 | 0,9200 | 0,7978 |
| Random Forest com clusters | 0,9376 | 0,8155 | 0,7200 | 0,9200 | 0,7978 |

Na validacao cruzada, os clusters nao melhoraram o F1, Recall ou Precision. O modelo sem clusters apresentou AUC-ROC e Average Precision medias superiores.

## 7. Comparacao inicial com e sem clusters

A comparacao inicial mostra um resultado misto:

- no conjunto de teste, o uso dos clusters manteve Recall, Precision e F1 iguais ao baseline e aumentou levemente o Average Precision;
- na validacao cruzada, o modelo sem clusters teve melhor AUC-ROC media e melhor Average Precision media;
- o sinal de cluster ainda nao demonstrou ganho consistente nesta amostra de 15.000 transacoes.

Portanto, a conclusao preliminar da Semana 4 e que os clusters sao informativos do ponto de vista exploratorio, mas ainda nao comprovaram melhora estavel no classificador supervisionado inicial.

Isso nao invalida o uso dos clusters. A avaliacao ainda esta limitada pela baixa quantidade de fraudes na amostra enriquecida: apenas 25 registros positivos. Na Semana 5, a recomendacao e gerar os rotulos de cluster para a base completa ou testar estrategias adicionais de ajuste de limiar e hiperparametros.

## 8. Produto esperado

O produto da Semana 4 foi entregue como um modelo inteligente funcional em versao inicial.

Entregaveis produzidos:

- definicao da tarefa de IC: classificacao binaria de fraude;
- tecnica escolhida e justificada: Random Forest com `class_weight='balanced'`;
- preparacao dos dados com integracao dos clusters da Semana 3;
- construcao de dois modelos: sem clusters e com clusters;
- treinamento e execucao do pipeline;
- avaliacao preliminar por metricas adequadas ao desbalanceamento;
- comparacao inicial entre baseline supervisionado e modelo hibrido.

## 9. Limitacoes e proximos passos

A principal limitacao e que `dados/saida_clusters_semana3.csv` contem 15.000 registros, nao a base completa. Como ha apenas 25 fraudes na amostra, pequenas mudancas no split podem alterar bastante as metricas.

Para a Semana 5, os proximos passos recomendados sao:

- gerar os clusters para a base completa ou ampliar a amostra estratificada;
- ajustar hiperparametros do Random Forest;
- avaliar limiares de decisao diferentes de 0,5;
- incluir curva Precision-Recall e matriz de confusao como visualizacoes finais;
- analisar importancia das features, incluindo as variaveis de cluster.
