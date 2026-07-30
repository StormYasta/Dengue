from pathlib import Path
import pandas as pd
import json
from datetime import datetime

ARQUIVO_ENTRADA = Path("casos_dengue_campinas.csv")
ARQUIVO_SAIDA = Path("dados_dengue_campinas.json")

COLUNAS = [
    "ID_UNIDADE",
    "DT_NOTIFIC",
    "NOME_UNIDADE",
    "TIPO_REDE",
    "LATITUDE",
    "LONGITUDE",
]

df = pd.read_csv(
    ARQUIVO_ENTRADA,
    usecols=COLUNAS,
    low_memory=False,
)

datas_texto = (
    df["DT_NOTIFIC"]
    .astype(str)
    .str.replace(r"\D", "", regex=True)
)

datas = pd.to_datetime(
    datas_texto,
    format="%Y%m%d",
    errors="coerce",
)

if datas.isna().any():
    raise ValueError(
        f"{datas.isna().sum()} datas inválidas foram encontradas."
    )

tipo_rede = (
    df["TIPO_REDE"]
    .fillna("")
    .astype(str)
    .str.strip()
    .replace({
        "SUS / Pública": "S",
        "Privada": "N",
    })
)

base = pd.DataFrame({
    "ano": datas.dt.year.astype(str),
    "mes": datas.dt.month.astype(str).str.zfill(2),
    "unidadeId": (
        pd.to_numeric(df["ID_UNIDADE"], errors="coerce")
        .astype("Int64")
        .astype(str)
        .replace("<NA>", "")
    ),
    "unidadeNome": (
        df["NOME_UNIDADE"]
        .fillna("")
        .astype(str)
        .str.strip()
    ),
    "sus": tipo_rede,
    "lat": pd.to_numeric(
        df["LATITUDE"],
        errors="coerce",
    ),
    "lng": pd.to_numeric(
        df["LONGITUDE"],
        errors="coerce",
    ),
})

agrupado = (
    base.groupby(
        [
            "ano",
            "mes",
            "unidadeId",
            "unidadeNome",
            "sus",
            "lat",
            "lng",
        ],
        dropna=False,
        as_index=False,
    )
    .size()
    .rename(columns={"size": "notificacoes"})
)

agrupado = agrupado.astype(object).where(
    pd.notna(agrupado),
    None,
)

registros = agrupado.to_dict(orient="records")

payload = {
    "meta": {
        "municipio": "Campinas",
        "uf": "SP",
        "primeiraData": datas.min().strftime("%Y-%m-%d"),
        "ultimaData": datas.max().strftime("%Y-%m-%d"),
        "totalNotificacoes": int(len(df)),
        "registrosAgregados": int(len(registros)),
        "geradoEm": datetime.now().strftime("%Y-%m-%d"),
    },
    "dados": registros,
}

ARQUIVO_SAIDA.write_text(
    json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
    ),
    encoding="utf-8",
)

print(
    f"{len(df):,} notificações foram reduzidas para "
    f"{len(registros):,} registros agregados."
)
print(f"Arquivo criado: {ARQUIVO_SAIDA}")
