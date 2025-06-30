# your_app/import_prices.py
import os
import pandas as pd
from project.settings import BASE_DIR
from .models import LadderPrice, TrayPrice

def import_prices():
    ladder_path = os.path.join(BASE_DIR, 'static', 'calculated_prices.xlsx')
    tray_path = os.path.join(BASE_DIR, 'static', 'tray_dataa.xlsx')

    # ⬇️ استيراد بيانات السلالم (Ladder)
    print("📥 Importing Ladder Prices...")
    try:
        df_ladder = pd.read_excel(ladder_path)
        df_ladder.columns = df_ladder.columns.str.strip().str.lower()
        df_ladder = df_ladder[df_ladder['type'].astype(str).str.contains(r"\*", na=False)]

        for _, row in df_ladder.iterrows():
            LadderPrice.objects.create(
                type=row['type'],
                thickness=row['thickness'],
                side=row['side'],
                dim=row['dim'],
                price_final=row['price_final']
            )
        print(f"✅ Ladder prices imported: {len(df_ladder)} rows")
    except Exception as e:
        print("❌ Error importing ladder prices:", e)

    # ⬇️ استيراد بيانات التراي (Tray)
    print("📥 Importing Tray Prices...")
    try:
        df_tray = pd.read_excel(tray_path)
        df_tray.columns = df_tray.columns.str.strip().str.lower()

        for _, row in df_tray.iterrows():
            TrayPrice.objects.create(
                type=str(row['type']).strip(),
                thickness=float(row['thickness']),
                dim=float(row['dim']),
                price_with_joints=row['price_with_joints']
            )
        print(f"✅ Tray prices imported: {len(df_tray)} rows")
    except Exception as e:
        print("❌ Error importing tray prices:", e)
