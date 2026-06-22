# Resumo da Estrutura Atual do Projeto

**Projeto:** Detecção de Fraude em Transações Financeiras  
**Grupo:** Ruan, Lucio e Artur  
**Última atualização:** 15 de junho de 2026

---

## Estado Atual

O projeto já não está mais apenas na estrutura inicial da Semana 1. Os arquivos foram organizados por finalidade:

- checklists semanais em `checklist_semanal/`;
- notebooks em `notebooks/`;
- documentos de Inteligência Computacional em `instrucoes_IC/`;
- base local em `dados/`;
- materiais futuros em `scripts/` e `relatorio/`.

---

## Estrutura Atual

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

## Arquivos Principais

| Arquivo | Finalidade |
|---------|------------|
| `README.md` | Guia principal do projeto |
| `INICIO_AQUI.md` | Roteiro rápido para começar |
| `GUIA_GIT_PUSH.md` | Orientações de Git e push |
| `PROBLEMA.md` | Definição do problema e pergunta central |
| `checklist_semanal/CHECKLIST_SEMANA_1.md` | Tarefas da Semana 1 |
| `checklist_semanal/CHECKLIST_SEMANA_2.md` | Tarefas da Semana 2 |
| `checklist_semanal/CHECKLIST_SEMANA_3.md` | Tarefas, cronograma e critérios da Semana 3 |
| `notebooks/Semana_1_EDA_e_Preparacao.ipynb` | EDA e preparação |
| `notebooks/semana_2_clustering_baseline.ipynb` | K-Means baseline |
| `notebooks/semana_3_comparacao.ipynb` | Comparação K-Means vs. DBSCAN |
| `relatorio/relatorio_semana_2.md` | Justificativas e resultados da Semana 2 |
| `relatorio/relatorio_semana_3.md` | Justificativas, comparação e decisão da Semana 3 |
| `instrucoes_IC/TECNICAS_IC.md` | Pesquisa e decisão de técnicas de IC |
| `instrucoes_IC/PLANO_IC.md` | Plano de integração clustering + IC |

---

## Progresso por Semana

### Semana 1

Status: estruturada.

Entregáveis:

- análise exploratória;
- preparação da base;
- identificação de outliers;
- documentação do problema;
- organização inicial do projeto.

Arquivos:

- `notebooks/Semana_1_EDA_e_Preparacao.ipynb`
- `checklist_semanal/CHECKLIST_SEMANA_1.md`
- `PROBLEMA.md`

### Semana 2

Status: checklist, notebook e relatório criados.

Entregáveis:

- seleção e justificativa de atributos;
- padronização;
- K-Means baseline;
- visualização;
- análise inicial dos clusters.

Arquivos:

- `notebooks/semana_2_clustering_baseline.ipynb`
- `checklist_semanal/CHECKLIST_SEMANA_2.md`
- `relatorio/relatorio_semana_2.md`

### Semana 3

Status: checklist, notebook e relatório criados.

Entregáveis:

- segundo algoritmo de agrupamento;
- comparação entre algoritmos;
- métricas de validação;
- interpretação dos clusters;
- nomeação dos perfis;
- estrutura de saída para a etapa de IC.

Arquivos:

- `notebooks/semana_3_comparacao.ipynb`
- `checklist_semanal/CHECKLIST_SEMANA_3.md`
- `relatorio/relatorio_semana_3.md`

Decisão consolidada:

- usar `cluster_kmeans_semana3` como feature categórica de perfil;
- usar `dbscan_ruido` como indicador binário de anomalia;
- testar essas variáveis na etapa supervisionada da Semana 4.

### Semanas 4 e 5

Status: planejadas nos documentos de IC.

Arquivos:

- `instrucoes_IC/TECNICAS_IC.md`
- `instrucoes_IC/PLANO_IC.md`
- `relatorio/README.md`

---

## Próximas Ações Recomendadas

1. Revisar se `relatorio/relatorio_semana_3.md` e `checklist_semanal/CHECKLIST_SEMANA_3.md` estão coerentes com o notebook.
2. Atualizar `instrucoes_IC/PLANO_IC.md` com a decisão final da Semana 3, se necessário.
3. Iniciar a Semana 4 com modelo supervisionado baseline sem clusters.
4. Criar versão supervisionada com `cluster_kmeans_semana3`.
5. Criar versão supervisionada com `cluster_kmeans_semana3` + `dbscan_ruido`.
6. Comparar os modelos usando AUC-ROC, F1-Score, Recall e Precision.

---

## Observações Importantes

- `dados/creditcard.csv` deve permanecer local e não deve ser versionado.
- A coluna `Class` não deve ser usada como entrada dos algoritmos de clustering.
- A coluna `Class` pode ser usada depois para análise externa dos clusters.
- Acurácia não deve ser métrica principal por causa do desbalanceamento extremo.
- Outliers devem ser analisados com cuidado, não removidos automaticamente.

---

**Status geral:** estrutura documentada até a Semana 3; próximo foco é a integração supervisionada da Semana 4.
