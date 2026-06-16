# Início Aqui

Este é o roteiro rápido para abrir e continuar o projeto de detecção de fraude.

---

## 1. Conferir a Estrutura

Os arquivos principais estão organizados assim:

```text
checklist_semanal/   -> checklists das semanas 1, 2 e 3
dados/               -> base local creditcard.csv
instrucoes_IC/       -> documentos de Inteligência Computacional
notebooks/           -> notebooks das semanas 1, 2 e 3
scripts/             -> scripts reutilizáveis futuros
relatorio/           -> relatórios semanais e apresentação final
```

---

## 2. Preparar o Ambiente

No terminal, dentro da pasta `fraud-detection`:

```bash
python -m venv venv
venv\Scripts\activate
pip install pandas numpy matplotlib seaborn scikit-learn jupyter
```

Se estiver usando `uv`:

```bash
uv sync
```

---

## 3. Conferir a Base

O arquivo esperado é:

```text
dados/creditcard.csv
```

Se ele não existir, baixar em:

https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

---

## 4. Ordem Recomendada de Execução

1. `notebooks/Semana_1_EDA_e_Preparacao.ipynb`
2. `notebooks/semana_2_clustering_baseline.ipynb`
3. `notebooks/semana_3_comparacao.ipynb`

Para abrir:

```bash
jupyter notebook
```

---

## 5. Onde Consultar Cada Coisa

| Preciso de... | Arquivo |
|---------------|---------|
| Visão geral do projeto | `README.md` |
| Tarefas da Semana 1 | `checklist_semanal/CHECKLIST_SEMANA_1.md` |
| Tarefas da Semana 2 | `checklist_semanal/CHECKLIST_SEMANA_2.md` |
| Tarefas da Semana 3 | `checklist_semanal/CHECKLIST_SEMANA_3.md` |
| Relatório da Semana 2 | `relatorio/relatorio_semana_2.md` |
| Relatório da Semana 3 | `relatorio/relatorio_semana_3.md` |
| Problema e pergunta central | `PROBLEMA.md` |
| Técnicas de IC | `instrucoes_IC/TECNICAS_IC.md` |
| Plano de IC | `instrucoes_IC/PLANO_IC.md` |
| Guia de Git | `GUIA_GIT_PUSH.md` |

---

## 6. Próximo Passo Atual

Revisar a entrega da Semana 3:

```text
notebooks/semana_3_comparacao.ipynb
checklist_semanal/CHECKLIST_SEMANA_3.md
relatorio/relatorio_semana_3.md
```

Decisão atual para a etapa de Inteligência Computacional:

- usar `cluster_kmeans_semana3` como feature categórica;
- usar `dbscan_ruido` como indicador binário de anomalia;
- comparar modelos supervisionados com e sem essas variáveis.

---

**Status:** estrutura atualizada até a Semana 3; próximo passo é iniciar a Semana 4.
