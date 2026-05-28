# 🚨 Detecção de Fraude em Transações Financeiras

**Trabalho Final Integrador - Semana 1**  
Disciplina: Tópicos Especiais 2 - Agrupamento de Dados e Inteligência Computacional

---

## 📋 Informações do Projeto

- **Cenário:** 4 - Detecção de Fraude ou Transações Financeiras Suspeitas
- **Grupo:** Ruan, Lucio e Artur
- **Base de Dados:** Credit Card Fraud Detection (Kaggle)
- **Linguagem:** Python
- **Período:** 5 semanas

---

## 👥 Divisão de Papéis

| Aluno | Papel | Responsabilidades |
|-------|-------|-------------------|
| **Ruan** | Agrupamento de Dados | • Implementação técnica em Python<br>• Preprocessamento de dados<br>• Detecção de outliers<br>• Clustering (K-Means, DBSCAN)<br>• Avaliação de clusters |
| **Lucio** | Dados, Pipeline e Integração | • Escolha e documentação da base<br>• Análise exploratória<br>• Organização do repositório<br>• Documentação técnica<br>• Decisões de dados |
| **Artur** | Inteligência Computacional e Decisão | • Pesquisa de técnicas de IC<br>• Modelagem preditiva<br>• Tratamento de desbalanceamento<br>• Seleção de métricas<br>• Integração clustering + IC |

---

## 📦 Estrutura do Repositório

```
fraud-detection/
├── README.md                                    # Este arquivo
├── Trabalho_Final_Agrupamento...pdf            # Especificações do trabalho
├── Semana_1_EDA_e_Preparacao.ipynb            # Notebook da Semana 1
├── dados/
│   └── creditcard.csv                          # Base de dados (a baixar)
├── notebooks/
│   ├── semana_2_clustering_baseline.ipynb      # Clustering I
│   ├── semana_3_clustering_validacao.ipynb     # Clustering II
│   ├── semana_4_ic_modelo.ipynb                # IC I
│   └── semana_5_integracao_final.ipynb         # IC II + Integração
├── scripts/
│   ├── preprocessing.py                         # Funções de preprocessamento
│   ├── clustering.py                            # Funções de clustering
│   └── metrics.py                               # Funções de avaliação
└── relatorio/
    ├── relatorio_tecnico.md                    # Relatório final
    └── slides.pptx                             # Apresentação final
```

---

## 🚀 Como Começar

### 1. Configurar o Ambiente

```bash
# Clonar o repositório
git clone <URL-do-repositorio>
cd fraud-detection

# Criar ambiente virtual (opcional, recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install pandas numpy matplotlib seaborn scikit-learn jupyter
```

### 2. Baixar a Base de Dados

1. Ir para: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
2. Fazer download de `creditcard.csv`
3. Descompactar em `dados/creditcard.csv`

```bash
# Verificar se o arquivo está no lugar certo
ls dados/creditcard.csv
```

### 3. Executar o Notebook da Semana 1

```bash
# Iniciar Jupyter
jupyter notebook

# Abrir: Semana_1_EDA_e_Preparacao.ipynb
# Executar todas as células (Kernel > Run All)
```

---

## 📅 Timeline de Entregas

### ✅ Semana 1 (ATUAL)
**Entrega:** Base tratada, entendimento do problema e preparação inicial

**O que vocês têm que fazer:**

1. **Lucio:**
   - [ ] Criar/organizar repositório GitHub
   - [ ] Baixar e documentar a base de dados
   - [ ] Executar seções 1-4 do notebook
   - [ ] Documentar problema e pergunta de negócio
   - [ ] Documentar divisão de papéis

2. **Ruan:**
   - [ ] Executar seções 2-10 do notebook
   - [ ] Implementar tratamento de ausentes
   - [ ] Implementar tratamento de duplicidades
   - [ ] Detectar e documentar outliers
   - [ ] Preparar dados para próxima etapa

3. **Artur:**
   - [ ] Pesquisar técnicas de detecção de fraude
   - [ ] Documentar desafios de desbalanceamento
   - [ ] Listar métricas apropriadas (AUC-ROC, F1-score, etc)
   - [ ] Planejar integração clustering + IC

### 📅 Semana 2
Agrupamento de Dados I: representação, distância e baseline
- Seleção de atributos
- Normalização
- Aplicar K-Means
- Análise inicial dos clusters

### 📅 Semana 3
Agrupamento de Dados II: comparação, validação e interpretação
- Aplicar DBSCAN
- Comparar algoritmos
- Calcular métricas de avaliação
- Interpretar clusters

### 📅 Semana 4
Inteligência Computacional I: construção do modelo inteligente
- Construir modelo preditivo
- Integrar clusters como features
- Avaliação preliminar
- Comparação com/sem clusters

### 📅 Semana 5
Inteligência Computacional II e integração final
- Refinamento do modelo
- Demonstração prática
- Relatório técnico
- Apresentação final

---

## 🔍 O que está pronto no Notebook?

O notebook `Semana_1_EDA_e_Preparacao.ipynb` já contém:

✅ Seção 1: Descrição do problema e base de dados  
✅ Seção 2: Importações e configurações  
✅ Seção 3: Carregamento da base  
✅ Seção 4: Análise exploratória inicial (EDA)  
✅ Seção 5: Tratamento de valores ausentes  
✅ Seção 6: Tratamento de duplicidades  
✅ Seção 7: Identificação de outliers  
✅ Seção 8: Transformação de variáveis categóricas  
✅ Seção 9: Descrição dos atributos  
✅ Seção 10: Correlações e padrões  
✅ Seção 11: Status final e próximas etapas  

---

## 📊 Sobre a Base de Dados

### Características
- **Tamanho:** 284.807 transações
- **Fraudes:** 492 transações (0.17%)
- **Período:** ~2 dias (setembro de 2013)
- **Features:** V1-V28 (PCA) + Amount + Time + Class
- **Desafio:** ALTAMENTE DESBALANCEADA!

### Atributos
- **Time:** Segundos desde primeira transação
- **V1-V28:** Componentes PCA (confidencial)
- **Amount:** Valor da transação em dólar
- **Class:** 0 (legítima) ou 1 (fraude)

### Desafios Principais
1. Desbalanceamento extremo (99.83% vs 0.17%)
2. Necessário usar métricas apropriadas
3. Features PCA não têm interpretação direta
4. Base cobre período curto (~2 dias)

---

## 🛠️ Requisitos Técnicos

### Bibliotecas Python Necessárias
```
pandas>=1.3.0          # Manipulação de dados
numpy>=1.20.0          # Computação numérica
matplotlib>=3.4.0      # Visualização
seaborn>=0.11.0        # Visualização avançada
scikit-learn>=0.24.0   # Machine learning
jupyter>=1.0.0         # Notebooks interativos
```

### Versão Python
- Python 3.8 ou superior recomendado

---

## 📝 Notas Importantes

### ⚠️ Para Ruan (Agrupamento):
- **Semana 2:** Foque em normalização e K-Means como baseline
- **Semana 3:** DBSCAN é IDEAL para detectar fraudes (outliers/anomalias)
- **Métrica importante:** Silhouette Score para validação
- **Desafio:** Dados PCA transformados - não há interpretação direta

### ⚠️ Para Lucio (Dados):
- **Semana 1:** Documentação clara é essencial
- **Base:** Decisão entre Kaggle ou UCI - Kaggle é mais clara
- **Repositório:** Use Git commits bem documentados
- **Análise:** Mostre correlações e padrões iniciais

### ⚠️ Para Artur (IC):
- **Desbalanceamento:** NÃO usar Acurácia! Use AUC-ROC, F1-score, Precision-Recall
- **Semana 4:** Considerar técnicas como:
  - Random Forest
  - Redes Neurais
  - SVM para anomalias
- **Integração:** Clusters como features + variáveis originais = melhor performance

---

## 🎯 Critérios de Sucesso - Semana 1

**Entrega deve conter:**

- ✅ Notebook executável com todas as seções
- ✅ Base carregada e documentada
- ✅ Análise exploratória com gráficos
- ✅ Tratamento de ausentes (0 valores NaN)
- ✅ Duplicidades removidas
- ✅ Outliers identificados e documentados
- ✅ Divisão de papéis clara
- ✅ Repositório Git com commits organizados
- ✅ Documentação em markdown

---

## 📚 Referências

### Bases de Dados
- Credit Card Fraud Detection: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
- Default of Credit Card Clients: https://archive.ics.uci.edu/ml/datasets/default%2Bof%2Bcredit%2Bcard%2Bclients

### Técnicas Recomendadas
- K-Means: Agrupar padrões de comportamento
- DBSCAN: Detectar anomalias/fraudes
- Random Forest: Classificação de fraude
- Neural Networks: Modelagem não-linear

### Métricas para Desbalanceamento
- AUC-ROC (Receiver Operating Characteristic)
- F1-Score (Harmonic mean de Precision e Recall)
- Precision-Recall Curve
- Confusion Matrix

---

## ❓ Dúvidas Frequentes

**P: Preciso remover os outliers em Amount?**  
R: Não! Outliers em Amount podem ser fraudes. Mantenha para análise posterior.

**P: Os dados estão muito desbalanceados, o que fazer?**  
R: Isso é normal. Semana 4 vocês aprenderão técnicas como SMOTE ou class_weight.

**P: Como interpretar features V1-V28?**  
R: São componentes PCA - já transformadas. Foco em Amount, Time e Class.

**P: Quando usar K-Means vs DBSCAN?**  
R: K-Means para clusters gerais. DBSCAN para detectar anomalias (MELHOR para fraude!).

**P: A pasta dados/ não aparece no GitHub?**  
R: ✅ Correto! `.gitignore` ignora `.csv` files. CSV fica local, não sobe online (160MB).

---

## 📞 Contato e Suporte

- **Notebook dúvidas:** Consultar seção "Notas e Observações"
- **Problema técnico:** Verificar imports e versões das bibliotecas
- **Dataset:** Qualquer dúvida, consultar documentação do Kaggle

---

## 📄 Licença e Atribuição

- Dataset: Kaggle MLG ULB - Crédito aos autores originais
- Trabalho: IFTM, Período 5, 2024-2025
- Professores: Dr. Gustavo Prado e Dr. Clarimundo Machado

---

**Última atualização:** 28 de maio de 2026  
**Status:** Semana 1 - Iniciado ✅
