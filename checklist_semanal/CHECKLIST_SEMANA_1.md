# ✅ CHECKLIST - SEMANA 1

**Projeto:** Detecção de Fraude em Transações Financeiras  
**Data Limite:** [Preencher com data da aula]  
**Status:** Em Progresso

---

## 👤 RUAN - Agrupamento de Dados | Python Expert

### ANTES DE COMEÇAR
- [ ] Clone/atualize o repositório Git
- [ ] Instale dependências: `pip install pandas numpy matplotlib seaborn scikit-learn`
- [ ] Verifique se o arquivo `creditcard.csv` está em `dados/`
- [ ] Abra o notebook `notebooks/Semana_1_EDA_e_Preparacao.ipynb`

### NOTEBOOK - SEÇÕES A IMPLEMENTAR
- [ ] **Seção 2:** Executar importações e configurações
- [ ] **Seção 3:** Carregar a base de dados (adapte o caminho se necessário)
- [ ] **Seção 4:** Análise exploratória completa (execute todos os gráficos)
- [ ] **Seção 5:** Tratamento de valores ausentes
  - [ ] Verificar se há NaN
  - [ ] Documentar decisões (remover, preencher, etc)
  - [ ] Resultado esperado: 0 valores ausentes
- [ ] **Seção 6:** Tratamento de duplicidades
  - [ ] Detectar linhas duplicadas
  - [ ] Remover duplicidades
  - [ ] Documentar quantas foram removidas
- [ ] **Seção 7:** Detecção de Outliers (IMPORTANTE!)
  - [ ] Implementar função IQR
  - [ ] Detectar outliers em Amount
  - [ ] Documentar (NÃO remover!)
- [ ] **Seção 8:** Variáveis categóricas (conferir se precisa)
- [ ] **Seção 10:** Correlações e padrões
  - [ ] Calcular correlação com Class (fraude)
  - [ ] Gerar visualizações
  - [ ] Documentar features mais importantes

### QUALIDADE DO CÓDIGO
- [ ] Todo código está comentado
- [ ] Nomes de variáveis são descritivos
- [ ] Sem erros de execução
- [ ] Todas as células rodam sem exceções
- [ ] Gráficos são legíveis e informativos

### DOCUMENTAÇÃO TÉCNICA
- [ ] Documentar decisões de preprocessing
- [ ] Explicar por que cada tratamento foi aplicado
- [ ] Justificar valores de threshold (outliers, etc)
- [ ] Adicionar notas sobre desafios encontrados

### GIT
- [ ] Faça commits regularmente (não deixe para o final)
- [ ] Commits com mensagens claras: `"feat: tratamento de outliers em Amount"`
- [ ] Exemplo de boas mensagens:
  - `"fix: corrigir leitura do CSV"`
  - `"docs: adicionar análise de correlações"`
  - `"feat: implementar detecção de outliers"`

### ENTREGA FINAL
- [ ] Notebook executa sem erros do início ao fim
- [ ] Todos os gráficos são exibidos corretamente
- [ ] Push para GitHub está feito
- [ ] Avise Lucio quando terminar

---

## 👤 LUCIO - Dados, Pipeline e Integração | Coordenação

### ANTES DE COMEÇAR
- [ ] Verifique acesso ao repositório Git
- [ ] Configure Git com seu nome e email:
  ```bash
  git config user.name "Seu Nome"
  git config user.email "seu.email@exemplo.com"
  ```

### REPOSITÓRIO GITHUB
- [ ] Criar/verificar repositório no GitHub
- [ ] Adicionar arquivo `.gitignore` (see template below)
- [ ] Adicionar colaboradores (Ruan, Artur)
- [ ] Criar issues para rastrear tarefas

### BASE DE DADOS
- [ ] Pesquisar e escolher entre: Kaggle vs UCI dataset
  - [ ] RECOMENDADO: Kaggle (mais clara, 284.807 transações)
  - Link: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
- [ ] Fazer download do arquivo
- [ ] Colocar em: `dados/creditcard.csv`
- [ ] Documentar origem no README.md ✅ (já feito)
- [ ] Adicionar arquivo `dados/.gitignore` com:
  ```
  *.csv
  *.xlsx
  *.parquet
  ```

### ANÁLISE EXPLORATÓRIA
- [ ] Executar Seções 1-4 do notebook com Ruan
- [ ] Documentar:
  - [ ] Tamanho da base (linhas, colunas)
  - [ ] Tipos de dados
  - [ ] Distribuição de fraudes vs legítimas
  - [ ] Intervalo de valores (Amount, Time)

### DOCUMENTAÇÃO DO PROBLEMA
- [ ] Escrever em formato Markdown:
  - [ ] **Problema:** 2-3 linhas
  - [ ] **Pergunta Central:** 1 linha
  - [ ] **Base de Dados:** características principais
  - [ ] **Relevância:** Por que é importante?
- [ ] Colocar em: `PROBLEMA.md` ou seção do README

### DIVISÃO DE PAPÉIS
- [ ] Criar documento com as responsabilidades
- [ ] Adicionar ao README.md ✅ (já feito)
- [ ] Formato:
  ```
  | Aluno | Papel | Responsabilidades |
  | Ruan | Agrupamento | ... |
  | Lucio | Dados | ... |
  | Artur | IC | ... |
  ```

### ORGANIZAÇÃO
- [ ] Estrutura de pastas pronta ✅ (template fornecido)
- [ ] README.md completo ✅ (feito)
- [ ] Notebook organizado com seções
- [ ] Adicionar arquivo `NOTAS.md` com observações da equipe

### GIT - Coordenação
- [ ] Fazer commits bem documentados
- [ ] Revisar commits dos outros
- [ ] Comunicar ao grupo quando fizer push
- [ ] Manter histórico limpo

### COMUNICAÇÃO
- [ ] Criar lista de tarefas (GitHub Projects / Trello)
- [ ] Comunicar progresso ao grupo
- [ ] Coordenar integração entre Ruan e Artur
- [ ] Lembrar prazos antes do final

### ENTREGA FINAL
- [ ] Verificar se tudo está no repositório
- [ ] Confirmar que notebook roda sem erros
- [ ] Documentação completa
- [ ] README atualizado
- [ ] Todos os commits estão feitos

---

## 👤 ARTUR - Inteligência Computacional e Decisão | Pesquisa

### PESQUISA E ESTUDO
- [ ] Estudar desafios de desbalanceamento de classes
  - [ ] Ler sobre: SMOTE, class_weight, stratified sampling
  - [ ] Documentar 2-3 abordagens
  
- [ ] Pesquisar técnicas de Inteligência Computacional para fraude
  - Recomendado:
    - [ ] Random Forest (excelente para desbalanceamento)
    - [ ] Neural Networks (pode capturar padrões complexos)
    - [ ] SVM (bom para anomalias)
  - Documentar vantagens/desvantagens de cada uma

- [ ] Estudar métricas apropriadas (CRÍTICO!)
  - [ ] ❌ NÃO usar: Acurácia (enganosa com desbalanceamento)
  - [ ] ✅ USAR:
    - AUC-ROC (área sob a curva)
    - F1-Score (média harmônica)
    - Precision (quantas preditas como fraude eram reais)
    - Recall (quantas fraudes reais foram detectadas)
    - Confusion Matrix
    - Precision-Recall Curve

### DOCUMENTAÇÃO TÉCNICA
- [ ] Criar documento `instrucoes_IC/TECNICAS_IC.md` com:
  - [ ] Problema: desbalanceamento extremo
  - [ ] Técnicas estudadas (pelo menos 3)
  - [ ] Justificativa da técnica escolhida
  - [ ] Métricas apropriadas
  - [ ] Como integrar com clustering?

### PLANEJAMENTO DE INTEGRAÇÃO
- [ ] Documentar como clusters serão usados:
  - [ ] Opção 1: Rótulo do cluster como feature
  - [ ] Opção 2: Clusters para definir recomendações
  - [ ] Opção 3: Comparar modelo COM e SEM clusters
  - [ ] Qual vocês vão usar? (DECIDIR COM O GRUPO)

### ESTRATÉGIA SEMANA 4-5
- [ ] Fazer rascunho de arquitetura do modelo
- [ ] Listar bibliotecas necessárias (já instaladas?)
- [ ] Planejar pipeline:
  ```
  Dados brutos 
    → Preprocessamento (Ruan)
    → Clustering (Ruan)
    → Features + Clusters
    → Modelo IC (Artur)
    → Predição + Confiança
  ```

### DOCUMENTAÇÃO
- [ ] Criar arquivo `instrucoes_IC/PLANO_IC.md` com:
  - [ ] Escolha da técnica (justificada)
  - [ ] Dados necessários (features? clusters?)
  - [ ] Métricas de avaliação
  - [ ] Como comparar com/sem clusters
  - [ ] Timeline Semana 4-5

### COMUNICAÇÃO COM O GRUPO
- [ ] Compartilhar pesquisa com Ruan e Lucio
- [ ] Decidir juntos:
  - [ ] Qual técnica de IC usar?
  - [ ] Como fazer integração?
  - [ ] Quais métricas focar?

### NOTAS IMPORTANTES
- [ ] Lembrar ao grupo: desbalanceamento é o maior desafio
- [ ] Não remover outliers (podem ser fraudes!)
- [ ] Features V1-V28 já transformadas (não interpretar)
- [ ] Amount e Time são features interpretáveis

### ENTREGA FINAL
- [ ] Documento com técnicas pesquisadas ✅
- [ ] Plano de IC para Semanas 4-5 ✅
- [ ] Métricas escolhidas e justificadas ✅
- [ ] Estratégia de integração documentada ✅

---

## 📋 CHECKLIST DO GRUPO

### REPOSITÓRIO
- [ ] GitHub criado e compartilhado
- [ ] `.gitignore` configurado
- [ ] Estrutura de pastas organizada
- [ ] README.md completo

### SEMANA 1 - ENTREGA OBRIGATÓRIA
- [ ] ✅ Identificação do cenário (Cenário 4)
- [ ] ✅ Base de dados documentada (Kaggle, 284.807 linhas)
- [ ] ✅ Problema descrito
- [ ] ✅ Pergunta central documentada
- [ ] ✅ Análise exploratória completa
- [ ] ✅ Valores ausentes tratados
- [ ] ✅ Duplicidades removidas
- [ ] ✅ Outliers identificados
- [ ] ✅ Variáveis categóricas revisadas
- [ ] ✅ Divisão de papéis documentada
- [ ] ✅ Notebook principal pronto

### NOTEBOOK FUNCIONANDO
- [ ] Executa sem erros
- [ ] Todas as células rodam
- [ ] Gráficos são exibidos
- [ ] Comentários explicativos
- [ ] Seções bem organizadas

### DOCUMENTAÇÃO
- [ ] README.md ✅
- [ ] PROBLEMA.md (se criado)
- [ ] `instrucoes_IC/TECNICAS_IC.md` (Artur)
- [ ] `instrucoes_IC/PLANO_IC.md` (Artur)
- [ ] Commit messages claras

### GIT
- [ ] Pelo menos 1 commit por pessoa
- [ ] Mensagens descritivas
- [ ] Sem conflitos no merge
- [ ] Histórico limpo

---

## ⏰ TIMELINE SUGERIDA

**Semana de [DATA]:**

| Dia | Ruan | Lucio | Artur |
|-----|------|-------|-------|
| 1 | Configurar env | Clonar repo | Estudar desbalanceamento |
| 2 | Carregar dados | Baixar CSV | Pesquisar técnicas |
| 3 | Limpeza de dados | Análise inicial | Documentar desafios |
| 4 | Outliers + Correlações | Documentação | Métricas apropriadas |
| 5 | Review + Push | Review + Push | Review + Push |

**Prazo Final:** [Preencher com data da apresentação]

---

## 📞 DÚVIDAS FREQUENTES DO GRUPO

**P: Por onde começamos?**  
R: 
1. Lucio cria/organiza repo
2. Ruan executa notebook
3. Artur pesquisa técnicas

**P: O que fazer se der erro no notebook?**  
R: 
1. Verificar se o CSV está em `dados/`
2. Verificar versões das bibliotecas
3. Testar uma célula de cada vez

**P: Já posso remover os outliers?**  
R: NÃO! Outliers podem ser fraudes. Mantenha para análise posterior.

**P: Quando começar a programar o modelo?**  
R: Semana 4. Agora é preparação de dados.

**P: Preciso fazer tudo sozinho?**  
R: NÃO! Vocês trabalham em paralelo. Comuniquem o progresso.

---

## ✨ DICAS DE OURO

1. **Ruan:** Faça commits pequenos e frequentes. Fica fácil revisar.
2. **Lucio:** Documentação agora = economia de tempo depois.
3. **Artur:** Escolha as métricas ANTES de programar o modelo.
4. **Todos:** Comuniquem dúvidas logo. Não esperem pro final.

---

**Status Atual:** Pronto para começar! 🚀  
**Última Atualização:** 28/05/2026
