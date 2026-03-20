import os
import django
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "disease_outbreak.settings")
django.setup()

from outbreak.models import OutbreakReport

def export_data():
    data = OutbreakReport.objects.all().values()
    df = pd.DataFrame(data)
    df.to_csv("outbreak_data.csv", index=False)
    print("Exported outbreak_data.csv successfully!")

# Run it
if __name__ == "__main__":
    export_data()
