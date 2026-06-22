# CHECKLIST - SEMANA 3

**Projeto:** Detecção de Fraude em Transações Financeiras  
**Tema:** Agrupamento de Dados II: comparação, validação e interpretação  
**Produto esperado:** Comparação entre K-Means e DBSCAN, interpretação dos perfis encontrados e definição de uso dos clusters na etapa de Inteligência Computacional.  
**Status:** Em Progresso

---

## Objetivo da Semana

Comparar o baseline da Semana 2 com um segundo algoritmo de agrupamento, validar os resultados com métricas, interpretar os clusters gerados, nomear os perfis encontrados e definir como a estrutura de agrupamento será usada nas Semanas 4 e 5.

Nesta semana, o foco não é apenas executar outro algoritmo. O objetivo é justificar tecnicamente se os clusters ajudam a identificar padrões de risco e como eles podem enriquecer a base para Inteligência Computacional.

---

## Entrega Obrigatória

- [ ] Aplicação de um segundo algoritmo de agrupamento
- [ ] Comparação entre os algoritmos
- [ ] Uso de pelo menos duas métricas de avaliação
- [ ] Análise dos parâmetros utilizados
- [ ] Interpretação dos clusters
- [ ] Nomeação dos perfis encontrados
- [ ] Definição de como os clusters serão usados na Inteligência Computacional
- [ ] Geração da variável ou estrutura de saída do agrupamento

---

## Arquivos Principais da Semana

- [ ] Executar e revisar o notebook `notebooks/semana_3_comparacao.ipynb`
- [ ] Registrar a análise escrita em `relatorio/relatorio_semana_3.md`
- [ ] Conferir se os resultados dialogam com `relatorio/relatorio_semana_2.md`
- [ ] Atualizar `instrucoes_IC/PLANO_IC.md` caso a decisão de uso dos clusters mude
- [ ] Exportar, se necessário, `dados/saida_clusters_semana3.csv`

---

## RUAN - Agrupamento de Dados | Implementação em Python

### Preparação

- [ ] Atualizar o repositório local com `git pull`
- [ ] Selecionar o kernel correto do notebook (`venv` ou `.venv`)
- [ ] Garantir que as dependências estejam instaladas:
  ```bash
  pip install pandas numpy matplotlib seaborn scikit-learn jupyter ipykernel
  ```
- [ ] Verificar se `dados/creditcard.csv` existe localmente
- [ ] Abrir o notebook `notebooks/semana_3_comparacao.ipynb`

### Carregamento e Atributos

- [ ] Carregar a base diretamente de `../dados/creditcard.csv`
- [ ] Confirmar dimensões esperadas: 284.807 linhas e 31 colunas
- [ ] Separar `Class` apenas para análise externa
- [ ] Usar como matriz de agrupamento:
  - `V1` a `V28`
  - `Time`
  - `Amount`
- [ ] Confirmar total de 30 atributos
- [ ] Documentar que `Class` não entra no clustering para evitar vazamento de informação

### Escalonamento

- [ ] Aplicar `StandardScaler` para o K-Means
- [ ] Aplicar `RobustScaler` para o DBSCAN
- [ ] Justificar a diferença entre os scalers
- [ ] Conferir se a matriz escalonada não possui valores ausentes ou infinitos

### K-Means

- [ ] Reconstruir o baseline da Semana 2 com K-Means
- [ ] Usar `k = 6`
- [ ] Fixar `random_state = 42`
- [ ] Criar a coluna `cluster_kmeans_semana3`
- [ ] Conferir se foram gerados 6 clusters avaliáveis
- [ ] Registrar métricas:
  - Silhouette: aproximadamente 0,0838
  - Davies-Bouldin: aproximadamente 2,4227
  - Calinski-Harabasz: aproximadamente 617,44

### DBSCAN

- [ ] Aplicar DBSCAN como segundo algoritmo de agrupamento
- [ ] Definir `min_samples = 60`
- [ ] Estimar `eps` pela curva de vizinhos mais próximos
- [ ] Testar valores de `eps`:
  - 6,2297
  - 8,3063
  - 10,3829
- [ ] Usar `eps = 8,3063` como valor final preliminar
- [ ] Criar a coluna `cluster_dbscan_semana3`
- [ ] Confirmar distribuição esperada na amostra:
  - cluster `0`: 14.614 registros
  - cluster `-1`: 386 registros
- [ ] Registrar que `-1` representa ruído/anomalia

### Comparação e Visualização

- [ ] Comparar K-Means e DBSCAN em tabela única
- [ ] Usar pelo menos duas métricas de avaliação
- [ ] Gerar visualização com PCA em 2 dimensões
- [ ] Criar gráfico colorido por `cluster_kmeans_semana3`
- [ ] Criar gráfico colorido por `cluster_dbscan_semana3`
- [ ] Verificar se os gráficos possuem título, legenda e leitura adequada

### Estrutura de Saída

- [ ] Criar `perfil_kmeans`
- [ ] Criar `perfil_dbscan`
- [ ] Criar `dbscan_ruido`
- [ ] Gerar `saida_clusters` com as colunas:
  - `cluster_kmeans_semana3`
  - `perfil_kmeans`
  - `cluster_dbscan_semana3`
  - `perfil_dbscan`
  - `dbscan_ruido`
  - `Class`, se disponível para análise externa
- [ ] Exportar `dados/saida_clusters_semana3.csv`, se necessário

---

## LUCIO - Dados, Pipeline e Integração | Documentação

### Organização da Entrega

- [ ] Verificar se o notebook está em `notebooks/semana_3_comparacao.ipynb`
- [ ] Verificar se o relatório está em `relatorio/relatorio_semana_3.md`
- [ ] Conferir se o README da pasta `relatorio/` está coerente com a existência do relatório da Semana 3
- [ ] Confirmar que o CSV original continua fora do Git
- [ ] Revisar se tabelas e gráficos estão compreensíveis

### Revisão Metodológica

- [ ] Confirmar que `Class` não foi usada como atributo de entrada do clustering
- [ ] Confirmar que `Class` foi usada apenas depois, para análise de fraude por cluster
- [ ] Verificar se `Time` foi mantido como atributo de agrupamento
- [ ] Conferir se a comparação usa a mesma amostra para os dois algoritmos
- [ ] Revisar se a escolha de `eps` e `min_samples` está explicada

### Relatório da Semana 3

- [ ] Revisar `relatorio/relatorio_semana_3.md`
- [ ] Conferir se o texto segue o padrão da Semana 2:
  - decisão tomada
  - justificativa
  - métrica ou evidência
  - limitação registrada
- [ ] Confirmar que os resultados principais foram documentados:
  - K-Means com 6 clusters
  - DBSCAN com cluster dominante e ruído
  - cluster 2 do K-Means como perfil crítico
  - ruído `-1` do DBSCAN como anomalia relevante
- [ ] Revisar ortografia, consistência dos nomes e caminhos dos arquivos

### Integração com Próximas Semanas

- [ ] Verificar se a estrutura de saída pode alimentar a Semana 4
- [ ] Confirmar se os nomes das colunas estão estáveis
- [ ] Registrar decisão de uso em IC:
  - `cluster_kmeans_semana3` como feature categórica
  - `dbscan_ruido` como indicador binário de anomalia
- [ ] Sugerir atualização em `instrucoes_IC/PLANO_IC.md`, se necessário

---

## ARTUR - Inteligência Computacional e Decisão | Análise Crítica

### Análise dos Resultados

- [ ] Interpretar a tabela comparativa entre K-Means e DBSCAN
- [ ] Registrar que o K-Means teve melhor avaliação interna por formar múltiplos clusters
- [ ] Registrar que o DBSCAN foi mais útil como detector de anomalia
- [ ] Avaliar a relevância do cluster 2 do K-Means:
  - 13 transações
  - 12 fraudes
  - taxa de fraude de 92,31%
- [ ] Avaliar a relevância do ruído DBSCAN:
  - 386 transações
  - 23 fraudes
  - taxa de fraude de 5,96%

### Nomeação dos Perfis

- [ ] Nomear os perfis K-Means:
  - Cluster 2: Perfil crítico de fraude concentrada
  - Cluster 0: Perfil de risco acima da média
  - Cluster 3: Perfil de transações de alto valor financeiro
  - Clusters 1 e 4: Perfis transacionais predominantes de baixo risco
  - Cluster 5: Perfil sem fraude observada na amostra
- [ ] Nomear os perfis DBSCAN:
  - Cluster 0: Comportamento transacional dominante
  - Cluster -1: Ruído/anomalia com alta concentração de fraude

### Definição para IC

- [ ] Definir `cluster_kmeans_semana3` como feature categórica
- [ ] Definir `dbscan_ruido` como feature binária
- [ ] Planejar comparação supervisionada da Semana 4:
  - modelo sem clusters
  - modelo com `cluster_kmeans_semana3`
  - modelo com `cluster_kmeans_semana3` + `dbscan_ruido`
- [ ] Avaliar modelos com métricas adequadas:
  - AUC-ROC
  - F1-Score
  - Recall
  - Precision
  - Matriz de confusão
- [ ] Não usar acurácia como métrica principal

### Limitações a Registrar

- [ ] Silhouette do K-Means é baixo, indicando sobreposição entre clusters
- [ ] DBSCAN gerou apenas um cluster principal e ruído
- [ ] Métricas internas do DBSCAN ficaram indisponíveis (`NaN`) por haver apenas um cluster válido
- [ ] Resultados foram calculados em amostra de 15.000 registros
- [ ] Confirmar utilidade real apenas na Semana 4, com modelo supervisionado

---

## Checklist do Grupo

### Implementação

- [ ] Notebook `notebooks/semana_3_comparacao.ipynb` executado
- [ ] Base carregada corretamente
- [ ] `Class` excluída do clustering
- [ ] `V1`–`V28`, `Time` e `Amount` usados como atributos
- [ ] K-Means reconstruído
- [ ] DBSCAN aplicado
- [ ] Parâmetros do DBSCAN analisados
- [ ] Métricas calculadas e documentadas
- [ ] PCA usado para visualização

### Comparação e Validação

- [ ] K-Means e DBSCAN comparados em tabela
- [ ] Silhouette calculado para K-Means
- [ ] Davies-Bouldin calculado para K-Means
- [ ] Calinski-Harabasz calculado para K-Means
- [ ] Taxa de ruído calculada para DBSCAN
- [ ] Explicação registrada para métricas `NaN` do DBSCAN
- [ ] Fraudes por cluster analisadas

### Interpretação

- [ ] Perfis K-Means nomeados
- [ ] Perfis DBSCAN nomeados
- [ ] Cluster 2 do K-Means destacado como crítico
- [ ] Ruído `-1` do DBSCAN destacado como anomalia relevante
- [ ] Limitações registradas
- [ ] Uso em IC definido

### Documentação

- [ ] `relatorio/relatorio_semana_3.md` preenchido
- [ ] Conclusão do notebook preenchida
- [ ] Caminhos dos arquivos revisados
- [ ] Relatório revisado por pelo menos um membro do grupo
- [ ] Commits feitos com mensagens claras

---

## Cronograma Semanal Sugerido

| Dia | Ruan | Lucio | Artur |
|-----|------|-------|-------|
| 1 | Preparar ambiente e executar imports | Conferir organização dos arquivos | Revisar objetivos da Semana 3 |
| 2 | Carregar dados, selecionar atributos e escalonar | Revisar se `Class` ficou fora do clustering | Validar decisão de usar `Time` |
| 3 | Rodar K-Means e DBSCAN | Conferir tabelas e gráficos | Interpretar métricas e parâmetros |
| 4 | Gerar perfis, PCA e estrutura de saída | Revisar relatório da Semana 3 | Definir uso em IC |
| 5 | Ajustar notebook final | Revisar documentação e caminhos | Consolidar conclusões e próximos passos |

---

## Sugestão de Estrutura do Notebook

1. Introdução e objetivo da Semana 3
2. Imports e configurações
3. Carregamento dos dados
4. Seleção dos atributos
5. Escalonamento
6. Amostra de comparação
7. K-Means baseline
8. DBSCAN
9. Métricas e comparação
10. Visualização com PCA
11. Interpretação dos clusters
12. Nomeação dos perfis
13. Definição de uso em IC
14. Exportação da estrutura de saída
15. Conclusão preliminar

---

## Perguntas para Responder na Entrega

- Qual foi o segundo algoritmo de agrupamento aplicado?
- Por que DBSCAN foi escolhido?
- Quais parâmetros foram usados no DBSCAN?
- Como `eps` foi escolhido?
- Quantos clusters o K-Means gerou?
- Quantos clusters o DBSCAN gerou?
- Por que as métricas do DBSCAN ficaram como `NaN`?
- Quais métricas foram usadas para comparar os algoritmos?
- Quais clusters concentraram mais fraudes?
- Quais perfis foram nomeados?
- Como os clusters serão usados na etapa de IC?
- Qual estrutura de saída foi gerada?

---

## Critérios de Pronto

A Semana 3 pode ser considerada pronta quando:

- [ ] O notebook executa sem erros até a conclusão
- [ ] DBSCAN foi aplicado como segundo algoritmo
- [ ] K-Means e DBSCAN foram comparados
- [ ] Pelo menos duas métricas foram usadas
- [ ] Os parâmetros do DBSCAN foram explicados
- [ ] Os clusters foram interpretados
- [ ] Os perfis foram nomeados
- [ ] A estrutura de saída foi gerada
- [ ] O uso em IC foi definido
- [ ] O relatório da Semana 3 foi preenchido

---

## Resultado Esperado

Ao final da Semana 3, o grupo deve conseguir defender que:

- K-Means é a melhor estrutura atual para segmentação de perfis.
- DBSCAN é útil como detector complementar de anomalias.
- O cluster 2 do K-Means merece atenção especial por concentrar fraude.
- O ruído `-1` do DBSCAN é um bom candidato a indicador de risco.
- A Semana 4 deve testar `cluster_kmeans_semana3` e `dbscan_ruido` como variáveis adicionais no modelo supervisionado.

---

**Última atualização:** 15 de junho de 2026  
**Status:** Semana 3 - Comparação, validação e interpretação de clusters
