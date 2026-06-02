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
Os dados serão enriquecidos com rótulos de clustering gerados por K-Means ou DBSCAN, conforme a estratégia de integração escolhida.

### Dados de Treino e Validação
- Utilização de **Amostragem Estratificada (Stratified K-Fold)** para garantir proporção original de 0,17% de fraudes em todas as dobras
- Aplicação de **SMOTE** e/ou **Class Weights** para mitigação do desbalanceamento
- Divisão treino/teste mantendo a proporção de classes

---

## Estratégias de Integração: Agrupamento + Inteligência Computacional

O grupo deve deliberar e formalizar a escolha de **uma das três opções**:

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

## Métricas de Avaliação

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

## Cronograma Detalhado: Semanas 4-5

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

### Decisões Pendentes (Fim da Semana 1)
1. **Definição da Abordagem de Integração**: Qual das opções (1, 2 ou 3) utilizaremos como arquitetura padrão?
2. **Validação da Técnica de IC**: Confirmaremos Random Forest pela explicabilidade facilitada ou faremos uso de uma Rede Neural de detecção de novidades?
3. **Infraestrutura**: Todos os integrantes devem possuir as bibliotecas `scikit-learn` e `imblearn` operacionais em seus ambientes de desenvolvimento.

### Possíveis Desafios
- Performance computacional de Random Forest com base massiva
- Ruído introduzido por SMOTE nas fronteiras de decisão
- Explicabilidade reduzida se optar por Redes Neurais
- Consistência de clusters entre diferentes execuções (K-Means é estocástico)