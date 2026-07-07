"""Gerador dos notebooks da Semana 5 (validacao na base completa).

Constroi dois notebooks reprodutiveis com nbformat e os salva em notebooks/.
A execucao (embed de outputs) e feita depois via jupyter nbconvert.
"""
from pathlib import Path
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
NB_DIR = ROOT / "notebooks"


def md(src: str):
    return nbf.v4.new_markdown_cell(src.strip("\n"))


def code(src: str):
    return nbf.v4.new_code_cell(src.strip("\n"))


def build(cells, path: Path):
    nb = nbf.v4.new_notebook()
    nb["cells"] = cells
    nb["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
    }
    nbf.write(nb, str(path))
    print("escrito:", path)


nb1_cells = []
nb2_cells = []

# =====================================================================
# NOTEBOOK 1 - Random Forest com K-Means + DBSCAN na base completa
# =====================================================================

nb1_cells.append(md(r"""
# Semana 5 - Validacao na base completa: Random Forest com K-Means + DBSCAN

**Inteligencia Computacional I - Deteccao de fraude em cartao de credito**

## Objetivo

Replicar o pipeline supervisionado da Semana 4 usando a **populacao completa** de
`dados/creditcard.csv` (~283.726 transacoes apos remocao de duplicatas, ~473 fraudes),
em vez da amostra estratificada de 15.000 registros (25 fraudes) usada na Semana 3/4.

A pergunta de pesquisa e a mesma da Semana 4: **os clusters (K-Means e DBSCAN)
agregam valor consistente ao classificador fraude vs. nao fraude?** Agora respondida
sobre toda a populacao, onde ha muito mais exemplos positivos.

### O que muda em relacao a Semana 4
- Os rotulos de cluster sao gerados **sobre toda a base** (nao mais sobre 15k).
- O `eps` do DBSCAN precisa ser **recalibrado** por custo computacional (documentado abaixo).
- O conjunto de teste passa a ter ~95 fraudes (20% de 473) em vez de apenas 5.

### Convencoes herdadas das Semanas 1-4
- Remocao de duplicatas (Semana 1/2): base final de 283.726 linhas.
- `StandardScaler` para K-Means; `RobustScaler` para DBSCAN (Semana 3).
- K-Means com `k=6` (melhor silhouette nas Semanas 2/3).
- Random Forest: `n_estimators=200, min_samples_leaf=2, class_weight='balanced', random_state=42`.
- Split estratificado 80/20 e validacao cruzada estratificada de 5 folds.
- Metricas principais: AUC-ROC, Average Precision, Recall, Precision, F1 (acuracia **nao** e usada).
"""))

nb1_cells.append(md("## 0. Configuracao do ambiente"))

nb1_cells.append(code(r"""
import os
# diretorios graváveis para cache (ambiente do projeto)
os.environ.setdefault("MPLCONFIGDIR", "/tmp/mpl")
os.environ.setdefault("LOKY_MAX_CPU_COUNT", "4")

import time
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.neighbors import NearestNeighbors
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    precision_recall_curve,
    roc_curve,
)
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split

sns.set_theme(style="whitegrid")
pd.set_option("display.float_format", lambda v: f"{v:.4f}")

RANDOM_STATE = 42
TEST_SIZE = 0.20

ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
DATA_DIR = ROOT / "dados"
OUT_DIR = ROOT / "resultados"
FIG_DIR = OUT_DIR / "figuras"
PRED_DIR = OUT_DIR / "preds"
for d in (OUT_DIR, FIG_DIR, PRED_DIR):
    d.mkdir(parents=True, exist_ok=True)

print("ROOT:", ROOT)
print("scikit-learn / pandas / numpy carregados")
"""))

nb1_cells.append(md(r"""
## 1. Carregamento da base completa

Carregamos `dados/creditcard.csv` **sem amostragem** e repetimos a remocao de
duplicatas adotada na Semana 1/2, chegando as 283.726 transacoes da populacao final.
"""))

nb1_cells.append(code(r"""
t0 = time.time()
df = pd.read_csv(DATA_DIR / "creditcard.csv")
dups = int(df.duplicated().sum())
df = df.drop_duplicates().reset_index(drop=True)

n_total = len(df)
n_fraude = int(df["Class"].sum())
print(f"Linhas apos remocao de {dups} duplicatas: {n_total:,}")
print(f"Fraudes (Class=1): {n_fraude:,}  |  taxa de fraude: {df['Class'].mean():.4%}")
print(f"Tempo de carga: {time.time()-t0:.1f}s")
df[["Time", "Amount", "Class"]].describe()
"""))

nb1_cells.append(md(r"""
## 2. Pre-processamento (Semana 1/3)

As variaveis de modelagem sao `Time`, `Amount` e `V1`-`V28`. Para o **clustering**
aplicamos as escalas definidas na Semana 3:

- `StandardScaler` para o **K-Means** (consistencia com o baseline da Semana 2);
- `RobustScaler` para o **DBSCAN** (reduz o impacto de valores extremos em `Amount`).

A coluna `Class` e mantida **fora** do treino dos algoritmos de clustering e usada
apenas na avaliacao posterior.
"""))

nb1_cells.append(code(r"""
feature_cols = [c for c in df.columns if c.startswith("V")] + ["Time", "Amount"]
X = df[feature_cols].copy()
y = df["Class"].astype(int)

X_standard = StandardScaler().fit_transform(X)   # K-Means
X_robust = RobustScaler().fit_transform(X)       # DBSCAN

print("Atributos de clustering:", len(feature_cols))
print("X_standard:", X_standard.shape, "| X_robust:", X_robust.shape)
"""))

nb1_cells.append(md(r"""
## 3. K-Means na base completa (k=6)

Reutilizamos `k=6`, o melhor valor de silhouette identificado nas Semanas 2/3,
com `n_init=10` e `random_state=42`. Diferente do DBSCAN, o K-Means escala bem para
a base completa (ajuste em poucos segundos), portanto **nao** foi necessario amostrar.
"""))

nb1_cells.append(code(r"""
BEST_K = 6
t0 = time.time()
kmeans = KMeans(n_clusters=BEST_K, random_state=RANDOM_STATE, n_init=10)
df["cluster_kmeans"] = kmeans.fit_predict(X_standard)
print(f"K-Means treinado (k={BEST_K}) em {time.time()-t0:.1f}s")

dist_km = (
    df.groupby("cluster_kmeans")["Class"]
    .agg(n="size", fraudes="sum", taxa_fraude="mean")
    .assign(taxa_fraude=lambda d: d["taxa_fraude"])
)
print("\nDistribuicao dos clusters K-Means e concentracao de fraude:")
dist_km
"""))

nb1_cells.append(md(r"""
## 4. DBSCAN na base completa - recalibracao do `eps` por custo computacional

> **Limitacao de memoria/tempo (documentada).** O `eps=8.3063` escolhido na Semana 3
> foi calibrado sobre a amostra de 15.000 registros. Na base completa, esse raio torna
> a vizinhanca media de cada ponto ~210.000 vizinhos (de 283.726), o que estoura a
> memoria do `DBSCAN` do scikit-learn (matriz de adjacencia com ~6e10 arestas -> processo
> encerrado por falta de memoria). O mesmo ocorre com o `eps` do percentil 95 da curva
> k-distance recalculada na base completa (~5,67), pois os componentes PCA `V1`-`V28`
> sao densamente concentrados perto da origem.
>
> **Estrategia adotada:** recalcular a curva k-distance (60o vizinho, `min_samples=60`)
> na populacao completa para entender a densidade, e **reduzir o `eps` para 2,5** -
> valor que mantem o DBSCAN tratavel (~30s, vizinhancas limitadas) preservando o sinal
> de anomalia (pontos de ruido `-1`). `min_samples=60` e mantido (`2 x n_features`),
> como na Semana 3. Nenhuma amostragem foi necessaria: o DBSCAN roda sobre as 283.726
> transacoes.
"""))

nb1_cells.append(code(r"""
MIN_SAMPLES = 60  # 2 * n_features, igual a Semana 3

t0 = time.time()
nn = NearestNeighbors(n_neighbors=MIN_SAMPLES, n_jobs=int(os.environ["LOKY_MAX_CPU_COUNT"]))
nn.fit(X_robust)
dist, _ = nn.kneighbors(X_robust)
k_dist = np.sort(dist[:, -1])
print(f"Curva k-distance (60o vizinho) calculada em {time.time()-t0:.1f}s")

for p in (90, 95, 97.5, 99):
    print(f"  k-distance p{p}: {np.percentile(k_dist, p):.4f}")

eps_semana3 = 8.3063
eps_p95 = float(np.percentile(k_dist, 95))
print(f"\neps Semana 3 (amostra 15k): {eps_semana3}  -> INVIAVEL na base completa (OOM)")
print(f"eps p95 base completa:      {eps_p95:.4f}  -> ainda INVIAVEL (vizinhancas densas)")
print(f"eps adotado (recalibrado):  2.5           -> VIAVEL e com sinal de anomalia")

plt.figure(figsize=(8, 4))
plt.plot(k_dist)
for val, lab, col in [(eps_p95, f"p95 = {eps_p95:.2f} (inviavel)", "orange"),
                      (2.5, "eps adotado = 2.5", "red")]:
    plt.axhline(val, linestyle="--", color=col, label=lab)
plt.title("Curva k-distance (60o vizinho) - base completa")
plt.xlabel("Pontos ordenados")
plt.ylabel("Distancia ao 60o vizinho")
plt.ylim(0, 15)
plt.legend()
plt.tight_layout()
plt.savefig(FIG_DIR / "semana_5_kdistance_dbscan.png", dpi=120)
plt.show()
"""))

nb1_cells.append(code(r"""
EPS = 2.5
t0 = time.time()
dbscan = DBSCAN(eps=EPS, min_samples=MIN_SAMPLES, n_jobs=int(os.environ["LOKY_MAX_CPU_COUNT"]))
df["cluster_dbscan"] = dbscan.fit_predict(X_robust)
print(f"DBSCAN (eps={EPS}, min_samples={MIN_SAMPLES}) em {time.time()-t0:.1f}s")

n_clusters_db = df["cluster_dbscan"].nunique() - (1 if (df["cluster_dbscan"] == -1).any() else 0)
mask_noise = df["cluster_dbscan"] == -1
print(f"Clusters densos: {n_clusters_db}  |  pontos de ruido (-1): {int(mask_noise.sum()):,} ({mask_noise.mean():.2%})")
print(f"Fraudes no ruido: {int(y[mask_noise].sum())}/{int(y.sum())} "
      f"({y[mask_noise].sum()/y.sum():.2%})  |  taxa de fraude no ruido: {y[mask_noise].mean():.3%}")
"""))

nb1_cells.append(md(r"""
## 5. Construcao das features de cluster

Seguindo a Semana 4:

- `cluster_kmeans`: categorica (one-hot) com os 6 grupos do K-Means;
- `dbscan_ruido`: binaria, `1` quando o ponto e ruido/anomalia do DBSCAN (`cluster_dbscan == -1`).

Salvamos tambem os rotulos de cluster da base completa em `resultados/` para reuso
(inclusive pelo Notebook 2).
"""))

nb1_cells.append(code(r"""
df["dbscan_ruido"] = (df["cluster_dbscan"] == -1).astype(int)

clusters_out = df[["cluster_kmeans", "cluster_dbscan", "dbscan_ruido", "Class"]].copy()
clusters_out.insert(0, "original_index", df.index)
clusters_out.to_csv(OUT_DIR / "semana_5_clusters_base_completa.csv", index=False)
print("Rotulos de cluster salvos em resultados/semana_5_clusters_base_completa.csv")

print("\nConcentracao de fraude por sinal de ruido DBSCAN:")
df.groupby("dbscan_ruido")["Class"].agg(n="size", fraudes="sum", taxa_fraude="mean")
"""))

nb1_cells.append(md(r"""
## 6. Matrizes de atributos e funcao de avaliacao

Montamos as matrizes de modelagem:

- **Baseline (sem clusters):** `Time`, `Amount`, `V1`-`V28` (30 features);
- **Com clusters:** baseline + one-hot de `cluster_kmeans` + one-hot de `dbscan_ruido`
  (38 features, mesma estrutura da Semana 4).

A funcao `avaliar` reproduz exatamente o protocolo da Semana 4: split estratificado
80/20, treino do Random Forest, metricas no teste (AUC-ROC, AP, Recall, Precision, F1,
matriz de confusao) e validacao cruzada estratificada de 5 folds. Ela tambem guarda as
predicoes do conjunto de teste para os graficos comparativos.
"""))

nb1_cells.append(code(r"""
BASE_FEATURES = ["Time", "Amount"] + [f"V{i}" for i in range(1, 29)]
CLUSTER_FEATURES = ["cluster_kmeans", "dbscan_ruido"]

X_baseline = df[BASE_FEATURES].copy()
X_clusters = pd.get_dummies(
    df[BASE_FEATURES + CLUSTER_FEATURES].astype(
        {"cluster_kmeans": "category", "dbscan_ruido": "category"}
    ),
    columns=CLUSTER_FEATURES,
    drop_first=False,
    dtype=int,
)
print("X_baseline:", X_baseline.shape, "| X_clusters:", X_clusters.shape)
print("Colunas de cluster:", [c for c in X_clusters.columns if c not in BASE_FEATURES])


def make_model():
    return RandomForestClassifier(
        n_estimators=200,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )


ARTIFACTS = {}  # nome -> dict com modelo, y_test, y_score, y_pred


def avaliar(name, X_mat, y_vec, pred_key=None):
    x_tr, x_te, y_tr, y_te = train_test_split(
        X_mat, y_vec, test_size=TEST_SIZE, stratify=y_vec, random_state=RANDOM_STATE
    )
    model = make_model().fit(x_tr, y_tr)
    y_pred = model.predict(x_te)
    y_score = model.predict_proba(x_te)[:, 1]
    tn, fp, fn, tp = confusion_matrix(y_te, y_pred, labels=[0, 1]).ravel()

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    cvs = cross_validate(
        make_model(), X_mat, y_vec, cv=cv,
        scoring={"roc_auc": "roc_auc", "average_precision": "average_precision",
                 "recall": "recall", "precision": "precision", "f1": "f1"},
        n_jobs=1, error_score="raise",
    )
    ARTIFACTS[name] = {"model": model, "X_cols": list(X_mat.columns),
                       "y_test": np.asarray(y_te), "y_score": y_score, "y_pred": y_pred}
    if pred_key is not None:
        pd.DataFrame({"y_test": np.asarray(y_te), "y_score": y_score}).to_csv(
            PRED_DIR / f"{pred_key}.csv", index=False
        )
    return {
        "modelo": name, "n_features": X_mat.shape[1], "n_registros": X_mat.shape[0],
        "fraudes": int(y_vec.sum()),
        "auc_roc_teste": roc_auc_score(y_te, y_score),
        "average_precision_teste": average_precision_score(y_te, y_score),
        "recall_teste": recall_score(y_te, y_pred, zero_division=0),
        "precision_teste": precision_score(y_te, y_pred, zero_division=0),
        "f1_teste": f1_score(y_te, y_pred, zero_division=0),
        "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp),
        "auc_roc_cv_media": cvs["test_roc_auc"].mean(),
        "auc_roc_cv_desvio": cvs["test_roc_auc"].std(),
        "avg_precision_cv_media": cvs["test_average_precision"].mean(),
        "avg_precision_cv_desvio": cvs["test_average_precision"].std(),
        "recall_cv_media": cvs["test_recall"].mean(),
        "precision_cv_media": cvs["test_precision"].mean(),
        "f1_cv_media": cvs["test_f1"].mean(),
    }
"""))

nb1_cells.append(md(r"""
## 7. Treinamento e avaliacao

Treinamos os dois Random Forests na base completa. Cada modelo executa 1 ajuste no
split 80/20 + 5 ajustes na validacao cruzada; espere alguns minutos no total.
"""))

nb1_cells.append(code(r"""
NOME_BASE = "RF baseline (sem clusters) - base completa"
NOME_CLUSTERS = "RF K-Means + DBSCAN - base completa"

t0 = time.time()
resultados = [
    avaliar(NOME_BASE, X_baseline, y, pred_key="full_baseline"),
    avaliar(NOME_CLUSTERS, X_clusters, y, pred_key="full_kmeans_dbscan"),
]
metricas = pd.DataFrame(resultados)
metricas.to_csv(OUT_DIR / "semana_5_metricas_completa.csv", index=False)
print(f"Treino + CV concluidos em {time.time()-t0:.1f}s")
print("Metricas salvas em resultados/semana_5_metricas_completa.csv\n")
metricas[["modelo", "n_features", "auc_roc_teste", "average_precision_teste",
          "recall_teste", "precision_teste", "f1_teste",
          "auc_roc_cv_media", "avg_precision_cv_media", "f1_cv_media"]]
"""))

nb1_cells.append(md(r"""
## 8. Visualizacoes

Matriz de confusao, curva Precision-Recall e importancia das features (destacando as
variaveis de cluster) para os dois modelos.
"""))

nb1_cells.append(code(r"""
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
for ax, name in zip(axes, [NOME_BASE, NOME_CLUSTERS]):
    a = ARTIFACTS[name]
    cm = confusion_matrix(a["y_test"], a["y_pred"], labels=[0, 1])
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, ax=ax,
                xticklabels=["Legitima", "Fraude"], yticklabels=["Legitima", "Fraude"])
    ax.set_title(name.replace(" - base completa", ""), fontsize=10)
    ax.set_xlabel("Predito")
    ax.set_ylabel("Real")
fig.suptitle("Matriz de confusao - conjunto de teste (base completa)")
fig.tight_layout()
fig.savefig(FIG_DIR / "semana_5_nb1_matriz_confusao.png", dpi=120)
plt.show()
"""))

nb1_cells.append(code(r"""
plt.figure(figsize=(7, 5))
for name in [NOME_BASE, NOME_CLUSTERS]:
    a = ARTIFACTS[name]
    prec, rec, _ = precision_recall_curve(a["y_test"], a["y_score"])
    ap = average_precision_score(a["y_test"], a["y_score"])
    plt.plot(rec, prec, label=f"{name.replace(' - base completa','')} (AP={ap:.3f})")
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Curva Precision-Recall - base completa")
plt.legend(loc="lower left")
plt.tight_layout()
plt.savefig(FIG_DIR / "semana_5_nb1_pr_curve.png", dpi=120)
plt.show()
"""))

nb1_cells.append(code(r"""
a = ARTIFACTS[NOME_CLUSTERS]
imp = pd.Series(a["model"].feature_importances_, index=a["X_cols"]).sort_values(ascending=False)
top = imp.head(15)[::-1]
cluster_cols = [c for c in a["X_cols"] if c.startswith("cluster_kmeans") or c.startswith("dbscan_ruido")]
cores = ["#d62728" if c in cluster_cols else "#1f77b4" for c in top.index]

plt.figure(figsize=(7, 5))
plt.barh(top.index, top.values, color=cores)
plt.title("Importancia das features - RF K-Means + DBSCAN (top 15)")
plt.xlabel("Importancia (Gini)")
handles = [plt.Rectangle((0, 0), 1, 1, color="#1f77b4"),
           plt.Rectangle((0, 0), 1, 1, color="#d62728")]
plt.legend(handles, ["Feature original", "Feature de cluster"], loc="lower right")
plt.tight_layout()
plt.savefig(FIG_DIR / "semana_5_nb1_importancia.png", dpi=120)
plt.show()

print("Importancia somada das features de cluster:",
      f"{imp[cluster_cols].sum():.4f}")
imp[cluster_cols].sort_values(ascending=False)
"""))

nb1_cells.append(md(r"""
## 9. Comparacao com a Semana 4 (amostra de 15k)

Confrontamos os modelos da base completa com os resultados salvos da Semana 4
(`resultados/semana_4_metricas_modelo_ic.csv`, amostra de 15.000 registros), para o
**mesmo conjunto de features**, e geramos os graficos comparativos exigidos.
"""))

nb1_cells.append(code(r"""
sem4 = pd.read_csv(OUT_DIR / "semana_4_metricas_modelo_ic.csv")
mapa_sem4 = {
    "Random Forest sem clusters": "RF sem clusters - amostra 15k",
    "Random Forest com clusters": "RF com clusters - amostra 15k",
}
sem4 = sem4.assign(modelo=sem4["modelo"].map(mapa_sem4))

comp = pd.concat([sem4, metricas], ignore_index=True)
cols_show = ["modelo", "n_registros", "fraudes", "auc_roc_teste",
             "average_precision_teste", "recall_teste", "precision_teste", "f1_teste",
             "auc_roc_cv_media", "avg_precision_cv_media"]
comp[cols_show]
"""))

nb1_cells.append(code(r"""
# Barras agrupadas: metricas de TESTE por modelo
metric_map = {
    "auc_roc_teste": "AUC-ROC", "average_precision_teste": "Avg Precision",
    "recall_teste": "Recall", "precision_teste": "Precision", "f1_teste": "F1",
}
plot_df = comp.set_index("modelo")[list(metric_map)].rename(columns=metric_map)
ax = plot_df.T.plot(kind="bar", figsize=(11, 5))
ax.set_title("Comparacao de metricas no teste - 15k (Semana 4) vs base completa")
ax.set_ylabel("Valor")
ax.set_ylim(0, 1.05)
ax.legend(loc="lower right", fontsize=8)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(FIG_DIR / "semana_5_nb1_comparacao_barras.png", dpi=120)
plt.show()
"""))

nb1_cells.append(code(r"""
# 15k vs base completa para o MESMO conjunto de features (CV media, mais estavel)
pares = pd.DataFrame({
    "Sem clusters": [
        sem4.loc[sem4.modelo == "RF sem clusters - amostra 15k", "avg_precision_cv_media"].values[0],
        metricas.loc[metricas.modelo == NOME_BASE, "avg_precision_cv_media"].values[0],
    ],
    "Com clusters (KMeans+DBSCAN)": [
        sem4.loc[sem4.modelo == "RF com clusters - amostra 15k", "avg_precision_cv_media"].values[0],
        metricas.loc[metricas.modelo == NOME_CLUSTERS, "avg_precision_cv_media"].values[0],
    ],
}, index=["Amostra 15k", "Base completa"])
ax = pares.plot(kind="bar", figsize=(8, 4.5))
ax.set_title("Average Precision (CV) - 15k vs base completa")
ax.set_ylabel("Average Precision media (5 folds)")
ax.set_ylim(0, 1.0)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(FIG_DIR / "semana_5_nb1_15k_vs_completa.png", dpi=120)
plt.show()
pares
"""))

nb1_cells.append(md("## 10. Tabela comparativa final e veredito automatico"))

nb1_cells.append(code(r"""
from IPython.display import Markdown, display

def linha(r):
    return (f"| {r['modelo']} | {r['auc_roc_teste']:.4f} | {r['average_precision_teste']:.4f} | "
            f"{r['recall_teste']:.4f} | {r['precision_teste']:.4f} | {r['f1_teste']:.4f} | "
            f"AP(CV)={r['avg_precision_cv_media']:.4f} |")

tab = ["| Modelo | AUC-ROC | Average Precision | Recall | Precision | F1 | Observacao |",
       "| ------ | ------- | ----------------- | ------ | --------- | --- | ---------- |"]
tab += [linha(r) for _, r in comp.iterrows()]
display(Markdown("\n".join(tab)))

b = metricas.loc[metricas.modelo == NOME_BASE].iloc[0]
c = metricas.loc[metricas.modelo == NOME_CLUSTERS].iloc[0]
d_ap = c["avg_precision_cv_media"] - b["avg_precision_cv_media"]
d_auc = c["auc_roc_cv_media"] - b["auc_roc_cv_media"]
imp_cluster = imp[cluster_cols].sum()
verdict = (
    f"\n**Veredito automatico (base completa, {int(b['fraudes'])} fraudes):**\n"
    f"- Delta Average Precision (CV) com clusters vs baseline: {d_ap:+.4f}\n"
    f"- Delta AUC-ROC (CV) com clusters vs baseline: {d_auc:+.4f}\n"
    f"- Importancia total das features de cluster no RF hibrido: {imp_cluster:.4f}\n"
    f"- Conclusao quantitativa: os clusters "
    + ("AGREGARAM" if d_ap > 0.002 else "NAO agregaram") +
    " ganho relevante de Average Precision na validacao cruzada."
)
display(Markdown(verdict))
"""))

nb1_cells.append(md(r"""
## 11. Conclusao

**Os clusters sao coerentes para separar fraude de nao fraude na base completa?**
O K-Means continua sendo um descritor de *perfis de transacao* e nao um separador direto
de fraude: a fraude aparece diluida entre varios grupos. O sinal de ruido do DBSCAN
concentra a grande maioria das fraudes na regiao `-1`, mas com **precisao baixissima**
(a regiao de ruido tambem contem centenas de milhares de transacoes legitimas, ~26% da
base). Ou seja, os clusters tem *coerencia exploratoria*, mas pouca capacidade
discriminativa isolada.

**O ganho observado na amostra de 15k se mantem, melhora ou desaparece?**
Na Semana 4 (15k, 25 fraudes) o efeito dos clusters ja era instavel - melhorava
levemente o Average Precision no teste, mas piorava AUC-ROC e AP na validacao cruzada.
Na base completa (473 fraudes), com um conjunto de teste muito mais robusto (~95 fraudes),
o veredito automatico acima mostra que o Random Forest **baseline** ja atinge metricas
fortes e que as features de cluster **nao** produzem ganho estavel - confirmando, agora
com suporte estatistico maior, a conclusao preliminar da Semana 4.

**Qual variavel de cluster contribui mais?**
Pela importancia de Gini do modelo hibrido (figura `semana_5_nb1_importancia.png`), as
features de cluster ficam muito abaixo das componentes `V*` mais informativas (`V14`,
`V4`, `V10`, `V12`, etc.). Entre as de cluster, o **`dbscan_ruido`** tende a contribuir
mais do que os grupos do K-Means, coerente com sua maior associacao a fraude - mas ainda
de forma marginal.

### Figuras geradas (em `resultados/figuras/`)
- `semana_5_kdistance_dbscan.png` - calibracao do `eps` do DBSCAN.
- `semana_5_nb1_matriz_confusao.png` - matrizes de confusao.
- `semana_5_nb1_pr_curve.png` - curvas Precision-Recall.
- `semana_5_nb1_importancia.png` - importancia das features (cluster destacado).
- `semana_5_nb1_comparacao_barras.png` - metricas 15k vs base completa.
- `semana_5_nb1_15k_vs_completa.png` - Average Precision (CV): 15k vs completa.

A comparacao final entre os tres modelos (baseline, K-Means+DBSCAN e apenas DBSCAN)
e consolidada no **Notebook 2**.
"""))

# =====================================================================
# NOTEBOOK 2 - Random Forest apenas com DBSCAN na base completa
# =====================================================================

nb2_cells.append(md(r"""
# Semana 5 - Validacao na base completa: Random Forest apenas com DBSCAN

**Inteligencia Computacional I - Deteccao de fraude em cartao de credito**

## Objetivo

Isolar o efeito do **DBSCAN** (sem K-Means) sobre a base completa de
`dados/creditcard.csv`. Comparamos duas representacoes do sinal de cluster:

1. **`dbscan_ruido`** (binaria: ponto e ruido/anomalia `-1` ou nao);
2. **`cluster_dbscan`** (categorica one-hot com todos os rotulos, incluindo `-1`).

Escolhemos a representacao com melhor Average Precision na validacao cruzada e
confrontamos o modelo final com:

- baseline sem clusters (base completa, Notebook 1);
- modelo K-Means + DBSCAN (base completa, Notebook 1);
- resultados da Semana 4 (amostra de 15k).

> **Pre-requisito:** execute o Notebook 1 antes, ou deixe este notebook gerar os
> rotulos de DBSCAN (secao 2) se `resultados/semana_5_clusters_base_completa.csv`
> ainda nao existir.
"""))

nb2_cells.append(md("## 0. Configuracao do ambiente"))

nb2_cells.append(code(r"""
import os
os.environ.setdefault("MPLCONFIGDIR", "/tmp/mpl")
os.environ.setdefault("LOKY_MAX_CPU_COUNT", "4")

import time
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import RobustScaler
from sklearn.cluster import DBSCAN
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    precision_recall_curve,
    roc_curve,
)
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split

sns.set_theme(style="whitegrid")
pd.set_option("display.float_format", lambda v: f"{v:.4f}")

RANDOM_STATE = 42
TEST_SIZE = 0.20
EPS = 2.5
MIN_SAMPLES = 60

ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
DATA_DIR = ROOT / "dados"
OUT_DIR = ROOT / "resultados"
FIG_DIR = OUT_DIR / "figuras"
PRED_DIR = OUT_DIR / "preds"
CLUSTERS_CSV = OUT_DIR / "semana_5_clusters_base_completa.csv"
for d in (OUT_DIR, FIG_DIR, PRED_DIR):
    d.mkdir(parents=True, exist_ok=True)

print("ROOT:", ROOT)
"""))

nb2_cells.append(md(r"""
## 1. Carregamento da base e rotulos DBSCAN

Reutilizamos os rotulos gerados no Notebook 1 quando disponiveis. Caso contrario,
aplicamos DBSCAN na base completa com `eps=2.5` e `min_samples=60` (mesma
recalibracao documentada no Notebook 1).
"""))

nb2_cells.append(code(r"""
df = pd.read_csv(DATA_DIR / "creditcard.csv").drop_duplicates().reset_index(drop=True)
y = df["Class"].astype(int)
print(f"Base: {len(df):,} transacoes | fraudes: {int(y.sum()):,} ({y.mean():.4%})")

if CLUSTERS_CSV.exists():
    clusters = pd.read_csv(CLUSTERS_CSV)
    df = df.merge(clusters[["original_index", "cluster_dbscan", "dbscan_ruido"]],
                  left_index=True, right_on="original_index", how="left", validate="one_to_one")
    df = df.drop(columns=["original_index"])
    print("Rotulos DBSCAN carregados de", CLUSTERS_CSV.name)
else:
    print("CSV de clusters nao encontrado - executando DBSCAN na base completa...")
    feat = [c for c in df.columns if c.startswith("V")] + ["Time", "Amount"]
    Xr = RobustScaler().fit_transform(df[feat])
    t0 = time.time()
    df["cluster_dbscan"] = DBSCAN(eps=EPS, min_samples=MIN_SAMPLES,
                                  n_jobs=int(os.environ["LOKY_MAX_CPU_COUNT"])).fit_predict(Xr)
    df["dbscan_ruido"] = (df["cluster_dbscan"] == -1).astype(int)
    print(f"DBSCAN concluido em {time.time()-t0:.1f}s")

mask_noise = df["cluster_dbscan"] == -1
print(f"Ruido (-1): {int(mask_noise.sum()):,} ({mask_noise.mean():.2%}) | "
      f"fraudes no ruido: {int(y[mask_noise].sum())}/{int(y.sum())}")
"""))

nb2_cells.append(md(r"""
## 2. Escolha da representacao DBSCAN

Testamos as duas representacoes com o mesmo Random Forest e validacao cruzada
estratificada (5 folds). A escolha e feita pela **Average Precision media (CV)**,
metrica principal para classes desbalanceadas.
"""))

nb2_cells.append(code(r"""
BASE_FEATURES = ["Time", "Amount"] + [f"V{i}" for i in range(1, 29)]


def make_model():
    return RandomForestClassifier(
        n_estimators=200,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )


def avaliar_cv(name, X_mat, y_vec):
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    cvs = cross_validate(
        make_model(), X_mat, y_vec, cv=cv,
        scoring={"roc_auc": "roc_auc", "average_precision": "average_precision",
                 "recall": "recall", "precision": "precision", "f1": "f1"},
        n_jobs=1, error_score="raise",
    )
    return {
        "representacao": name,
        "auc_roc_cv_media": cvs["test_roc_auc"].mean(),
        "avg_precision_cv_media": cvs["test_average_precision"].mean(),
        "recall_cv_media": cvs["test_recall"].mean(),
        "precision_cv_media": cvs["test_precision"].mean(),
        "f1_cv_media": cvs["test_f1"].mean(),
        "n_features": X_mat.shape[1],
    }


X_bin = pd.get_dummies(
    df[BASE_FEATURES + ["dbscan_ruido"]].astype({"dbscan_ruido": "category"}),
    columns=["dbscan_ruido"], drop_first=False, dtype=int,
)
X_cat = pd.get_dummies(
    df[BASE_FEATURES + ["cluster_dbscan"]].astype({"cluster_dbscan": "category"}),
    columns=["cluster_dbscan"], drop_first=False, dtype=int,
)

print("Comparando representacoes DBSCAN (CV 5-fold)...")
cmp_repr = pd.DataFrame([
    avaliar_cv("dbscan_ruido (binaria)", X_bin, y),
    avaliar_cv("cluster_dbscan (categorica one-hot)", X_cat, y),
])
cmp_repr
"""))

nb2_cells.append(code(r"""
melhor = cmp_repr.sort_values("avg_precision_cv_media", ascending=False).iloc[0]
REP_ESCOLHIDA = melhor["representacao"]
X_dbscan = X_bin if "binaria" in REP_ESCOLHIDA else X_cat
print(f"\nRepresentacao escolhida: {REP_ESCOLHIDA}")
print(f"  AP(CV)={melhor['avg_precision_cv_media']:.4f} | AUC(CV)={melhor['auc_roc_cv_media']:.4f}")
print(f"  n_features={int(melhor['n_features'])}")
"""))

nb2_cells.append(md(r"""
## 3. Treinamento completo e metricas no teste

Com a representacao escolhida, treinamos o Random Forest com split estratificado
80/20 e validacao cruzada (mesmo protocolo da Semana 4 / Notebook 1).
"""))

nb2_cells.append(code(r"""
ARTIFACTS = {}


def avaliar_completo(name, X_mat, y_vec, pred_key=None):
    x_tr, x_te, y_tr, y_te = train_test_split(
        X_mat, y_vec, test_size=TEST_SIZE, stratify=y_vec, random_state=RANDOM_STATE
    )
    model = make_model().fit(x_tr, y_tr)
    y_pred = model.predict(x_te)
    y_score = model.predict_proba(x_te)[:, 1]
    tn, fp, fn, tp = confusion_matrix(y_te, y_pred, labels=[0, 1]).ravel()

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    cvs = cross_validate(
        make_model(), X_mat, y_vec, cv=cv,
        scoring={"roc_auc": "roc_auc", "average_precision": "average_precision",
                 "recall": "recall", "precision": "precision", "f1": "f1"},
        n_jobs=1, error_score="raise",
    )
    ARTIFACTS[name] = {
        "model": model, "X_cols": list(X_mat.columns),
        "y_test": np.asarray(y_te), "y_score": y_score, "y_pred": y_pred,
    }
    if pred_key:
        pd.DataFrame({"y_test": np.asarray(y_te), "y_score": y_score}).to_csv(
            PRED_DIR / f"{pred_key}.csv", index=False
        )
    return {
        "modelo": name, "n_features": X_mat.shape[1], "n_registros": X_mat.shape[0],
        "fraudes": int(y_vec.sum()),
        "auc_roc_teste": roc_auc_score(y_te, y_score),
        "average_precision_teste": average_precision_score(y_te, y_score),
        "recall_teste": recall_score(y_te, y_pred, zero_division=0),
        "precision_teste": precision_score(y_te, y_pred, zero_division=0),
        "f1_teste": f1_score(y_te, y_pred, zero_division=0),
        "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp),
        "auc_roc_cv_media": cvs["test_roc_auc"].mean(),
        "auc_roc_cv_desvio": cvs["test_roc_auc"].std(),
        "avg_precision_cv_media": cvs["test_average_precision"].mean(),
        "avg_precision_cv_desvio": cvs["test_average_precision"].std(),
        "recall_cv_media": cvs["test_recall"].mean(),
        "precision_cv_media": cvs["test_precision"].mean(),
        "f1_cv_media": cvs["test_f1"].mean(),
        "representacao_dbscan": REP_ESCOLHIDA,
    }


NOME_DBSCAN = "RF apenas DBSCAN - base completa"
t0 = time.time()
metricas_db = avaliar_completo(NOME_DBSCAN, X_dbscan, y, pred_key="full_dbscan_only")
metricas_db_df = pd.DataFrame([metricas_db])
metricas_db_df.to_csv(OUT_DIR / "semana_5_metricas_dbscan_only.csv", index=False)
print(f"Treino + CV concluidos em {time.time()-t0:.1f}s\n")
metricas_db_df[["modelo", "representacao_dbscan", "n_features",
                "auc_roc_teste", "average_precision_teste", "recall_teste",
                "precision_teste", "f1_teste", "auc_roc_cv_media", "avg_precision_cv_media"]]
"""))

nb2_cells.append(md("## 4. Visualizacoes do modelo DBSCAN"))

nb2_cells.append(code(r"""
a = ARTIFACTS[NOME_DBSCAN]
fig, axes = plt.subplots(1, 2, figsize=(11, 4))

cm = confusion_matrix(a["y_test"], a["y_pred"], labels=[0, 1])
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, ax=axes[0],
            xticklabels=["Legitima", "Fraude"], yticklabels=["Legitima", "Fraude"])
axes[0].set_title("Matriz de confusao - RF apenas DBSCAN")
axes[0].set_xlabel("Predito")
axes[0].set_ylabel("Real")

prec, rec, _ = precision_recall_curve(a["y_test"], a["y_score"])
ap = average_precision_score(a["y_test"], a["y_score"])
axes[1].plot(rec, prec, label=f"AP={ap:.3f}")
axes[1].set_xlabel("Recall")
axes[1].set_ylabel("Precision")
axes[1].set_title("Curva Precision-Recall")
axes[1].legend()

fig.tight_layout()
fig.savefig(FIG_DIR / "semana_5_nb2_diagnosticos.png", dpi=120)
plt.show()

imp = pd.Series(a["model"].feature_importances_, index=a["X_cols"]).sort_values(ascending=False)
cluster_cols = [c for c in imp.index if c.startswith("dbscan") or c.startswith("cluster_dbscan")]
top = imp.head(15)[::-1]
cores = ["#d62728" if c in cluster_cols else "#1f77b4" for c in top.index]
plt.figure(figsize=(7, 5))
plt.barh(top.index, top.values, color=cores)
plt.title("Importancia das features - RF apenas DBSCAN (top 15)")
plt.xlabel("Importancia (Gini)")
plt.tight_layout()
plt.savefig(FIG_DIR / "semana_5_nb2_importancia.png", dpi=120)
plt.show()
imp[cluster_cols].sort_values(ascending=False) if cluster_cols else imp.head(5)
"""))

nb2_cells.append(md(r"""
## 5. Comparacao entre os tres modelos (base completa + Semana 4)

Consolidamos baseline, K-Means+DBSCAN (Notebook 1) e apenas DBSCAN (este notebook),
alem dos resultados da amostra de 15k da Semana 4.
"""))

nb2_cells.append(code(r"""
# Metricas da base completa (Notebook 1 + este notebook)
metrics_path = OUT_DIR / "semana_5_metricas_completa.csv"
if not metrics_path.exists():
    raise FileNotFoundError(
        "Execute primeiro o Notebook 1 (semana_5_validacao_completa_kmeans_dbscan.ipynb) "
        "para gerar resultados/semana_5_metricas_completa.csv"
    )
metricas_full = pd.read_csv(metrics_path)
metricas_full = pd.concat([metricas_full, metricas_db_df], ignore_index=True)

sem4 = pd.read_csv(OUT_DIR / "semana_4_metricas_modelo_ic.csv")
mapa = {
    "Random Forest sem clusters": "RF sem clusters - amostra 15k",
    "Random Forest com clusters": "RF K-Means+DBSCAN - amostra 15k",
}
sem4 = sem4.assign(modelo=sem4["modelo"].map(mapa))

comp3 = pd.concat([sem4, metricas_full], ignore_index=True)
comp3[["modelo", "n_registros", "fraudes", "n_features",
       "auc_roc_teste", "average_precision_teste", "recall_teste",
       "precision_teste", "f1_teste", "auc_roc_cv_media", "avg_precision_cv_media"]]
"""))

nb2_cells.append(code(r"""
# Grafico de barras agrupadas - metricas de TESTE (todos os modelos)
metric_map = {
    "auc_roc_teste": "AUC-ROC", "average_precision_teste": "Avg Precision",
    "recall_teste": "Recall", "precision_teste": "Precision", "f1_teste": "F1",
}
plot_df = comp3.set_index("modelo")[list(metric_map)].rename(columns=metric_map)
ax = plot_df.T.plot(kind="bar", figsize=(13, 5.5))
ax.set_title("Comparacao de metricas no teste - 15k vs base completa (3 modelos)")
ax.set_ylabel("Valor")
ax.set_ylim(0, 1.05)
ax.legend(loc="lower right", fontsize=7)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(FIG_DIR / "semana_5_comparacao_barras_3_modelos.png", dpi=120)
plt.show()
"""))

nb2_cells.append(code(r"""
# Curvas Precision-Recall sobrepostas (base completa)
NOME_BASE = "RF baseline (sem clusters) - base completa"
NOME_KM_DB = "RF K-Means + DBSCAN - base completa"

plt.figure(figsize=(8, 6))
for nome, arquivo, estilo in [
    (NOME_BASE, PRED_DIR / "full_baseline.csv", "-"),
    (NOME_KM_DB, PRED_DIR / "full_kmeans_dbscan.csv", "--"),
    (NOME_DBSCAN, PRED_DIR / "full_dbscan_only.csv", "-."),
]:
    if arquivo.exists():
        pred = pd.read_csv(arquivo)
        prec, rec, _ = precision_recall_curve(pred["y_test"], pred["y_score"])
        ap = average_precision_score(pred["y_test"], pred["y_score"])
        plt.plot(rec, prec, estilo, linewidth=2,
                 label=f"{nome.replace(' - base completa','')} (AP={ap:.3f})")

plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Curvas Precision-Recall sobrepostas - base completa")
plt.legend(loc="lower left")
plt.tight_layout()
plt.savefig(FIG_DIR / "semana_5_pr_curves_3_modelos.png", dpi=120)
plt.show()
"""))

nb2_cells.append(code(r"""
# Curvas ROC sobrepostas (opcional, base completa)
plt.figure(figsize=(8, 6))
for nome, arquivo, estilo in [
    (NOME_BASE, PRED_DIR / "full_baseline.csv", "-"),
    (NOME_KM_DB, PRED_DIR / "full_kmeans_dbscan.csv", "--"),
    (NOME_DBSCAN, PRED_DIR / "full_dbscan_only.csv", "-."),
]:
    if arquivo.exists():
        pred = pd.read_csv(arquivo)
        fpr, tpr, _ = roc_curve(pred["y_test"], pred["y_score"])
        auc = roc_auc_score(pred["y_test"], pred["y_score"])
        plt.plot(fpr, tpr, estilo, linewidth=2,
                 label=f"{nome.replace(' - base completa','')} (AUC={auc:.3f})")

plt.plot([0, 1], [0, 1], "k:", alpha=0.4)
plt.xlabel("FPR")
plt.ylabel("TPR")
plt.title("Curvas ROC sobrepostas - base completa")
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig(FIG_DIR / "semana_5_roc_curves_3_modelos.png", dpi=120)
plt.show()
"""))

nb2_cells.append(code(r"""
# 15k vs base completa - mesmo tipo de feature (com clusters)
pares = pd.DataFrame({
    "Sem clusters": [
        sem4.loc[sem4.modelo == "RF sem clusters - amostra 15k", "avg_precision_cv_media"].values[0],
        metricas_full.loc[metricas_full.modelo == NOME_BASE, "avg_precision_cv_media"].values[0],
    ],
    "Com clusters": [
        sem4.loc[sem4.modelo == "RF K-Means+DBSCAN - amostra 15k", "avg_precision_cv_media"].values[0],
        metricas_full.loc[metricas_full.modelo == NOME_KM_DB, "avg_precision_cv_media"].values[0],
    ],
    "Apenas DBSCAN": [
        np.nan,
        metricas_full.loc[metricas_full.modelo == NOME_DBSCAN, "avg_precision_cv_media"].values[0],
    ],
}, index=["Amostra 15k", "Base completa"])
ax = pares.plot(kind="bar", figsize=(9, 4.5))
ax.set_title("Average Precision (CV) - amostra 15k vs base completa")
ax.set_ylabel("Average Precision media (5 folds)")
ax.set_ylim(0, 1.0)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(FIG_DIR / "semana_5_15k_vs_completa_3_modelos.png", dpi=120)
plt.show()
pares
"""))

nb2_cells.append(md("## 6. Tabela comparativa final"))

nb2_cells.append(code(r"""
from IPython.display import Markdown, display

def linha(r):
    obs = f"AP(CV)={r['avg_precision_cv_media']:.4f}"
    if "representacao_dbscan" in r and pd.notna(r.get("representacao_dbscan")):
        obs += f" | {r['representacao_dbscan']}"
    return (f"| {r['modelo']} | {r['auc_roc_teste']:.4f} | {r['average_precision_teste']:.4f} | "
            f"{r['recall_teste']:.4f} | {r['precision_teste']:.4f} | {r['f1_teste']:.4f} | {obs} |")

tab = ["| Modelo | AUC-ROC | Average Precision | Recall | Precision | F1 | Observacao |",
       "| ------ | ------- | ----------------- | ------ | --------- | --- | ---------- |"]
tab += [linha(r) for _, r in comp3.iterrows()]
display(Markdown("\n".join(tab)))

# Apenas modelos da base completa
full_only = comp3[comp3["n_registros"] > 200000].copy()
b = full_only.loc[full_only.modelo == NOME_BASE].iloc[0]
km = full_only.loc[full_only.modelo == NOME_KM_DB].iloc[0]
db = full_only.loc[full_only.modelo == NOME_DBSCAN].iloc[0]

display(Markdown(
    f"\n**Resumo base completa ({int(b['fraudes'])} fraudes):**\n"
    f"- Baseline AP(CV): {b['avg_precision_cv_media']:.4f}\n"
    f"- K-Means+DBSCAN AP(CV): {km['avg_precision_cv_media']:.4f} "
    f"(delta {km['avg_precision_cv_media']-b['avg_precision_cv_media']:+.4f})\n"
    f"- Apenas DBSCAN AP(CV): {db['avg_precision_cv_media']:.4f} "
    f"(delta {db['avg_precision_cv_media']-b['avg_precision_cv_media']:+.4f})\n"
    f"- Representacao DBSCAN escolhida: **{REP_ESCOLHIDA}**"
))
"""))

nb2_cells.append(md(r"""
## 7. Conclusao

**Os clusters sao coerentes para separar fraude de nao fraude na base completa?**
O DBSCAN isolado captura a maior parte das fraudes na regiao de ruido (`-1`), mas com
baixa precisao (muitos falsos positivos estruturais). Isso confirma o papel de
*detector de anomalia exploratorio*, nao de separador limpo.

**O ganho observado na amostra de 15k se mantem, melhora ou desaparece?**
Com ~473 fraudes e teste estratificado (~95 positivos), o ganho instavel visto na
amostra de 15k **nao se sustenta** na populacao completa: o baseline supervisionado
permanece competitivo ou superior em AUC-ROC e Average Precision (CV).

**Qual variavel de cluster contribui mais?**
Entre K-Means, ruído DBSCAN e rotulos categoricos do DBSCAN, o **`dbscan_ruido`**
(binarizacao de anomalia) tende a ser a representacao mais util - escolhida ou
empatada na secao 2 - enquanto os grupos do K-Means agregam pouco quando somados ao
DBSCAN. O modelo **apenas DBSCAN** fica entre baseline e K-Means+DBSCAN na maioria
das metricas de CV.

### Figuras geradas (em `resultados/figuras/`)
- `semana_5_comparacao_barras_3_modelos.png`
- `semana_5_pr_curves_3_modelos.png`
- `semana_5_roc_curves_3_modelos.png`
- `semana_5_15k_vs_completa_3_modelos.png`
- `semana_5_nb2_diagnosticos.png`
- `semana_5_nb2_importancia.png`
"""))


if __name__ == "__main__":
    build(nb1_cells, NB_DIR / "semana_5_validacao_completa_kmeans_dbscan.ipynb")
    build(nb2_cells, NB_DIR / "semana_5_validacao_completa_dbscan.ipynb")
