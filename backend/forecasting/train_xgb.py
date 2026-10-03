import os
import pickle
import xgboost as xgb
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt

# Purani files se function bulayenge
from fetch_nasa import get_weather_data
from features import create_features

def train_and_evaluate():
    print("Generating 1 year of weather data...")
    df = get_weather_data(days=365)
    df = create_features(df)
    
    # Humare Clues aur humara Answer
    features = ['hour_sin', 'hour_cos', 'cloud_cover', 'solar_kw', 'solar_lag_1h']
    target = 'target_1h'
    
    # 1. TRAIN/TEST SPLIT: Shuru ka 80% padhai ke liye, aakhiri 20% test ke liye
    split_idx = int(len(df) * 0.8)
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]
    
    X_train, y_train = train_df[features], train_df[target]
    X_test, y_test = test_df[features], test_df[target]
    
    # 2. BEVKUF BACHA (Baseline): "Abhi jo dhoop hai, 1 ghante baad bhi wahi hogi"
    baseline_predictions = test_df['solar_kw']
    baseline_mae = mean_absolute_error(y_test, baseline_predictions)
    
    # 3. SMART AI (XGBoost): Isko Train karo
    print("Training XGBoost AI Model...")
    model = xgb.XGBRegressor(n_estimators=100, max_depth=3, learning_rate=0.1)
    model.fit(X_train, y_train)
    
    # 4. AI ka Test lo aur error check karo
    xgb_predictions = model.predict(X_test)
    xgb_mae = mean_absolute_error(y_test, xgb_predictions)
    
    print("\n=== FORECAST EVALUATION ===")
    print(f"Baseline (Dumb Model) Error : {baseline_mae:.2f} kW")
    print(f"XGBoost (Smart AI) Error    : {xgb_mae:.2f} kW")
    
    # 5. AI ka dimaag file mein save kar lo, taaki baar-baar train na karna pade
    model_path = os.path.join(os.path.dirname(__file__), "../data/xgboost_model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
        
    # 6. Result ka Graph (Sirf pehle 3 din ka zoom karke dikhayenge)
    plt.figure(figsize=(10, 5))
    plt.plot(y_test.values[:72], label='Asli (Actual) Future', color='green', linewidth=2)
    plt.plot(baseline_predictions.values[:72], label='Dumb Predict', color='red', linestyle=':')
    plt.plot(xgb_predictions[:72], label='AI Predict', color='blue', linestyle='--')
    plt.title("Solar Forecast: Asli Dhoop vs AI Prediction")
    plt.xlabel("Test Hours")
    plt.ylabel("Solar Power (kW)")
    plt.legend()
    plt.grid(True)
    
    save_path = os.path.join(os.path.dirname(__file__), "../data/forecast_graph.png")
    plt.savefig(save_path)
    print(f"\nGraph saved at: {save_path}")

if __name__ == "__main__":
    train_and_evaluate()