# Plano de IC

## Contexto
Planejamento prático da engenharia de dados, roteiro de integração entre a modelagem não supervisionada (clustering) e supervisionada (IC), e cronograma operacional das Semanas 4 e 5. O objetivo é desenvolver um pipeline integrado que combine técnicas de agrupamento com classificação supervisionada para detecção de fraudes em ambientes com desbalanceamento extremo.

---

## Técnica Proposta

**Random Forest** é a técnica escolhida para modelagem de Inteligência Computacional, com possível complementação por Autoencoders.

### Motivo da Escolha
- Robustez nativa contra overfitting com dados desbalanceados
- Isolamento eficiente de subamostras e construção independente de árvores
- Fornece métricas nativas de importância de atributos para explicabilidade
- Custo computacional adequado para o escopo do projeto

---

## Dados Necessários

### Features de Entrada
- **V1 a V28**: Variáveis já transformadas via PCA para questões de privacidade bancária (tratamento estatístico obrigatório)
- **Time (Tempo)**: Segundos decorridos entre a transação atual e a primeira do dataset (captura janelas temporais de ataques coordenados)
- **Amount (Valor)**: Valor financeiro absoluto envolvido na transação (associa comportamento de risco ao volume monetário)

### Uso de Clusters
Os dados serão enriquecidos com rótulos de clustering gerados por K-Means (Semana 2) e DBSCAN (Semana 3), conforme a estratégia de integração escolhida na Semana 2.

### Formato do Rótulo de Cluster (alinhado com Ruan — Semana 2)
| Campo | Valor |
|-------|-------|
| **Coluna** | `cluster` |
| **Tipo** | `int` (0 a k-1; baseline k=6 → valores 0–5) |
| **Origem** | `KMeans.fit_predict()` sobre features normalizadas |
| **Features de entrada do clustering** | `V1`–`V28`, `Time`, `Amount` (sem `Class`) |
| **Notebook fonte** | `notebooks/semana_2_clustering_baseline.ipynb` |
| **Uso na Semana 4** | Injetado como feature categórica no dataset supervisionado |

### Dados de Treino e Validação
- Utilização de **Amostragem Estratificada (Stratified K-Fold)** para garantir proporção original de 0,17% de fraudes em todas as dobras
- Aplicação de **SMOTE** e/ou **Class Weights** para mitigação do desbalanceamento
- Divisão treino/teste mantendo a proporção de classes

---

## Estratégias de Integração: Agrupamento + Inteligência Computacional

### ✅ Decisão Formalizada (Semana 2 — Artur)

**Estratégia adotada: Opção 3 (Validação por Contraste)**, com implementação do braço
**“com clusters”** via **Opção 1 (rótulo do cluster como feature)**.

| Opção | Papel no projeto | Status |
|-------|------------------|--------|
| **Opção 1** | Mecanismo de integração — coluna `cluster` entra como feature no Random Forest | ✅ Adotada (braço híbrido) |
| **Opção 2** | Submodelos por cluster | ❌ Descartada (complexidade alta para o prazo; clusters desbalanceados) |
| **Opção 3** | Experimento principal — comparar modelo SEM vs. COM `cluster` | ✅ Adotada (estratégia de avaliação) |

**Justificativa da decisão:**
- A Opção 3 gera evidência acadêmica de que o clustering agrega valor à IC.
- A Opção 1 é simples, rastreável e compatível com o formato já produzido por Ruan (`df['cluster']`).
- A Opção 2 foi descartada porque clusters têm tamanhos muito desiguais (ex.: cluster 2 com 44,6% das transações vs. cluster 3 com 1,4%), o que dificulta treinar submodelos estáveis por grupo.

**Como os rótulos da Semana 2 entram no pipeline da Semana 4:**
```
1. Ruan exporta df com coluna `cluster` (K-Means, k=6)
2. Artur monta X com 31 features: V1–V28 + Time + Amount + cluster
3. Artur treina dois Random Forest:
   - Baseline: 30 features (sem cluster)
   - Híbrido:  31 features (com cluster)
4. Compara AUC-ROC e F1-Score entre os dois
5. Semana 3: repetir com rótulos DBSCAN (se melhorar, substituir ou combinar)
```

---

### Opção 1: Rótulo do Cluster como Atributo (Feature Engineering)
- O pipeline de clustering (K-Means/DBSCAN) processa os dados primeiro
- O ID do cluster gerado para cada transação é injetado como **nova coluna categórica** no dataset
- O modelo de IC utiliza essa feature enriquecida para realizar a classificação final
- **Vantagem**: Abordagem simples e rastreável

### Opção 2: Clusters para Definição de Recomendações e Submodelos
- Os dados são **segmentados fisicamente** através dos perfis comportamentais mapeados pelos clusters (ex: perfis de alta frequência, perfis corporativos, perfis sazonais)
- Um modelo específico de IC é treinado **exclusivamente** para atender e monitorar cada um dos clusters individualmente
- **Vantagem**: Maior especificidade por perfil comportamental

### Opção 3: Validação por Contraste (Baseline vs. Híbrido)
- Abordagem focada em **experimentação acadêmica rigorosa**
- Desenvolve-se um modelo puramente supervisionado (**Sem Clusters**)
- Compara-se estatisticamente o seu desempenho contra o modelo híbrido (**Com Clusters**)
- Métricas de comparação: F1-Score e AUC-ROC para provar o ganho real do agrupamento
- **Vantagem**: Fornece evidência científica do valor agregado do clustering

---

## Pipeline de Processamento e Distribuição de Papéis (Semanas 4-5)

```
Dados Brutos
    ↓
Pré-processamento [Responsável: Ruan]
    ↓
Clustering (K-Means/DBSCAN) [Responsável: Ruan]
    ↓
Fusão de Features Originais + Rótulos de Clusters
    ↓
Modelo de Inteligência Computacional [Responsável: Artur]
    ↓
Predição Final + Atribuição de Score de Confiança
```

---

## Infraestrutura Tecnológica e Bibliotecas

Ferramentas no ecossistema Python para sustentação do pipeline:

- **Scikit-Learn**: K-Means, DBSCAN, Random Forest, Árvores de Decisão, funções utilitárias de métricas
- **Imbalanced-Learn (imblearn)**: Implementação nativa do SMOTE e utilitários de amostragem estratificada
- **Pandas & NumPy**: Manipulação matricial de alta performance e engenharia de tabelas
- **Matplotlib & Seaborn**: Visualização de matrizes de confusão e curvas Precision-Recall

---

## Avaliação dos Clusters — Semana 2 (Artur)

Análise sobre o baseline K-Means (k=6) de Ruan. Taxa global de fraude: **0,173%**.

| Cluster | Transações | % do total | Taxa de fraude | vs. média global | Perfil |
|---------|------------|------------|----------------|------------------|--------|
| 0 | 15.716 | 5,5% | 0,000% | 0,0× | Baixo risco — nenhuma fraude detectada |
| 1 | 86.447 | 30,5% | 0,036% | 0,2× | Abaixo da média |
| 2 | 126.518 | 44,6% | 0,123% | 0,7× | Maior cluster; fraude abaixo da média |
| 3 | 4.070 | 1,4% | 0,246% | 1,5× | Alto risco — `Amount` médio elevado (~US$ 1.550) |
| 4 | 19.641 | 6,9% | 0,372% | 2,2× | Alto risco |
| **5** | **31.334** | **11,0%** | **0,648%** | **3,9×** | **Candidato principal a alto risco** |

**Conclusão:** o clustering **já separa fraudes melhor que o acaso**. Clusters **3, 4 e 5** concentram taxas acima da média global; o **cluster 5** é o principal candidato a sinal de risco para o modelo da Semana 4.

> ⚠️ **Métrica proibida:** não usar Acurácia como métrica principal (99,83% classificando tudo como legítimo seria “bom” na acurácia, mas inútil na prática).

---

## Métricas de Avaliação

### ✅ Métricas Confirmadas para Semana 4 (Artur)

| Métrica | Uso | Prioridade |
|---------|-----|------------|
| **AUC-ROC** | Discriminação global legítima vs. fraude | Alta |
| **F1-Score** | Equilíbrio Precision/Recall | Alta |
| **Recall** | Fraudes reais interceptadas | **Crítica** |
| **Precision** | Alertas que eram fraudes de fato | Média |
| **Confusion Matrix** | Distribuição visual de erros | Apoio |
| **Curva Precision-Recall** | Análise focada na classe minoritária | Apoio |
| ~~Acurácia~~ | **Proibida** como métrica principal | — |

### Métricas Principais
- **AUC-ROC**: Capacidade global de discriminação entre legítimas e fraudulentas
- **F1-Score**: Equilíbrio forçado entre Precisão e Recall
- **Recall (Sensibilidade)**: Percentual de fraudes reais interceptadas (métrica mais crítica)

### Métricas de Apoio
- **Precisão**: Percentual de alertas que eram fraudes reais
- **Matriz de Confusão**: Mapeamento visual de erros
- **Curva Precision-Recall**: Análise detalhada com foco na classe minoritária

---

## Comparação com e sem Clusters

### Cenário Sem Clusters
- Modelo supervisionado puro sobre features V1-V28, Time e Amount
- Baseline para avaliação do impacto do clustering

### Cenário Com Clusters
- Modelo supervisionado com enriquecimento de features através dos rótulos de cluster
- Testado conforme a Opção de Integração escolhida (1, 2 ou 3)

### Critério de Comparação
- Comparação estatística de **F1-Score** e **AUC-ROC**
- Análise de custo-benefício de falsos positivos vs. falsos negativos
- Documentação final do ganho real do agrupamento

---

## Estratégia de Desbalanceamento — Confirmada (Artur)

| Técnica | Decisão | Justificativa |
|---------|---------|---------------|
| **Stratified train/test (80/20)** | ✅ Adotada | Mantém ~0,17% de fraudes em treino e teste |
| **Stratified K-Fold (k=5)** | ✅ Adotada | Validação cruzada com proporção de classes preservada |
| **`class_weight='balanced'`** | ✅ Adotada (primária) | Penaliza erros na classe minoritária sem dados sintéticos |
| **SMOTE** | ⚠️ Experimento opcional | Testar na Semana 4; risco de ruído nas fronteiras |

**Split proposto:**
```python
from sklearn.model_selection import train_test_split, StratifiedKFold

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
```

**Modelo confirmado:** Random Forest (`sklearn.ensemble.RandomForestClassifier`) com `class_weight='balanced'`.

---

## Cronograma Revisado: Semanas 3–5

### Semana 3 (Ruan + Artur acompanha)
| Atividade | Responsável | Entregável |
|-----------|-------------|------------|
| DBSCAN e comparação com K-Means | Ruan | Notebook `semana_3_clustering_validacao.ipynb` |
| Avaliar se DBSCAN melhora separação de fraudes | Artur | Atualizar tabela de clusters em `PLANO_IC.md` |
| Decidir rótulo final para Semana 4 (K-Means, DBSCAN ou ambos) | Grupo | Decisão documentada |

### Semana 4

### Semana 4

| Atividade | Responsável | Entregável |
|-----------|-------------|----------|
| Integração das bases pré-processadas | Ruan | Dataset preparado e validado |
| Engenharia de Atributos com inclusão de dados de clusters | Artur | Features enriquecidas prontas |
| Ajuste inicial do modelo de IC sob validação estratificada | Artur | Primeira versão do classificador rodando sobre clusters |

**Entregável Esperado**: Script de fusão de dados concluído; Primeira versão do classificador operacional

### Semana 5

| Atividade | Responsável | Entregável |
|-----------|-------------|----------|
| Otimização refinada de hiperparâmetros (via busca em grid/AG) | Artur | Hiperparâmetros otimizados documentados |
| Extração e plotagem de matrizes de confusão e curvas PR | Artur | Visualizações completas e interpretadas |
| Documentação final comparativa (com e sem agrupamento) | Artur | Relatório de explicabilidade pronto |

**Entregável Esperado**: 
- Pipeline integrado fim a fim
- Gráficos de performance consolidados
- Relatório de explicabilidade do modelo
- Análise comparativa comprovando valor do clustering

---

## Premissas Críticas e Tratamento de Dados

### Compreensão das Variáveis V1-V28
As variáveis V1 a V28 já passaram por transformação matemática via **PCA** por questões de privacidade bancária. Elas não possuem significado de negócio direto interpretável. **O modelo deve tratá-las puramente de forma estatística**.

### Únicas Variáveis Originais Interpretáveis
- **Time**: Segundos decorridos desde a primeira transação (captura ataques coordenados)
- **Amount**: Valor financeiro absoluto (associa risco ao volume)

### ⚠️ PROIBIÇÃO: Não Remover Outliers
Em problemas de fraude bancária, os comportamentos bizarros que fogem do padrão estatístico são, em grande parte das vezes, **as próprias fraudes** que estamos tentando capturar. Eliminar outliers equivaleria a apagar o histórico de fraudes da base de dados.

---

## Riscos e Pendências

### ✅ Decisões Resolvidas (Semana 2 — Artur)
1. **Integração:** Opção 3 (contraste) + Opção 1 (cluster como feature) — formalizado
2. **Técnica de IC:** Random Forest confirmado (`class_weight='balanced'`)
3. **Métricas:** AUC-ROC, F1, Recall, Precision, Confusion Matrix — confirmadas; Acurácia proibida
4. **Split:** Stratified train/test + Stratified K-Fold
5. **Formato do cluster:** coluna `cluster` (int, 0–5) — alinhado com Ruan

### Pendências para Semana 3
1. Comparar rótulos K-Means vs. DBSCAN antes de fixar feature final
2. Instalar `imbalanced-learn` se for testar SMOTE na Semana 4 (`pip install imbalanced-learn`)
3. Lucio: interpretação de negócio dos clusters 3, 4 e 5 para o relatório

### Possíveis Desafios
- Performance computacional de Random Forest com base massiva
- Ruído introduzido por SMOTE nas fronteiras de decisão
- Explicabilidade reduzida se optar por Redes Neurais
- Consistência de clusters entre diferentes execuções (K-Means é estocástico)