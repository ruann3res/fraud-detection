from __future__ import annotations

import os
import warnings
from pathlib import Path
from typing import Callable

os.environ.setdefault("MPLCONFIGDIR", "/tmp/mpl")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

import gc
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.base import clone
from sklearn.calibration import CalibratedClassifierCV
from sklearn.exceptions import ConvergenceWarning
from sklearn.frozen import FrozenEstimator
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.utils.class_weight import compute_sample_weight


warnings.filterwarnings("ignore", category=ConvergenceWarning)

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "dados"
OUTPUT_DIR = ROOT / "resultados"
PRED_DIR = OUTPUT_DIR / "preds"
FIG_DIR = OUTPUT_DIR / "figuras"

RANDOM_STATE = 42
TEST_SIZE = 0.20
VAL_SIZE = 0.20
CV_SPLITS = 5
MIN_RECALL_THRESHOLD = 0.72

BASE_FEATURES = ["Time", "Amount"] + [f"V{i}" for i in range(1, 29)]
CLUSTER_FEATURES = ["cluster_kmeans", "dbscan_ruido"]

MLP_MODELS = {
    "MLP baseline (sem clusters) - base completa": {
        "pred_key": "mlp_baseline",
        "features": "baseline",
        "observacao": "Baseline neural com 30 features originais.",
    },
    "MLP K-Means + DBSCAN - base completa": {
        "pred_key": "mlp_clusters",
        "features": "clusters",
        "observacao": "Features originais + K-Means one-hot + ruido DBSCAN.",
    },
    "MLP apenas DBSCAN - base completa": {
        "pred_key": "mlp_dbscan",
        "features": "dbscan",
        "observacao": "Features originais + sinal binario de ruido DBSCAN.",
    },
}

MLP_CONFIGS = {
    "MLP (64,32) alpha=1e-4": {"hidden_layer_sizes": (64, 32), "alpha": 1e-4},
    "MLP (32,16) alpha=1e-3": {"hidden_layer_sizes": (32, 16), "alpha": 1e-3},
    "MLP (32,) alpha=1e-3": {"hidden_layer_sizes": (32,), "alpha": 1e-3},
    "MLP (16,) alpha=1e-2": {"hidden_layer_sizes": (16,), "alpha": 1e-2},
}


def load_dataset() -> pd.DataFrame:
    transactions = pd.read_csv(DATA_DIR / "creditcard.csv")
    transactions = transactions.drop_duplicates().reset_index(drop=True)
    transactions = transactions.reset_index().rename(columns={"index": "original_index"})

    clusters = pd.read_csv(OUTPUT_DIR / "semana_5_clusters_base_completa.csv")
    required = {"original_index", "cluster_kmeans", "cluster_dbscan", "dbscan_ruido", "Class"}
    missing = required.difference(clusters.columns)
    if missing:
        raise ValueError(f"Arquivo de clusters sem colunas esperadas: {sorted(missing)}")

    selected = ["original_index", *BASE_FEATURES, "Class"]
    dataset = transactions[selected].merge(
        clusters[["original_index", "cluster_kmeans", "cluster_dbscan", "dbscan_ruido", "Class"]],
        on="original_index",
        how="inner",
        suffixes=("", "_cluster"),
        validate="one_to_one",
    )

    mismatches = (dataset["Class"] != dataset["Class_cluster"]).sum()
    if mismatches:
        raise ValueError(f"Divergencia entre Class da base e dos clusters: {mismatches}")

    return dataset.drop(columns=["Class_cluster"])


def build_feature_matrices(dataset: pd.DataFrame) -> dict[str, pd.DataFrame]:
    x_baseline = dataset[BASE_FEATURES].copy()
    x_clusters = pd.get_dummies(
        dataset[BASE_FEATURES + CLUSTER_FEATURES].astype(
            {"cluster_kmeans": "category", "dbscan_ruido": "category"}
        ),
        columns=CLUSTER_FEATURES,
        drop_first=False,
        dtype=int,
    )
    x_dbscan = pd.get_dummies(
        dataset[BASE_FEATURES + ["dbscan_ruido"]].astype({"dbscan_ruido": "category"}),
        columns=["dbscan_ruido"],
        drop_first=False,
        dtype=int,
    )
    return {"baseline": x_baseline, "clusters": x_clusters, "dbscan": x_dbscan}


def make_mlp_pipeline(
    hidden_layer_sizes: tuple[int, ...] = (64, 32),
    alpha: float = 1e-4,
) -> Pipeline:
    return Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "mlp",
                MLPClassifier(
                    hidden_layer_sizes=hidden_layer_sizes,
                    activation="relu",
                    solver="adam",
                    alpha=alpha,
                    batch_size=256,
                    learning_rate="adaptive",
                    max_iter=300,
                    early_stopping=True,
                    validation_fraction=0.1,
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )


def make_lr_pipeline() -> Pipeline:
    return Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "lr",
                LogisticRegression(
                    class_weight="balanced",
                    max_iter=2000,
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )


def fit_mlp(model: Pipeline, x_train: pd.DataFrame, y_train: pd.Series) -> Pipeline:
    sample_weight = compute_sample_weight(class_weight="balanced", y=y_train)
    model.fit(x_train, y_train, mlp__sample_weight=sample_weight)
    return model


def find_threshold(
    y_true: np.ndarray,
    y_score: np.ndarray,
    min_recall: float = MIN_RECALL_THRESHOLD,
) -> tuple[float, float, float]:
    precision, recall, thresholds = precision_recall_curve(y_true, y_score)
    best_thresh = 0.5
    best_precision = 0.0
    best_recall = 0.0

    for p, r, t in zip(precision[:-1], recall[:-1], thresholds):
        if r >= min_recall and p >= best_precision:
            best_precision = float(p)
            best_recall = float(r)
            best_thresh = float(t)

    if best_precision == 0.0:
        f1_vals = (2 * precision[:-1] * recall[:-1]) / (precision[:-1] + recall[:-1] + 1e-12)
        idx = int(np.argmax(f1_vals))
        best_thresh = float(thresholds[idx])
        best_precision = float(precision[idx])
        best_recall = float(recall[idx])

    return best_thresh, best_precision, best_recall


def metrics_at_threshold(
    y_true: np.ndarray,
    y_score: np.ndarray,
    threshold: float,
) -> dict[str, float | int]:
    y_pred = (y_score >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    return {
        "threshold": threshold,
        "auc_roc_teste": roc_auc_score(y_true, y_score),
        "average_precision_teste": average_precision_score(y_true, y_score),
        "recall_teste": recall_score(y_true, y_pred, zero_division=0),
        "precision_teste": precision_score(y_true, y_pred, zero_division=0),
        "f1_teste": f1_score(y_true, y_pred, zero_division=0),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    }


def metric_row(
    name: str,
    familia: str,
    x: pd.DataFrame,
    y: pd.Series,
    y_test: pd.Series,
    y_pred: np.ndarray,
    y_score: np.ndarray,
    cv_scores: dict[str, list[float]],
    pred_key: str,
    observacao: str,
    threshold: float = 0.5,
    calibrado: bool = False,
) -> dict[str, object]:
    base = metrics_at_threshold(np.asarray(y_test), y_score, threshold)
    return {
        "familia": familia,
        "modelo": name,
        "n_features": x.shape[1],
        "n_registros": x.shape[0],
        "fraudes": int(y.sum()),
        "threshold": threshold,
        "calibrado": calibrado,
        "auc_roc_teste": base["auc_roc_teste"],
        "average_precision_teste": base["average_precision_teste"],
        "recall_teste": base["recall_teste"],
        "precision_teste": base["precision_teste"],
        "f1_teste": base["f1_teste"],
        "tn": base["tn"],
        "fp": base["fp"],
        "fn": base["fn"],
        "tp": base["tp"],
        "auc_roc_cv_media": np.mean(cv_scores["auc_roc"]) if cv_scores["auc_roc"] else np.nan,
        "auc_roc_cv_desvio": np.std(cv_scores["auc_roc"]) if cv_scores["auc_roc"] else np.nan,
        "avg_precision_cv_media": np.mean(cv_scores["average_precision"]) if cv_scores["average_precision"] else np.nan,
        "avg_precision_cv_desvio": np.std(cv_scores["average_precision"]) if cv_scores["average_precision"] else np.nan,
        "recall_cv_media": np.mean(cv_scores["recall"]) if cv_scores["recall"] else np.nan,
        "precision_cv_media": np.mean(cv_scores["precision"]) if cv_scores["precision"] else np.nan,
        "f1_cv_media": np.mean(cv_scores["f1"]) if cv_scores["f1"] else np.nan,
        "pred_key": pred_key,
        "observacao": observacao,
    }


def run_cv(
    name: str,
    x: pd.DataFrame,
    y: pd.Series,
    pipeline_factory: Callable[[], Pipeline],
    use_sample_weight: bool = False,
) -> dict[str, list[float]]:
    cv = StratifiedKFold(n_splits=CV_SPLITS, shuffle=True, random_state=RANDOM_STATE)
    scores: dict[str, list[float]] = {
        "auc_roc": [],
        "average_precision": [],
        "recall": [],
        "precision": [],
        "f1": [],
    }

    for fold, (train_idx, test_idx) in enumerate(cv.split(x, y), start=1):
        print(f"  CV {fold}/{CV_SPLITS}: {name}", flush=True)
        model = clone(pipeline_factory())
        x_train = x.iloc[train_idx]
        y_train = y.iloc[train_idx]
        if use_sample_weight:
            model = fit_mlp(model, x_train, y_train)
        else:
            model.fit(x_train, y_train)

        y_fold = y.iloc[test_idx]
        y_pred = model.predict(x.iloc[test_idx])
        y_score = model.predict_proba(x.iloc[test_idx])[:, 1]
        scores["auc_roc"].append(roc_auc_score(y_fold, y_score))
        scores["average_precision"].append(average_precision_score(y_fold, y_score))
        scores["recall"].append(recall_score(y_fold, y_pred, zero_division=0))
        scores["precision"].append(precision_score(y_fold, y_pred, zero_division=0))
        scores["f1"].append(f1_score(y_fold, y_pred, zero_division=0))
        del model, y_pred, y_score
        gc.collect()

    return scores


def evaluate_model(
    name: str,
    familia: str,
    x: pd.DataFrame,
    y: pd.Series,
    pred_key: str,
    observacao: str,
    pipeline_factory: Callable[[], Pipeline],
    use_sample_weight: bool = False,
) -> tuple[dict, dict]:
    print(f"\nTreinando {name}", flush=True)
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=TEST_SIZE,
        stratify=y,
        random_state=RANDOM_STATE,
    )

    model = clone(pipeline_factory())
    if use_sample_weight:
        model = fit_mlp(model, x_train, y_train)
    else:
        model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    y_score = model.predict_proba(x_test)[:, 1]

    pd.DataFrame(
        {
            "y_test": np.asarray(y_test),
            "y_score": y_score,
            "y_pred": y_pred,
        }
    ).to_csv(PRED_DIR / f"{pred_key}.csv", index=False)

    cv_scores = run_cv(name, x, y, pipeline_factory, use_sample_weight=use_sample_weight)
    row = metric_row(
        name,
        familia,
        x,
        y,
        y_test,
        y_pred,
        y_score,
        cv_scores,
        pred_key,
        observacao,
    )
    artifacts = {
        "model": model,
        "y_test": np.asarray(y_test),
        "y_score": y_score,
        "y_pred": y_pred,
    }
    return row, artifacts


def evaluate_calibrated_tuned(
    name: str,
    familia: str,
    x: pd.DataFrame,
    y: pd.Series,
    pred_key: str,
    observacao: str,
    pipeline_factory: Callable[[], Pipeline],
    use_sample_weight: bool = False,
) -> tuple[list[dict], dict]:
    print(f"\nAjustando {name} (calibracao + limiar)", flush=True)
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=TEST_SIZE,
        stratify=y,
        random_state=RANDOM_STATE,
    )
    x_fit, x_val, y_fit, y_val = train_test_split(
        x_train,
        y_train,
        test_size=VAL_SIZE,
        stratify=y_train,
        random_state=RANDOM_STATE,
    )

    base_model = clone(pipeline_factory())
    if use_sample_weight:
        base_model = fit_mlp(base_model, x_fit, y_fit)
    else:
        base_model.fit(x_fit, y_fit)

    calibrated = CalibratedClassifierCV(FrozenEstimator(base_model), method="sigmoid")
    calibrated.fit(x_val, y_val)

    val_score = calibrated.predict_proba(x_val)[:, 1]
    threshold, val_precision, val_recall = find_threshold(np.asarray(y_val), val_score)

    test_score = calibrated.predict_proba(x_test)[:, 1]
    y_pred_default = (test_score >= 0.5).astype(int)
    y_pred_tuned = (test_score >= threshold).astype(int)

    pd.DataFrame(
        {
            "y_test": np.asarray(y_test),
            "y_score": test_score,
            "y_pred_default": y_pred_default,
            "y_pred_tuned": y_pred_tuned,
            "threshold": threshold,
        }
    ).to_csv(PRED_DIR / f"{pred_key}_tuned.csv", index=False)

    rows = []
    for suffix, thr, pred_key_suffix, note in [
        ("limiar 0.5", 0.5, "default", "Probabilidades calibradas, limiar padrao."),
        (
            f"limiar {threshold:.3f}",
            threshold,
            "tuned",
            f"Calibrado + limiar otimizado (recall val >= {MIN_RECALL_THRESHOLD:.0%} ou max F1).",
        ),
    ]:
        y_pred = (test_score >= thr).astype(int)
        row = metric_row(
            f"{name} [{suffix}]",
            familia,
            x,
            y,
            y_test,
            y_pred,
            test_score,
            cv_scores={"auc_roc": [], "average_precision": [], "recall": [], "precision": [], "f1": []},
            pred_key=f"{pred_key}_{pred_key_suffix}",
            observacao=f"{observacao} {note}",
            threshold=thr,
            calibrado=True,
        )
        rows.append(row)

    artifacts = {
        "model": calibrated,
        "y_test": np.asarray(y_test),
        "y_score": test_score,
        "y_pred": y_pred_tuned,
        "threshold": threshold,
        "val_precision": val_precision,
        "val_recall": val_recall,
    }
    print(
        f"  limiar escolhido={threshold:.4f} | val precision={val_precision:.4f} "
        f"| val recall={val_recall:.4f}",
        flush=True,
    )
    return rows, artifacts


def load_rf_metrics() -> pd.DataFrame:
    rf_full = pd.read_csv(OUTPUT_DIR / "semana_5_metricas_completa.csv")
    rf_dbscan = pd.read_csv(OUTPUT_DIR / "semana_5_metricas_dbscan_only.csv")
    rf = pd.concat([rf_full, rf_dbscan], ignore_index=True)
    rf["familia"] = "Random Forest"
    rf["threshold"] = 0.5
    rf["calibrado"] = False
    rf["observacao"] = [
        "RF baseline da Semana 5 (referencia principal).",
        "RF com K-Means + DBSCAN da Semana 5.",
        "RF apenas com ruido DBSCAN da Semana 5.",
    ]
    return rf


def rf_reference_row(rf: pd.DataFrame) -> pd.Series:
    return rf.sort_values(["avg_precision_cv_media", "f1_cv_media"], ascending=False).iloc[0]


def beats_rf_reference(row: pd.Series, rf_ref: pd.Series) -> bool:
    ap_ok = row["avg_precision_cv_media"] > rf_ref["avg_precision_cv_media"]
    f1_ok = row["f1_cv_media"] > rf_ref["f1_cv_media"]
    if pd.isna(row["avg_precision_cv_media"]) or pd.isna(row["f1_cv_media"]):
        ap_test = row["average_precision_teste"] > rf_ref["average_precision_teste"]
        f1_test = row["f1_teste"] > rf_ref["f1_teste"]
        return bool(ap_test and f1_test)
    return bool(ap_ok and f1_ok)


def comparison_table(metrics: pd.DataFrame) -> pd.DataFrame:
    rf = load_rf_metrics()
    cols = [
        "familia",
        "modelo",
        "n_features",
        "threshold",
        "calibrado",
        "auc_roc_teste",
        "average_precision_teste",
        "recall_teste",
        "precision_teste",
        "f1_teste",
        "auc_roc_cv_media",
        "avg_precision_cv_media",
        "f1_cv_media",
        "observacao",
    ]
    return pd.concat([rf[cols], metrics[cols]], ignore_index=True)


def save_confusion_matrix(artifacts: dict[str, dict], filename: str, title: str) -> None:
    n = len(artifacts)
    fig, axes = plt.subplots(1, n, figsize=(4.5 * n, 4.2))
    if n == 1:
        axes = [axes]
    for ax, (name, data) in zip(axes, artifacts.items()):
        cm = confusion_matrix(data["y_test"], data["y_pred"], labels=[0, 1])
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            cbar=False,
            ax=ax,
            xticklabels=["Legitima", "Fraude"],
            yticklabels=["Legitima", "Fraude"],
        )
        ax.set_title(name[:42], fontsize=9)
        ax.set_xlabel("Predito")
        ax.set_ylabel("Real")
    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(FIG_DIR / filename, dpi=120)
    plt.close(fig)


def save_pr_curve(artifacts: dict[str, dict], filename: str, title: str) -> None:
    fig, ax = plt.subplots(figsize=(7.5, 5))
    for name, data in artifacts.items():
        precision, recall, _ = precision_recall_curve(data["y_test"], data["y_score"])
        ap = average_precision_score(data["y_test"], data["y_score"])
        ax.plot(recall, precision, label=f"{name[:36]} (AP={ap:.3f})")
    ax.set_title(title)
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.legend(loc="lower left", fontsize=7)
    fig.tight_layout()
    fig.savefig(FIG_DIR / filename, dpi=120)
    plt.close(fig)


def save_model_bars(comparison: pd.DataFrame, filename: str, title: str) -> None:
    metric_map = {
        "auc_roc_teste": "AUC-ROC",
        "average_precision_teste": "Avg Precision",
        "recall_teste": "Recall",
        "precision_teste": "Precision",
        "f1_teste": "F1",
    }
    plot_df = comparison.set_index("modelo")[list(metric_map)].rename(columns=metric_map)
    ax = plot_df.T.plot(kind="bar", figsize=(13, 5.5), width=0.82)
    ax.set_title(title)
    ax.set_ylabel("Valor")
    ax.set_ylim(0, 1.05)
    ax.legend(loc="lower right", fontsize=6)
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(FIG_DIR / filename, dpi=120)
    plt.close()


def save_figures(
    mlp_artifacts: dict[str, dict],
    tuned_artifacts: dict[str, dict],
    comparison_initial: pd.DataFrame,
    comparison_tuned: pd.DataFrame,
) -> None:
    sns.set_theme(style="whitegrid")
    save_confusion_matrix(
        mlp_artifacts,
        "semana_6_matriz_confusao.png",
        "Semana 6 - Matriz de confusao dos MLPs (limiar 0.5)",
    )
    save_pr_curve(
        mlp_artifacts,
        "semana_6_pr_curve.png",
        "Semana 6 - Curva Precision-Recall dos MLPs (limiar 0.5)",
    )
    save_model_bars(
        comparison_initial,
        "semana_6_comparacao_rf_vs_mlp.png",
        "Semana 6 - RF vs MLP/LR no teste (configuracao inicial)",
    )
    save_confusion_matrix(
        tuned_artifacts,
        "semana_6_matriz_confusao_ajustada.png",
        "Semana 6 - Matriz de confusao (calibrado + limiar ajustado)",
    )
    save_pr_curve(
        tuned_artifacts,
        "semana_6_pr_curve_ajustada.png",
        "Semana 6 - Curvas PR calibradas com limiar ajustado",
    )
    save_model_bars(
        comparison_tuned,
        "semana_6_comparacao_modelos_ajustada.png",
        "Semana 6 - Comparacao no teste apos calibracao e limiar",
    )


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    PRED_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    dataset = load_dataset()
    y = dataset["Class"].astype(int)
    matrices = build_feature_matrices(dataset)
    x_baseline = matrices["baseline"]

    print("Dataset Semana 6", flush=True)
    print(f"- Registros: {len(dataset)}", flush=True)
    print(f"- Fraudes: {int(y.sum())}", flush=True)
    print(f"- Taxa de fraude: {y.mean():.4%}", flush=True)
    print(f"- Recall minimo alvo no limiar: {MIN_RECALL_THRESHOLD:.0%}", flush=True)

    initial_results: list[dict] = []
    mlp_artifacts: dict[str, dict] = {}
    initial_path = OUTPUT_DIR / "semana_6_metricas_mlp.csv"

    if initial_path.exists():
        print("\nCarregando metricas iniciais existentes (pulando retreino MLP/LR).", flush=True)
        initial_metrics = pd.read_csv(initial_path)
        for _, row in initial_metrics.iterrows():
            pred_path = PRED_DIR / f"{row['pred_key']}.csv"
            if pred_path.exists():
                pred = pd.read_csv(pred_path)
                y_pred = pred["y_pred"].to_numpy() if "y_pred" in pred.columns else pred["y_pred_tuned"].to_numpy()
                mlp_artifacts[row["modelo"]] = {
                    "y_test": pred["y_test"].to_numpy(),
                    "y_score": pred["y_score"].to_numpy(),
                    "y_pred": y_pred,
                }
    else:
        for name, spec in MLP_MODELS.items():
            row, artifact = evaluate_model(
                name,
                "MLP",
                matrices[spec["features"]],
                y,
                pred_key=spec["pred_key"],
                observacao=spec["observacao"],
                pipeline_factory=make_mlp_pipeline,
                use_sample_weight=True,
            )
            initial_results.append(row)
            mlp_artifacts[name] = artifact

        lr_row, _ = evaluate_model(
            "Regressao Logistica balanceada - base completa",
            "Regressao Logistica",
            x_baseline,
            y,
            pred_key="lr_baseline",
            observacao="Baseline linear escalonado com class_weight='balanced'.",
            pipeline_factory=make_lr_pipeline,
            use_sample_weight=False,
        )
        initial_results.append(lr_row)
        initial_metrics = pd.DataFrame(initial_results)
        initial_metrics.to_csv(initial_path, index=False)

    tuned_results: list[dict] = []
    tuned_artifacts: dict[str, dict] = {}

    lr_tuned_rows, lr_tuned_art = evaluate_calibrated_tuned(
        "Regressao Logistica balanceada",
        "Regressao Logistica",
        x_baseline,
        y,
        pred_key="lr_baseline",
        observacao="Baseline linear escalonado.",
        pipeline_factory=make_lr_pipeline,
        use_sample_weight=False,
    )
    tuned_results.extend([r for r in lr_tuned_rows if r["threshold"] != 0.5])
    tuned_artifacts["LR calibrada"] = lr_tuned_art

    for config_name, cfg in MLP_CONFIGS.items():
        factory = lambda cfg=cfg: make_mlp_pipeline(cfg["hidden_layer_sizes"], cfg["alpha"])
        rows, artifact = evaluate_calibrated_tuned(
            config_name,
            "MLP ajustado",
            x_baseline,
            y,
            pred_key=config_name.lower().replace(" ", "_").replace(",", "").replace("=", ""),
            observacao=f"Arquitetura {cfg['hidden_layer_sizes']}, alpha={cfg['alpha']}.",
            pipeline_factory=factory,
            use_sample_weight=True,
        )
        tuned_only = [r for r in rows if r["threshold"] != 0.5]
        tuned_results.extend(tuned_only)
        tuned_artifacts[config_name] = artifact

    tuned_metrics = pd.DataFrame(tuned_results)
    tuned_metrics.to_csv(OUTPUT_DIR / "semana_6_metricas_ajustadas.csv", index=False)

    comparison_initial = comparison_table(initial_metrics)
    comparison_initial.to_csv(OUTPUT_DIR / "semana_6_comparacao_rf_vs_mlp.csv", index=False)

    comparison_tuned = comparison_table(tuned_metrics)
    comparison_tuned.to_csv(OUTPUT_DIR / "semana_6_comparacao_modelos_ajustada.csv", index=False)

    rf_ref = rf_reference_row(load_rf_metrics())
    summary = pd.DataFrame(
        [
            {
                "referencia_rf": rf_ref["modelo"],
                "rf_ap_cv": rf_ref["avg_precision_cv_media"],
                "rf_f1_cv": rf_ref["f1_cv_media"],
                "rf_ap_teste": rf_ref["average_precision_teste"],
                "rf_f1_teste": rf_ref["f1_teste"],
                "melhor_desafiante_ap_teste": tuned_metrics.sort_values(
                    "average_precision_teste", ascending=False
                ).iloc[0]["modelo"],
                "melhor_desafiante_f1_teste": tuned_metrics.sort_values(
                    "f1_teste", ascending=False
                ).iloc[0]["modelo"],
                "algum_supera_rf_consistente": any(
                    beats_rf_reference(row, rf_ref) for _, row in initial_metrics.iterrows()
                )
                or any(beats_rf_reference(row, rf_ref) for _, row in tuned_metrics.iterrows()),
            }
        ]
    )
    summary.to_csv(OUTPUT_DIR / "semana_6_resumo_referencia_rf.csv", index=False)

    gc.collect()
    save_figures(mlp_artifacts, tuned_artifacts, comparison_initial, comparison_tuned)

    display_cols = [
        "modelo",
        "threshold",
        "calibrado",
        "auc_roc_teste",
        "average_precision_teste",
        "recall_teste",
        "precision_teste",
        "f1_teste",
        "avg_precision_cv_media",
        "f1_cv_media",
    ]
    print()
    print("Metricas iniciais (limiar 0.5)")
    print(initial_metrics[display_cols].to_string(index=False))
    print()
    print("Metricas ajustadas (calibracao + limiar)")
    print(tuned_metrics[display_cols].to_string(index=False))
    print()
    print("Referencia RF principal")
    print(
        f"- {rf_ref['modelo']}: AP(CV)={rf_ref['avg_precision_cv_media']:.4f}, "
        f"F1(CV)={rf_ref['f1_cv_media']:.4f}, AP(teste)={rf_ref['average_precision_teste']:.4f}, "
        f"F1(teste)={rf_ref['f1_teste']:.4f}"
    )
    print(
        f"- Algum modelo supera RF de forma consistente (AP e F1)? "
        f"{'SIM' if summary.iloc[0]['algum_supera_rf_consistente'] else 'NAO'}"
    )
    print()
    print(f"Metricas iniciais: {OUTPUT_DIR / 'semana_6_metricas_mlp.csv'}")
    print(f"Metricas ajustadas: {OUTPUT_DIR / 'semana_6_metricas_ajustadas.csv'}")
    print(f"Comparacao ajustada: {OUTPUT_DIR / 'semana_6_comparacao_modelos_ajustada.csv'}")
    print(f"Resumo RF: {OUTPUT_DIR / 'semana_6_resumo_referencia_rf.csv'}")


if __name__ == "__main__":
    main()
