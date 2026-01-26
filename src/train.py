from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

def train_random_forest(X, y):
    model = RandomForestClassifier(
        n_estimators=150,
        n_jobs=-1,
        class_weight='balanced',
        random_state=42
    )
    model.fit(X, y)
    return model

def train_xgboost(X, y):
    model = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric='logloss',
        tree_method='hist',
        random_state=42
    )
    model.fit(X, y)
    return model
