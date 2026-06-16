# CHECKLIST - SEMANA 2

**Projeto:** Deteccao de Fraude em Transacoes Financeiras  
**Tema:** Agrupamento de Dados I: representacao, distancia e baseline  
**Produto esperado:** Primeiro modelo de agrupamento funcionando, ainda que seja um baseline.  
**Status:** Em Progresso

---

## Objetivo da Semana

Construir o primeiro pipeline de agrupamento do projeto, partindo dos dados preparados na Semana 1. Nesta etapa, o foco nao e encontrar o modelo final, mas criar um baseline claro, executavel e bem documentado para servir de comparacao nas proximas semanas.

---

## Entrega Obrigatoria

- [ ] Selecao dos atributos para agrupamento
- [ ] Justificativa dos atributos escolhidos
- [ ] Normalizacao ou padronizacao dos dados
- [ ] Definicao da medida de distancia ou similaridade
- [ ] Aplicacao do primeiro algoritmo de agrupamento
- [ ] Aplicacao de pelo menos uma visualizacao dos dados
- [ ] Analise inicial dos clusters
- [ ] Identificacao de problemas no agrupamento inicial

---

## Arquivo Principal da Semana

- [ ] Criar ou atualizar o notebook `notebooks/semana_2_clustering_baseline.ipynb`
- [ ] Usar como entrada a base limpa/preparada na Semana 1
- [ ] Registrar conclusoes em celulas Markdown, nao apenas em codigo
- [ ] Garantir que o notebook execute do inicio ao fim sem erros

---

## RUAN - Agrupamento de Dados | Implementacao em Python

### Preparacao

- [ ] Atualizar o repositorio local com `git pull`
- [ ] Verificar se `dados/creditcard.csv` existe localmente
- [ ] Conferir se as dependencias estao instaladas:
  ```bash
  pip install pandas numpy matplotlib seaborn scikit-learn jupyter
  ```
- [ ] Criar ou abrir `notebooks/semana_2_clustering_baseline.ipynb`

### Selecao de Atributos

- [ ] Separar a coluna `Class` para analise posterior, sem usa-la como entrada do clustering
- [ ] Definir o conjunto inicial de atributos para agrupamento
- [ ] Recomendacao para baseline:
  - `V1` a `V28`
  - `Amount`
  - `Time`, se for usada com cuidado e padronizada
- [ ] Testar pelo menos uma versao simples:
  - Apenas `V1` a `V28`
  - `V1` a `V28` + `Amount`
- [ ] Documentar a escolha dos atributos no notebook

### Normalizacao ou Padronizacao

- [ ] Aplicar `StandardScaler` ou `RobustScaler`
- [ ] Justificar a escolha do scaler
- [ ] Evitar rodar K-Means com `Amount` e `Time` sem escala
- [ ] Conferir se o resultado final nao possui valores ausentes ou infinitos

### Distancia ou Similaridade

- [ ] Definir a medida usada no baseline
- [ ] Para K-Means, documentar que o algoritmo usa distancia euclidiana
- [ ] Explicar por que distancia euclidiana faz sentido apos padronizacao
- [ ] Registrar limitacoes da distancia escolhida

### Primeiro Algoritmo de Agrupamento

- [ ] Aplicar K-Means como baseline inicial
- [ ] Testar valores simples de `k`, por exemplo `k=2`, `k=3` e `k=5`
- [ ] Fixar `random_state` para reprodutibilidade
- [ ] Salvar os rotulos dos clusters em uma coluna, por exemplo `cluster_kmeans`
- [ ] Comparar a distribuicao de transacoes por cluster
- [ ] Verificar se algum cluster concentra mais fraudes usando `Class` apenas para analise

### Visualizacao dos Dados

- [ ] Aplicar pelo menos uma tecnica de reducao de dimensionalidade:
  - PCA para 2 componentes
  - Opcional: t-SNE ou UMAP, se houver tempo
- [ ] Gerar grafico 2D colorido por cluster
- [ ] Gerar grafico 2D colorido por `Class` para comparar com fraude real
- [ ] Garantir titulos, legendas e eixos legiveis

### Analise Inicial dos Clusters

- [ ] Contar quantidade de registros por cluster
- [ ] Calcular media/mediana de `Amount` por cluster
- [ ] Calcular proporcao de fraudes por cluster usando `Class` apenas como validacao externa
- [ ] Descrever os clusters em linguagem simples
- [ ] Identificar se ha clusters muito grandes ou muito pequenos

### Problemas do Agrupamento Inicial

- [ ] Registrar problemas observados, como:
  - Clusters muito desbalanceados
  - Fraudes espalhadas entre varios clusters
  - K-Means sensivel a outliers
  - Dificuldade de interpretar `V1` a `V28`
  - Separacao visual fraca no PCA
- [ ] Listar melhorias para a Semana 3

---

## LUCIO - Dados, Pipeline e Integracao | Documentacao

### Organizacao da Entrega

- [ ] Verificar se o notebook da Semana 2 esta no caminho correto
- [ ] Atualizar o README se o notebook for criado
- [ ] Conferir se os dados brutos continuam fora do Git
- [ ] Revisar se os graficos e tabelas estao compreensiveis

### Justificativa dos Atributos

- [ ] Revisar a justificativa dos atributos escolhidos
- [ ] Confirmar que `Class` nao foi usada para treinar o agrupamento
- [ ] Explicar que `Class` sera usada apenas para avaliacao posterior dos clusters
- [ ] Documentar qualquer atributo removido e o motivo

### Documentacao Tecnica

- [ ] Registrar o pipeline da Semana 2:
  ```text
  Dados limpos
    -> selecao de atributos
    -> padronizacao
    -> K-Means baseline
    -> visualizacao
    -> analise inicial dos clusters
  ```
- [ ] Garantir que as decisoes estejam escritas em Markdown
- [ ] Conferir se as tabelas de resultados sao suficientes para explicar a entrega

### Revisao Final

- [ ] Rodar o notebook do inicio ao fim
- [ ] Verificar se todos os imports funcionam
- [ ] Conferir se nao ha caminhos absolutos de maquina local
- [ ] Revisar ortografia e clareza da entrega
- [ ] Fazer commit com mensagem clara

---

## ARTUR - Inteligencia Computacional e Decisao | Analise Critica

### Conexao com a Etapa de IC

- [ ] Avaliar se os clusters podem virar features para os modelos das Semanas 4 e 5
- [ ] Verificar se algum cluster tem maior concentracao de fraude
- [ ] Comparar clusters com a variavel `Class`, sem usar `Class` no treinamento do clustering
- [ ] Documentar se o baseline parece util para deteccao de fraude

### Analise dos Resultados

- [ ] Interpretar a distribuicao de fraudes por cluster
- [ ] Identificar se o agrupamento ajuda ou nao a separar comportamento suspeito
- [ ] Registrar limitacoes para uso em modelo supervisionado
- [ ] Sugerir quais experimentos devem ser feitos na Semana 3

### Pontos de Atencao

- [ ] Nao avaliar o clustering apenas por acuracia
- [ ] Lembrar que o dataset e extremamente desbalanceado
- [ ] Observar se um cluster pequeno concentra casos relevantes
- [ ] Evitar conclusoes fortes com base apenas no primeiro baseline

---

## Checklist do Grupo

### Implementacao

- [ ] Notebook `notebooks/semana_2_clustering_baseline.ipynb` criado
- [ ] Dados carregados corretamente
- [ ] Atributos selecionados
- [ ] Justificativa dos atributos documentada
- [ ] Normalizacao/padronizacao aplicada
- [ ] Medida de distancia definida
- [ ] K-Means baseline executado
- [ ] Rotulos de cluster adicionados ao dataframe

### Visualizacao e Analise

- [ ] Pelo menos uma visualizacao 2D criada
- [ ] Distribuicao de registros por cluster analisada
- [ ] Proporcao de fraude por cluster analisada
- [ ] Problemas do baseline documentados
- [ ] Proximos passos para Semana 3 listados

### Qualidade

- [ ] Notebook roda sem erros
- [ ] Codigo esta organizado e comentado quando necessario
- [ ] Graficos possuem titulos e legendas
- [ ] Decisoes metodologicas estao explicadas
- [ ] Commits foram feitos com mensagens claras

---

## Sugestao de Estrutura do Notebook

1. Introducao e objetivo da Semana 2
2. Imports e configuracoes
3. Carregamento dos dados
4. Selecao dos atributos
5. Justificativa dos atributos escolhidos
6. Normalizacao ou padronizacao
7. Definicao da distancia/similaridade
8. K-Means baseline
9. Visualizacao com PCA 2D
10. Analise dos clusters
11. Problemas encontrados
12. Conclusao e proximos passos

---

## Exemplo de Codigo Base

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

df = pd.read_csv("../dados/creditcard.csv")

features = [col for col in df.columns if col.startswith("V")]
features = features + ["Amount"]

X = df[features].copy()
y = df["Class"].copy()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df["cluster_kmeans"] = kmeans.fit_predict(X_scaled)

pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_scaled)

df["pca_1"] = X_pca[:, 0]
df["pca_2"] = X_pca[:, 1]
```

---

## Perguntas para Responder na Entrega

- Quais atributos foram usados no agrupamento?
- Por que esses atributos foram escolhidos?
- Qual tecnica de escala foi usada?
- Qual medida de distancia/similaridade esta implicita no algoritmo?
- Quantos clusters foram gerados?
- Os clusters ficaram equilibrados?
- Algum cluster concentrou mais fraudes?
- O PCA mostrou separacao visual clara?
- Quais problemas apareceram no baseline?
- O que deve ser melhorado na Semana 3?

---

## Criterios de Pronto

A Semana 2 pode ser considerada pronta quando:

- [ ] Existe um notebook executavel com o primeiro clustering
- [ ] A selecao de atributos esta justificada
- [ ] A escala dos dados foi tratada corretamente
- [ ] A distancia/similaridade foi definida
- [ ] O primeiro algoritmo de agrupamento foi aplicado
- [ ] Existe pelo menos uma visualizacao
- [ ] Ha analise inicial dos clusters
- [ ] Os problemas do baseline foram identificados

---

**Ultima atualizacao:** 15 de junho de 2026  
**Status:** Semana 2 - Baseline de agrupamento
