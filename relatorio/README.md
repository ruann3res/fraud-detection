# Relatório

Pasta com os relatórios semanais do trabalho.

## Relatórios disponíveis

| Semana | Arquivo | Conteúdo |
|--------|---------|----------|
| 2 | `relatorio_semana_2.md` | K-Means baseline |
| 3 | `relatorio_semana_3.md` | Comparação K-Means vs. DBSCAN |
| 4 | `relatorio_semana_4.md` | Random Forest (amostra 15k) |
| 5 | `relatorio_semana_5.md` | Validação na base completa |
| 6 | `relatorio_semana_6.md` | MLP, Regressão Logística, calibração e limiar |

## Resultados associados

Métricas e figuras referenciadas nos relatórios estão em `resultados/`:

- `semana_4_metricas_modelo_ic.csv`
- `semana_5_metricas_completa.csv`
- `semana_6_metricas_mlp.csv`
- `semana_6_metricas_ajustadas.csv`
- `semana_6_resumo_referencia_rf.csv`
- `figuras/semana_5_*.png`, `figuras/semana_6_*.png`

## Conclusão atual do projeto

O **Random Forest** (Semana 5) permanece o classificador de referência. MLP e Regressão
Logística (Semana 6) melhoraram com calibração e ajuste de limiar, mas não superaram o RF
em Average Precision e F1 de forma consistente.

## Relatório final

| Arquivo | Conteúdo |
|---------|----------|
| `relatorio_final.md` | Consolidação de todas as semanas (estrutura exigida pelo TFI) |

## Entregáveis finais previstos

- `slides.pptx`: apresentação final (ver `presentation/`).
