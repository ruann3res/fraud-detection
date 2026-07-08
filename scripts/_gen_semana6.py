"""Gerador do notebook da Semana 6 (MLP supervisionado).

Constroi um notebook didatico com exemplo minimo, uso do script reprodutivel
e leitura das metricas/figuras geradas em resultados/.
"""
from pathlib import Path

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
NB_DIR = ROOT / "notebooks"


def md(src: str):
    return nbf.v4.new_markdown_cell(src.strip("\n"))


def code(src: str):
    return nbf.v4.new_code_cell(src.strip("\n"))


def build(cells, path: Path) -> None:
    nb = nbf.v4.new_notebook()
    nb["cells"] = cells
    nb["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
    }
    nbf.write(nb, str(path))
    print("escrito:", path)


cells = []

cells.append(
    md(
        r"""
# Semana 6 - Modelo supervisionado MLP com scikit-learn

**Inteligencia Computacional I - Deteccao de fraude em cartao de credito**

## Objetivo

Testar uma rede neural MLP supervisionada (`sklearn.neural_network.MLPClassifier`)
na populacao completa de `dados/creditcard.csv`, comparando-a com os Random Forests
da Semana 5 e verificando se os clusters K-Means/DBSCAN agregam mais valor para uma
rede neural do que agregaram para arvores.

O protocolo permanece igual ao da Semana 5:

- base completa deduplicada: 283.726 transacoes, 473 fraudes;
- split estratificado 80/20 com `random_state=42`;
- validacao cruzada estratificada com 5 folds;
- metricas principais: AUC-ROC, Average Precision, Recall, Precision e F1;
- acuracia nao e usada como criterio por causa do forte desbalanceamento.
"""
    )
)

cells.append(md("## 0. Setup"))

cells.append(
    code(
        r"""
import os
os.environ.setdefault("MPLCONFIGDIR", "/tmp/mpl")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

import subprocess
import sys
from pathlib import Path

import pandas as pd
from IPython.display import Image, Markdown, display
from sklearn.metrics import average_precision_score
from sklearn.model_selection import train_test_split

ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
OUT_DIR = ROOT / "resultados"
FIG_DIR = OUT_DIR / "figuras"
PRED_DIR = OUT_DIR / "preds"

sys.path.insert(0, str(ROOT))
from scripts.semana_6_modelo_mlp import (  # noqa: E402
    RANDOM_STATE,
    TEST_SIZE,
    build_feature_matrices,
    fit_mlp,
    load_dataset,
    make_mlp_pipeline,
)

pd.set_option("display.float_format", lambda v: f"{v:.4f}")
print("ROOT:", ROOT)
print("TEST_SIZE:", TEST_SIZE, "| RANDOM_STATE:", RANDOM_STATE)
"""
    )
)

cells.append(
    md(
        r"""
## 1. Carregamento da base completa e dos clusters

O notebook reutiliza `resultados/semana_5_clusters_base_completa.csv`, sem recalcular
K-Means ou DBSCAN. A funcao `load_dataset()` valida se a coluna `Class` do arquivo de
clusters ainda corresponde a base deduplicada.
"""
    )
)

cells.append(
    code(
        r"""
dataset = load_dataset()
y = dataset["Class"].astype(int)
matrices = build_feature_matrices(dataset)

print(f"Registros: {len(dataset):,}")
print(f"Fraudes: {int(y.sum()):,}")
print(f"Taxa de fraude: {y.mean():.4%}")
print("Matrizes:")
for nome, X in matrices.items():
    print(f"- {nome}: {X.shape}")
"""
    )
)

cells.append(
    md(
        r"""
## 2. Por que `StandardScaler` e obrigatorio no MLP

O Random Forest das Semanas 4 e 5 usa arvores, portanto nao depende da escala absoluta
das variaveis. O MLP usa otimizacao por gradiente (`adam`) e funcoes de ativacao; sem
padronizacao, variaveis como `Amount` e `Time` podem dominar o treinamento.

Por isso o classificador e encapsulado em:

```python
Pipeline([
    ("scaler", StandardScaler()),
    ("mlp", MLPClassifier(...))
])
```

Observacao de compatibilidade: a versao local do scikit-learn nao tem parametro
`class_weight` em `MLPClassifier`. O script aplica a mesma ideia com
`sample_weight="balanced"` no `fit`, que e a API suportada pelo ambiente.
"""
    )
)

cells.append(md("## 3. Exemplo minimo didatico: `fit` -> `predict_proba`"))

cells.append(
    code(
        r"""
# Subset pequeno e estratificado manualmente para demonstracao rapida.
fraudes = dataset[dataset["Class"] == 1].sample(n=100, random_state=RANDOM_STATE)
legitimas = dataset[dataset["Class"] == 0].sample(n=5000, random_state=RANDOM_STATE)
mini = pd.concat([legitimas, fraudes]).sample(frac=1, random_state=RANDOM_STATE)

X_mini = mini[["Time", "Amount"] + [f"V{i}" for i in range(1, 29)]]
y_mini = mini["Class"].astype(int)

x_train, x_test, y_train, y_test = train_test_split(
    X_mini,
    y_mini,
    test_size=0.2,
    stratify=y_mini,
    random_state=RANDOM_STATE,
)

mini_model = fit_mlp(make_mlp_pipeline(), x_train, y_train)
probas = mini_model.predict_proba(x_test)[:, 1]
preds = mini_model.predict(x_test)

print("Exemplo minimo")
print("- treino:", x_train.shape, "| teste:", x_test.shape)
print("- iteracoes ate parada:", mini_model.named_steps["mlp"].n_iter_)
print("- Average Precision:", f"{average_precision_score(y_test, probas):.4f}")
pd.DataFrame({"y_real": y_test.to_numpy()[:10], "prob_fraude": probas[:10], "pred": preds[:10]})
"""
    )
)

cells.append(
    md(
        r"""
## 4. Pipeline completo e ajustes

O pipeline reprodutivel esta em `scripts/semana_6_modelo_mlp.py`. Alem dos tres MLPs
iniciais, o script executa:

- **Regressao Logistica balanceada** como baseline linear escalonado;
- **variantes de MLP** com arquiteturas menores e maior regularizacao (`alpha`);
- **calibracao de probabilidades** (`CalibratedClassifierCV`, metodo sigmoid);
- **ajuste de limiar** na validacao interna, buscando aumentar Precision sem perder
  Recall abaixo de 72% (referencia do RF baseline).

O Random Forest da Semana 5 permanece como **referencia principal** ate que outro
modelo supere AP e F1 de forma consistente.
"""
    )
)

cells.append(
    code(
        r"""
required_outputs = [
    OUT_DIR / "semana_6_metricas_mlp.csv",
    OUT_DIR / "semana_6_metricas_ajustadas.csv",
    OUT_DIR / "semana_6_comparacao_modelos_ajustada.csv",
    OUT_DIR / "semana_6_resumo_referencia_rf.csv",
]

if not all(path.exists() for path in required_outputs):
    print("Saidas da Semana 6 nao encontradas. Executando script completo...")
    subprocess.run([sys.executable, str(ROOT / "scripts" / "semana_6_modelo_mlp.py")], check=True)
else:
    print("Saidas da Semana 6 encontradas. Carregando CSVs existentes.")

metricas_mlp = pd.read_csv(OUT_DIR / "semana_6_metricas_mlp.csv")
metricas_ajustadas = pd.read_csv(OUT_DIR / "semana_6_metricas_ajustadas.csv")
comparacao = pd.read_csv(OUT_DIR / "semana_6_comparacao_rf_vs_mlp.csv")
comparacao_ajustada = pd.read_csv(OUT_DIR / "semana_6_comparacao_modelos_ajustada.csv")
resumo_rf = pd.read_csv(OUT_DIR / "semana_6_resumo_referencia_rf.csv")
metricas_mlp
"""
    )
)

cells.append(md("## 5. Comparacao inicial (limiar 0.5)"))

cells.append(
    code(
        r"""
cols = [
    "familia",
    "modelo",
    "n_features",
    "auc_roc_teste",
    "average_precision_teste",
    "recall_teste",
    "precision_teste",
    "f1_teste",
    "auc_roc_cv_media",
    "avg_precision_cv_media",
    "f1_cv_media",
]
comparacao[cols]
"""
    )
)

cells.append(md("## 6. Ajustes: calibracao + limiar + regularizacao"))

cells.append(
    code(
        r"""
metricas_ajustadas[
    [
        "familia",
        "modelo",
        "threshold",
        "calibrado",
        "average_precision_teste",
        "recall_teste",
        "precision_teste",
        "f1_teste",
        "observacao",
    ]
]
"""
    )
)

cells.append(md("## 7. Referencia Random Forest vs desafiantes"))

cells.append(
    code(
        r"""
resumo_rf
"""
    )
)

cells.append(md("## 8. Visualizacoes geradas"))

cells.append(
    code(
        r"""
figuras = [
    "semana_6_matriz_confusao.png",
    "semana_6_pr_curve.png",
    "semana_6_comparacao_rf_vs_mlp.png",
    "semana_6_matriz_confusao_ajustada.png",
    "semana_6_pr_curve_ajustada.png",
    "semana_6_comparacao_modelos_ajustada.png",
]

for figura in figuras:
    path = FIG_DIR / figura
    if path.exists():
        display(Markdown(f"### `{figura}`"))
        display(Image(filename=str(path)))
"""
    )
)

cells.append(md("## 9. Conclusao quantitativa"))

cells.append(
    code(
        r"""
rf = comparacao_ajustada[comparacao_ajustada["familia"] == "Random Forest"].copy()
best_rf = rf.sort_values(["avg_precision_cv_media", "f1_cv_media"], ascending=False).iloc[0]
best_tuned = metricas_ajustadas.sort_values(["f1_teste", "average_precision_teste"], ascending=False).iloc[0]
best_lr = metricas_ajustadas[metricas_ajustadas["familia"] == "Regressao Logistica"].sort_values("f1_teste", ascending=False).iloc[0]
supera_rf = bool(resumo_rf.iloc[0]["algum_supera_rf_consistente"])

texto = (
    f"**Referencia principal:** `{best_rf['modelo']}` com AP(CV)={best_rf['avg_precision_cv_media']:.4f} "
    f"e F1(CV)={best_rf['f1_cv_media']:.4f}.\n\n"
    f"**Melhor modelo ajustado:** `{best_tuned['modelo']}` com AP(teste)={best_tuned['average_precision_teste']:.4f}, "
    f"Recall={best_tuned['recall_teste']:.4f}, Precision={best_tuned['precision_teste']:.4f}, "
    f"F1={best_tuned['f1_teste']:.4f}, limiar={best_tuned['threshold']:.4f}.\n\n"
    f"**Regressao Logistica calibrada:** AP(teste)={best_lr['average_precision_teste']:.4f}, "
    f"F1(teste)={best_lr['f1_teste']:.4f}.\n\n"
    f"**Algum modelo supera o RF de forma consistente (AP e F1)?** "
    f"{'Sim' if supera_rf else 'Nao'} — o Random Forest permanece referencia principal."
)
display(Markdown(texto))
"""
    )
)

cells.append(
    md(
        r"""
## 10. Limitacoes

- Calibracao e limiar foram ajustados em subconjunto de validacao interna; ainda ha risco
  de variacao entre folds.
- O MLP continua menos explicavel que o Random Forest.
- Mesmo com calibracao e limiar, nenhum modelo alternativo superou o RF de forma
  consistente em AP e F1 na validacao cruzada.
- Os clusters permanecem com ganho marginal; o foco desta etapa foi melhorar o
  classificador neural/linear, nao redefinir o clustering.
"""
    )
)


build(cells, NB_DIR / "semana_6_modelo_mlp.ipynb")
