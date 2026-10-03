import numpy as np

def create_features(df):
    # TARGET (Answer Key): AI ko agle 1 ghante ki dhoop predict karni hai
    # shift(-1) ka matlab hai neeche wali row ka data upar khiska do
    df['target_1h'] = df['solar_kw'].shift(-1)
    
    # FEATURES (Clues): Time ko gol (circle) banane ke liye Sine aur Cosine lagaya
    df['hour_sin'] = np.sin(2 * np.pi * df['hour_of_day'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour_of_day'] / 24)
    
    # LAG FEATURE: Pichle ghante mein kitni dhoop thi?
    df['solar_lag_1h'] = df['solar_kw'].shift(1)
    
    # Jo rows shift ki wajah se khali (NaN) ho gayi, unhe hata do
    df = df.dropna()
    return df