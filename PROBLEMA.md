# 🚨 Definição do Problema - Cenário 4

## Detecção de Fraude em Transações Financeiras

---

## 📋 Problema

Instituições financeiras processam **milhões de transações diariamente** com cartão de crédito. Dessas transações, uma **minúscula fração é fraude** (menos de 0.2%), mas cada fraude representa um prejuízo significativo para o cliente e para o banco.

**O Desafio:** Identificar essas poucas fraudes entre muitas transações legítimas, em tempo real, com alta precisão.

---

## 🎯 Pergunta Central

**Como usar agrupamento para identificar padrões normais e anômalos e apoiar um modelo de detecção de fraude ou risco?**

Ou mais concretamente:
- Como encontrar padrões que diferenciam fraudes de transações legítimas?
- Como usar clustering para melhorar um modelo de predição de fraude?

---

## 📊 Base de Dados

### Informações Gerais
- **Nome:** Credit Card Fraud Detection
- **Fonte:** [Kaggle MLG ULB Dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
- **Total de transações:** 284.807
- **Período:** 2 dias (setembro de 2013)
- **Região:** Europa (cartões de crédito europeu)

### Distribuição de Classes
| Classe | Quantidade | Percentual |
|--------|-----------|-----------|
| Legítima (0) | 284.315 | 99.83% |
| Fraude (1) | 492 | 0.17% |
| **Total** | **284.807** | **100%** |

**Observação:** Base ALTAMENTE DESBALANCEADA - fraudes são muito raras!

### Atributos da Base
- **V1 a V28:** Componentes PCA (transformação de privacidade)
  - Números entre -5 e +5
  - Já normalizados
  - Não têm interpretação direta
  - São as FEATURES principais para análise
  
- **Time:** Segundos desde primeira transação
  - Intervalo: 0 a 172.792 segundos (~2 dias)
  - Pode capturar sazonalidade temporal
  
- **Amount:** Valor da transação em dólar
  - Intervalo: $0,00 a $25.691,16
  - NÃO foi transformado por PCA
  - Única feature com interpretação direta
  
- **Class:** Variável alvo
  - 0 = Transação legítima
  - 1 = Fraude
  - Desbalanceada

---

## ❓ Por Que É Um Problema Importante?

### Relevância Prática
1. **Proteção do cliente:** Evita perdas financeiras do portador do cartão
2. **Proteção da instituição:** Evita reembolsos e chargebacks
3. **Confiança:** Aumenta segurança percebida pelos clientes
4. **Compliance:** Atende regulamentações de segurança financeira

### Relevância Técnica
1. **Desbalanceamento extremo:** Fraudes são 0.17% dos dados
   - Acurácia simples é enganosa (99,83% acertando tudo como legítimo!)
   - Necessário usar métricas apropriadas
   
2. **Problema de anomalia:** Fraudes são ANÔMALAS (padrão diferente)
   - Clustering é excelente para detectar anomalias
   - DBSCAN pode identificar transações "fora do padrão"
   
3. **Features transformadas:** V1-V28 são componentes PCA
   - Privacidade mantida
   - Necessário usar técnicas que funcionem com features abstratas

---

## 🔍 Desafios Principais

### 1️⃣ Desbalanceamento de Classes
- **Problema:** 492 fraudes vs 284.315 legítimas
- **Impacto:** Modelo pode ficar tendencioso
- **Solução:** SMOTE, class weights, stratified sampling, métricas apropriadas

### 2️⃣ Features Abstratas
- **Problema:** V1-V28 são PCA - sem significado direto
- **Impacto:** Difícil interpretar relações de negócio
- **Oportunidade:** Amount e Time são interpretáveis

### 3️⃣ Período Curto
- **Problema:** Base cobre apenas ~2 dias
- **Impacto:** Pode não capturar sazonalidade completa
- **Observação:** Dados históricos completariam análise

### 4️⃣ Métricas Inadequadas
- **Problema:** Acurácia NÃO funciona bem com desbalanceamento
- **Impacto:** Modelo ruim pode parecer bom (99% acurácia!)
- **Solução:** AUC-ROC, F1-Score, Precision-Recall

---

## 💡 O Que Vamos Resolver

### Semana 1
✅ Explorar e preparar os dados
✅ Entender distribuições e padrões
✅ Identificar outliers (possíveis fraudes)

### Semana 2
✅ Encontrar grupos (clusters) de padrões normais com K-Means
✅ Definir baseline de agrupamento
✅ Justificar atributos, escala, distância e problemas iniciais

### Semana 3
✅ Comparar K-Means com DBSCAN
✅ Interpretar e nomear perfis encontrados
✅ Definir `cluster_kmeans_semana3` e `dbscan_ruido` para uso em IC

### Semana 4-5
⬜ Construir modelo preditivo
⬜ Usar clusters como features para melhorar predição
⬜ Demonstrar que clustering melhora detecção de fraude

---

## 🎯 Objetivo Final

Ao final de 5 semanas, vocês entregaram:

1. **Pipeline de dados:** Coleta → Limpeza → Análise
2. **Modelo de clustering:** 2+ algoritmos comparados
3. **Modelo preditivo:** Com e sem clusters
4. **Integração:** Demonstrar que clustering ajuda na predição
5. **Conclusão:** Pode uma transação ser fraude? Com que confiança?

---

## 📈 Fluxo Esperado da Solução

```
Base pública (284.807 transações)
    ↓
Análise exploratória (EDA)
    ↓
Pré-processamento (limpeza, normalização)
    ↓
Agrupamento (K-Means + DBSCAN)
    ↓
Interpretação dos clusters
    ↓
Inteligência Computacional (Random Forest/NN)
    ↓
Predição de fraude / Alerta de risco
    ↓
Decisão: Aprovar, recusar ou exigir verificação?
```

---

## 📝 Resumo Executivo

| Aspecto | Descrição |
|--------|-----------|
| **Cenário** | Detecção de fraude em cartão de crédito |
| **Base de dados** | 284.807 transações em 2 dias |
| **Fraudes** | 492 casos (0.17% - RARAMENTE) |
| **Challenge** | Desbalanceamento + anomalias em dados abstratos |
| **Solução** | Clustering + Predição integrados |
| **Resultado esperado** | Modelo que detecta fraude com alta confiança |
| **Métrica crítica** | AUC-ROC (não Acurácia!) |

---

## 🔗 Referências

- **Dataset:** https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
- **Paper:** Andrea Dal Pozzolo et al., 2015 - Calibrating Probability with Undersampling
- **Contexto:** Kaggle + Université Libre de Bruxelles (ULB) + MLG

---

## ✅ CHECKLIST DE VERIFICAÇÃO

- [x] Problema definido claramente
- [x] Pergunta central documentada  
- [x] Base de dados descrita (284.807 transações)
- [x] Desafios principais identificados
- [x] Fluxo da solução definido
- [x] Métricas apropriadas mencionadas (AUC-ROC, F1-Score)
- [x] Referências incluídas

**Revisor:** Lucio | **Criado:** 28/05/2026 | **Status:** ✅ Aprovado
