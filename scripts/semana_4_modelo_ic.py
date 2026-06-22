from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "dados"
OUTPUT_DIR = ROOT / "resultados"

RANDOM_STATE = 42
TEST_SIZE = 0.20

BASE_FEATURES = ["Time", "Amount"] + [f"V{i}" for i in range(1, 29)]
CLUSTER_FEATURES = ["cluster_kmeans_semana3", "dbscan_ruido"]


def load_week4_dataset() -> pd.DataFrame:
    transactions = pd.read_csv(DATA_DIR / "creditcard.csv")
    clusters = pd.read_csv(DATA_DIR / "saida_clusters_semana3.csv")

    transactions = transactions.reset_index().rename(columns={"index": "original_index"})
    selected_columns = ["original_index", *BASE_FEATURES, "Class"]
    dataset = clusters.merge(
        transactions[selected_columns],
        on="original_index",
        how="inner",
        suffixes=("_cluster", ""),
        validate="one_to_one",
    )

    if "Class_cluster" in dataset.columns:
        mismatches = (dataset["Class_cluster"] != dataset["Class"]).sum()
        if mismatches:
            raise ValueError(f"Class mismatch between source files: {mismatches}")
        dataset = dataset.drop(columns=["Class_cluster"])

    return dataset


def make_model() -> RandomForestClassifier:
    return RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )


def evaluate_model(name: str, x: pd.DataFrame, y: pd.Series) -> dict:
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=TEST_SIZE,
        stratify=y,
        random_state=RANDOM_STATE,
    )

    model = make_model()
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    y_score = model.predict_proba(x_test)[:, 1]
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred, labels=[0, 1]).ravel()

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    cv_scores = cross_validate(
        make_model(),
        x,
        y,
        cv=cv,
        scoring={
            "roc_auc": "roc_auc",
            "average_precision": "average_precision",
            "recall": "recall",
            "precision": "precision",
            "f1": "f1",
        },
        n_jobs=-1,
        error_score="raise",
    )

    return {
        "modelo": name,
        "n_features": x.shape[1],
        "n_registros": x.shape[0],
        "fraudes": int(y.sum()),
        "auc_roc_teste": roc_auc_score(y_test, y_score),
        "average_precision_teste": average_precision_score(y_test, y_score),
        "recall_teste": recall_score(y_test, y_pred, zero_division=0),
        "precision_teste": precision_score(y_test, y_pred, zero_division=0),
        "f1_teste": f1_score(y_test, y_pred, zero_division=0),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
        "auc_roc_cv_media": cv_scores["test_roc_auc"].mean(),
        "auc_roc_cv_desvio": cv_scores["test_roc_auc"].std(),
        "avg_precision_cv_media": cv_scores["test_average_precision"].mean(),
        "avg_precision_cv_desvio": cv_scores["test_average_precision"].std(),
        "recall_cv_media": cv_scores["test_recall"].mean(),
        "precision_cv_media": cv_scores["test_precision"].mean(),
        "f1_cv_media": cv_scores["test_f1"].mean(),
    }


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    dataset = load_week4_dataset()
    y = dataset["Class"].astype(int)

    x_without_clusters = dataset[BASE_FEATURES]
    x_with_clusters = pd.get_dummies(
        dataset[BASE_FEATURES + CLUSTER_FEATURES].astype(
            {"cluster_kmeans_semana3": "category", "dbscan_ruido": "category"}
        ),
        columns=CLUSTER_FEATURES,
        drop_first=False,
        dtype=int,
    )

    results = [
        evaluate_model("Random Forest sem clusters", x_without_clusters, y),
        evaluate_model("Random Forest com clusters", x_with_clusters, y),
    ]

    metrics = pd.DataFrame(results)
    metrics.to_csv(OUTPUT_DIR / "semana_4_metricas_modelo_ic.csv", index=False)

    print("Dataset Semana 4")
    print(f"- Registros: {len(dataset)}")
    print(f"- Fraudes: {int(y.sum())}")
    print(f"- Taxa de fraude: {y.mean():.4%}")
    print()
    print(metrics.to_string(index=False))
    print()
    print(f"Metricas salvas em: {OUTPUT_DIR / 'semana_4_metricas_modelo_ic.csv'}")


if __name__ == "__main__":
    main()
