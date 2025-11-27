import pandas as pd
from pathlib import Path

# Ruta donde quieres guardarlo
path = Path("data/taxonomy_skills.csv")
path.parent.mkdir(exist_ok=True)   # crea /data si no existe

# Contenido de la taxonomía
data = [
    ("Python", "programming"),
    ("SQL", "programming"),
    ("R", "programming"),
    ("Excel", "analytics"),
    ("Power BI", "analytics"),
    ("Tableau", "analytics"),
    ("Machine Learning", "ml"),
    ("Statistics", "ml"),
    ("Git", "tools"),
    ("AWS", "cloud"),
    ("Azure", "cloud"),
    ("Spark", "bigdata"),
    ("Hadoop", "bigdata"),
    ("Communication", "soft"),
    ("Teamwork", "soft"),
    ("Pandas", "programming"),
    ("Numpy", "programming")
]

df = pd.DataFrame(data, columns=["skill", "category"])

df.to_csv(path, index=False, encoding="utf-8")

print("taxonomy_skills.csv creado en:", path)
