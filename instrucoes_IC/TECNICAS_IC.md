# Técnicas de IC

## Objetivo
Descrever o problema de fraude em ambientes com desbalanceamento extremo de classes e fundamentar as decisões teóricas do projeto. O cenário de detecção de fraudes financeiras é caracterizado por um severo desequilíbrio estatístico: na base Credit Card Fraud Detection (Kaggle), existem apenas 492 instâncias fraudulentas em um universo de 284.807 transações (aproximadamente 0,17% do total).

Modelos preditivos tradicionais expostos a esse nível de desbalanceamento convergem para a classificação da classe majoritária, apresentando uma falsa alta acurácia global enquanto falham completamente em identificar o risco real.

---

## Problema Central: Desbalanceamento Extremo de Classes

O cenário é caracterizado por:
- **Desproporção severa**: 0,17% de transações fraudulentas vs. 99,83% legítimas
- **Risco de viés**: Modelos que ignoram fraudes obtêm alta acurácia global (ex: 99,83% classificando tudo como legítimo)
- **Impacto financeiro**: Falsos negativos representam perdas diretas; falsos positivos, custos operacionais

---

## Estratégias de Mitigação do Desbalanceamento

### 1. SMOTE (Synthetic Minority Over-sampling Technique)
- **Resumo**: Algoritmo de sobreamostragem que cria instâncias sintéticas da classe minoritária (fraude) através de interpolação de vizinhos mais próximos (KNN)
- **Vantagens**: Evita overfitting por simples duplicação de registros
- **Limitações**: Pode introduzir ruído nas fronteiras de decisão

### 2. Class Weight (Pesos de Classes Penalizados)
- **Resumo**: Modificação direta na função de custo do algoritmo de aprendizado
- **Vantagens**: Atribui peso inversamente proporcional à frequência da classe, punindo severamente erros em fraudes
- **Limitações**: Requer ajuste cuidadoso de hiperparâmetros

### 3. Amostragem Estratificada (Stratified K-Fold)
- **Resumo**: Garantia metodológica na divisão dos dados de treino e teste
- **Vantagens**: Mantém proporção original (0,17%) em todas as dobras de validação cruzada
- **Limitações**: Não elimina o desbalanceamento, apenas o preserva de forma estruturada

---

## Análise Comparativa de Técnicas Científicas de IC

| Técnica | Vantagens no Contexto de Fraude | Desvantagens / Desafios |
|---------|----------------------------------|------------------------|
| **Random Forest (Floresta Aleatória)** | Altamente robusto contra overfitting; manipula bem distribuições desbalanceadas através do isolamento de subamostras; provê métricas nativas de importância de atributos | Pode se tornar computacionalmente lento para inferência em tempo real; consome muita memória com bases massivas |
| **Redes Neurais Artificiais** | Extrema capacidade de capturar relações não-lineares e padrões complexos de comportamento financeiro | Exige grande volume de dados; risco severo de sobreajuste na classe majoritária; natureza de 'caixa-preta' (baixa explicabilidade) |
| **SVM (Support Vector Machines)** | Excelente capacidade de generalização espacial através de Kernel; foca na maximização das margens de decisão | Custo computacional proibitivo para bases muito extensas (complexidade quadrática); sensível a ruídos introduzidos por sobreamostragem |

---

## Técnica Escolhida: Random Forest

### Justificativa Preliminar
Com base no levantamento, a recomendação inicial pende para o uso de **Random Forest** devido à:
- Estabilidade nativa com dados desbalanceados
- Capacidade de extrair importância das features
- Desempenho computacional adequado para o escopo do projeto

### Alternativa Complementar
Arquiteturas de **Redes Neurais do tipo Autoencoder** (aprendizado não supervisionado focado no erro de reconstrução da classe legítima) despontam como uma abordagem inovadora e cientificamente rica para complementar o agrupamento.

---

## Métricas Críticas de Avaliação

⚠️ **PROIBIÇÃO METODOLÓGICA**: Sob hipótese alguma a **Acurácia Global** deverá ser utilizada como métrica de sucesso neste projeto. Um modelo estúpido que classifique 100% das transações como legítimas obteria 99,83% de acurácia na base do Kaggle, operando um desastre financeiro real.

### Métricas Mandatórias

**AUC-ROC (Area Under the Receiver Operating Characteristic Curve)**
- Avalia a capacidade global do modelo em discriminar entre transações legítimas e fraudulentas
- Independente do limiar de probabilidade adotado
- Métrica robusta para datasets desbalanceados

**F1-Score (Média Harmônica)**
- Média harmônica entre Precisão e Recall
- Garante equilíbrio forçado entre as duas métricas
- Penaliza modelos que otimizam apenas uma das pontas

**Precisão (Precision)**
- Percentual de alertas gerados que eram fraudes reais
- Crucial para mensurar o custo operacional de falsos positivos

**Recall (Sensibilidade)**
- Percentual de fraudes reais que foram interceptadas pelo sistema
- **Métrica mais crítica** para mitigar o prejuízo financeiro direto

**Matriz de Confusão & Curva Precision-Recall**
- Ferramentas visuais indispensáveis para mapear a distribuição exata dos erros
- Focus especial na curva PR dada a raridade da classe positiva
- Permite visualizar trade-offs entre falsos alarmes e fraudes perdidas

---

## Integração com Clusters

### ✅ Decisão Formalizada (Semana 2)

**Estratégia:** Opção 3 (comparar modelo COM vs. SEM clusters) com implementação via Opção 1 (rótulo `cluster` como feature).

| Opção | Status |
|-------|--------|
| Opção 1 — cluster como feature | ✅ Adotada (braço híbrido) |
| Opção 2 — submodelos por cluster | ❌ Descartada |
| Opção 3 — contraste baseline vs. híbrido | ✅ Adotada (experimento principal) |

### Evidência da Semana 2 (K-Means, k=6)

O clustering já separa fraudes acima do acaso. Clusters de alto risco identificados:

| Cluster | Taxa de fraude | vs. global (0,173%) |
|---------|----------------|---------------------|
| 3 | 0,246% | 1,5× |
| 4 | 0,372% | 2,2× |
| **5** | **0,648%** | **3,9×** |

Coluna produzida por Ruan: `cluster` (int, 0–5). Detalhes em `instrucoes_IC/PLANO_IC.md`.

---

## Próximos Passos

- [x] Confirmar Random Forest como técnica padrão
- [x] Definir estratégia de mitigação: `class_weight='balanced'` (primária) + SMOTE (experimento opcional)
- [x] Definir split: Stratified train/test + Stratified K-Fold
- [x] Formalizar integração clustering + IC (Opção 3 + Opção 1)
- [ ] Semana 3: avaliar em `notebooks/semana_3_comparacao.ipynb` se DBSCAN melhora separação vs. K-Means
- [ ] Semana 4: treinar Random Forest baseline vs. híbrido e comparar AUC-ROC / F1
- [ ] Instalar `imbalanced-learn` se for testar SMOTE (`pip install imbalanced-learn`)
