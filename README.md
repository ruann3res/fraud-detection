# Detecção de Fraude em Transações Financeiras

**Trabalho Final Integrador**  
Disciplina: Tópicos Especiais 2 - Agrupamento de Dados e Inteligência Computacional

---

## Visão Geral

Este projeto investiga detecção de fraudes em transações financeiras usando uma combinação de:

- análise exploratória e preparação de dados;
- agrupamento de dados com K-Means e DBSCAN;
- comparação e interpretação dos clusters;
- integração dos clusters com modelos de Inteligência Computacional.

O cenário escolhido é **Detecção de Fraude ou Transações Financeiras Suspeitas**, usando a base **Credit Card Fraud Detection**.

---

## Estrutura Atual do Projeto

```text
fraud-detection/
├── README.md
├── INICIO_AQUI.md
├── GUIA_GIT_PUSH.md
├── PROBLEMA.md
├── RESUMO_ARQUIVOS_CRIADOS.md
├── Trabalho_Final_AgrupamentoDeDados_InteligênciaComputacional.docx (1).pdf
├── pyproject.toml
├── uv.lock
├── checklist_semanal/
│   ├── CHECKLIST_SEMANA_1.md
│   ├── CHECKLIST_SEMANA_2.md
│   └── CHECKLIST_SEMANA_3.md
├── dados/
│   └── creditcard.csv
├── instrucoes_IC/
│   ├── Documentacao_Referencia_IC.pdf
│   ├── PLANO_IC.md
│   └── TECNICAS_IC.md
├── notebooks/
│   ├── README.md
│   ├── Semana_1_EDA_e_Preparacao.ipynb
│   ├── semana_2_clustering_baseline.ipynb
│   └── semana_3_comparacao.ipynb
├── relatorio/
│   ├── README.md
│   ├── relatorio_semana_2.md
│   └── relatorio_semana_3.md
└── scripts/
    └── README.md
```

---

## Divisão de Papéis

| Aluno | Papel | Responsabilidades |
|-------|-------|-------------------|
| **Ruan** | Agrupamento de Dados | Implementação técnica em Python, preprocessing, K-Means, DBSCAN, avaliação dos clusters |
| **Lucio** | Dados, Pipeline e Integração | Organização do repositório, documentação da base, análise exploratória, integração dos entregáveis |
| **Artur** | Inteligência Computacional e Decisão | Técnicas de IC, métricas, desbalanceamento, integração clustering + modelo supervisionado |

---

## Como Começar

### 1. Preparar o ambiente

O projeto usa Python 3.12 ou superior, conforme `pyproject.toml`.

```bash
python -m venv venv
venv\Scripts\activate
pip install pandas numpy matplotlib seaborn scikit-learn jupyter
```

Se estiver usando `uv`:

```bash
uv sync
```

### 2. Conferir a base de dados

O arquivo esperado é:

```text
dados/creditcard.csv
```

A base pode ser obtida em: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

### 3. Abrir os notebooks

```bash
jupyter notebook
```

Ordem sugerida:

1. `notebooks/Semana_1_EDA_e_Preparacao.ipynb`
2. `notebooks/semana_2_clustering_baseline.ipynb`
3. `notebooks/semana_3_comparacao.ipynb`

---

## Entregas por Semana

### Semana 1 - EDA e Preparação

Arquivos principais:

- `notebooks/Semana_1_EDA_e_Preparacao.ipynb`
- `checklist_semanal/CHECKLIST_SEMANA_1.md`
- `PROBLEMA.md`

Entrega:

- definição do problema;
- entendimento da base;
- análise exploratória;
- tratamento de ausentes e duplicidades;
- identificação de outliers;
- preparação para clustering.

### Semana 2 - Agrupamento I: Representação, Distância e Baseline

Arquivos principais:

- `notebooks/semana_2_clustering_baseline.ipynb`
- `checklist_semanal/CHECKLIST_SEMANA_2.md`
- `relatorio/relatorio_semana_2.md`

Entrega:

- seleção e justificativa dos atributos;
- normalização/padronização;
- definição da distância;
- K-Means como primeiro baseline;
- visualização e análise inicial dos clusters;
- identificação de problemas no agrupamento inicial.

### Semana 3 - Agrupamento II: Comparação, Validação e Interpretação

Arquivos principais:

- `notebooks/semana_3_comparacao.ipynb`
- `checklist_semanal/CHECKLIST_SEMANA_3.md`
- `relatorio/relatorio_semana_3.md`

Entrega:

- aplicação de DBSCAN como segundo algoritmo;
- comparação com K-Means;
- uso de métricas como Silhouette, Davies-Bouldin e Calinski-Harabasz;
- análise de parâmetros;
- interpretação e nomeação dos perfis;
- geração de estrutura de saída para uso em IC.

Resultado consolidado:

- K-Means mantido como estrutura principal de segmentação;
- DBSCAN usado como sinal complementar de anomalia;
- `cluster_kmeans_semana3` definido como feature categórica;
- `dbscan_ruido` definido como indicador binário para a etapa de IC.

### Semana 4 - Inteligência Computacional I

Arquivos de apoio:

- `instrucoes_IC/TECNICAS_IC.md`
- `instrucoes_IC/PLANO_IC.md`

Entrega esperada:

- construção do modelo supervisionado;
- uso dos clusters como features;
- tratamento do desbalanceamento;
- comparação preliminar com e sem clusters.

### Semana 5 - Integração Final

Pasta prevista:

- `relatorio/`

Entrega esperada:

- refinamento do modelo;
- análise final dos resultados;
- relatório técnico;
- apresentação.

---

## Sobre a Base de Dados

- **Tamanho:** 284.807 transações
- **Fraudes:** 492 transações, aproximadamente 0,17%
- **Features:** `V1` a `V28`, `Time`, `Amount`, `Class`
- **Classe alvo:** `Class`, com `0` para legítima e `1` para fraude

Observações importantes:

- `V1` a `V28` são componentes PCA anonimizados.
- `Amount` e `Time` são as variáveis interpretáveis.
- A base é extremamente desbalanceada.
- Outliers não devem ser removidos automaticamente, pois podem representar fraudes.

---

## Estratégia Técnica

### Agrupamento

- **K-Means:** baseline de clustering da Semana 2.
- **DBSCAN:** segundo algoritmo da Semana 3, útil para ruído e anomalias.
- **Decisão Semana 3:** usar K-Means para perfis e DBSCAN como indicador de ruído/anomalia.
- **Validação:** métricas internas e análise externa usando `Class` apenas após o agrupamento.

### Inteligência Computacional

Plano atual:

- usar Random Forest como técnica supervisionada principal;
- testar modelos com e sem variáveis de cluster;
- usar `class_weight='balanced'` e, se necessário, SMOTE como experimento;
- priorizar AUC-ROC, F1-Score, Recall, Precision e curva Precision-Recall.

Detalhes em `instrucoes_IC/PLANO_IC.md` e `instrucoes_IC/TECNICAS_IC.md`.

---

## Métricas Importantes

Para clustering:

- Silhouette Score;
- Davies-Bouldin;
- Calinski-Harabasz;
- distribuição de fraudes por cluster.

Para classificação de fraude:

- AUC-ROC;
- F1-Score;
- Recall;
- Precision;
- Confusion Matrix;
- Precision-Recall Curve.

Não usar acurácia como métrica principal, pois a base é muito desbalanceada.

---

## Status Atual

- Semana 1 documentada e com notebook em `notebooks/`.
- Semana 2 documentada com checklist, relatório e baseline K-Means.
- Semana 3 documentada com checklist, relatório e comparação K-Means vs. DBSCAN.
- Documentos de IC estão em `instrucoes_IC/`.
- Próximo foco: Semana 4, integração dos clusters ao modelo supervisionado.

---

**Última atualização:** 15 de junho de 2026  
**Status:** Estrutura atualizada até a Semana 3
