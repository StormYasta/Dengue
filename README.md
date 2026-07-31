# Monitor das Notificações de Dengue — Campinas/SP

Painel interativo para exploração descritiva das notificações de dengue registradas em Campinas/SP até a data mais recente disponível na base processada.

O projeto organiza a série histórica, compara períodos, apresenta a sazonalidade mensal, mostra a participação das redes pública e privada e localiza os estabelecimentos de saúde associados às notificações.

> Este painel tem finalidade acadêmica e de estudo. Ele não realiza diagnóstico, não apresenta dados em tempo real e não deve ser interpretado como um mapa dos locais de transmissão.

---

## Visão geral

O monitor foi desenvolvido para responder a três perguntas principais:

1. Como as notificações se distribuem ao longo dos meses e dos anos?
2. Quais estabelecimentos de saúde aparecem associados a maiores volumes de registros?
3. Como transformar uma base pública extensa em uma visualização clara, verificável e atualizável?

A página oferece:

- mapa interativo por estabelecimento de saúde;
- filtro por ano;
- filtro por rede pública/SUS ou privada;
- total de notificações no período selecionado;
- quantidade de notificações por rede;
- quantidade de estabelecimentos associados aos registros;
- gráfico mensal de sazonalidade;
- total anual e variação percentual;
- média e mediana mensal;
- composição entre rede pública e privada;
- informação sobre a primeira e a última data da base processada.

---

## Origem e inspiração

Este estudo surgiu a partir do contato com um projeto de monitoramento das notificações de dengue desenvolvido para São José do Rio Preto/SP.

A experiência motivou o aprofundamento em todo o fluxo de trabalho envolvido na análise de dados epidemiológicos: obtenção das bases públicas, tratamento, integração cadastral, agregação e construção de visualizações interativas.

A versão de Campinas foi desenvolvida de forma independente, com um novo recorte municipal e finalidade exclusivamente acadêmica e de estudo.

Projeto inspirador:

- [Mas-Rodrigues — Monitor da Dengue](https://github.com/Mas-Rodrigues/Monitor-da-Dengue)

Notebook utilizado:

- https://colab.research.google.com/drive/1yOblVeZjGJ2cLUxDrQKBd9vRJWx2JwAv?usp=sharing

---

## Tecnologias utilizadas

### Preparação dos dados

- Python
- Google Colab
- pandas
- PySUS
- arquivos CSV e JSON

### Interface e visualização

- HTML
- CSS
- JavaScript
- Leaflet
- Chart.js
- OpenStreetMap
- CARTO

O Papa Parse foi utilizado durante a etapa anterior do projeto, quando o navegador fazia a leitura direta do CSV. A versão atual utiliza um arquivo JSON agregado e leitura nativa com `fetch`.

---

## Estrutura recomendada do projeto

```text
monitor-dengue-campinas/
├── index.html
├── dados_dengue_campinas.json
├── gerar_json_agregado.py
├── README.md
└── dados-originais/
    └── casos_dengue_campinas.csv
```

### Arquivos publicados

Para executar o painel, somente estes arquivos precisam estar disponíveis no servidor:

```text
index.html
dados_dengue_campinas.json
```

O CSV completo não precisa ser publicado.

---

## Como executar localmente

O painel carrega o JSON por meio de `fetch`. Por isso, não é recomendado abrir o HTML diretamente com `file://`.

Na pasta do projeto, inicie um servidor local:

```bash
python -m http.server 5500
```

Depois, abra no navegador:

```text
http://localhost:5500
```

Também é possível utilizar extensões como **Live Server** no Visual Studio Code.

---

## Base de dados

O arquivo original contém uma linha por notificação.

As colunas utilizadas na preparação são:

```text
ID_UNIDADE
DT_NOTIFIC
NOME_UNIDADE
TIPO_REDE
LATITUDE
LONGITUDE
```

### Significado dos campos

| Campo | Descrição |
|---|---|
| `ID_UNIDADE` | Identificador ou código CNES do estabelecimento |
| `DT_NOTIFIC` | Data da notificação |
| `NOME_UNIDADE` | Nome do estabelecimento associado ao registro |
| `TIPO_REDE` | Classificação da rede pública/SUS ou privada |
| `LATITUDE` | Latitude do estabelecimento |
| `LONGITUDE` | Longitude do estabelecimento |

### Classificação da rede

Durante a preparação, a rede é normalizada para:

```text
S = SUS / rede pública
N = rede privada
```

Registros sem classificação permanecem com valor vazio e não entram no cálculo percentual entre as duas redes.

---

## Otimização dos dados

A base original possuía aproximadamente:

```text
698.175 notificações
128 MB em CSV
```

Depois da agregação:

```text
10.344 registros agregados
aproximadamente 1,6 MB em JSON
```

A agregação é feita por:

- ano;
- mês;
- estabelecimento;
- nome da unidade;
- rede de atendimento;
- latitude;
- longitude.

Cada objeto do JSON possui uma coluna `notificacoes`, que representa quantos registros originais foram agrupados naquela combinação.

Exemplo:

```json
{
  "ano": "2024",
  "mes": "03",
  "unidadeId": "1234567",
  "unidadeNome": "UNIDADE DE SAÚDE EXEMPLO",
  "sus": "S",
  "lat": -22.905,
  "lng": -47.061,
  "notificacoes": 157
}
```

---

## Estrutura do JSON

O arquivo `dados_dengue_campinas.json` possui duas seções:

```json
{
  "meta": {
    "municipio": "Campinas",
    "uf": "SP",
    "primeiraData": "2015-01-04",
    "ultimaData": "2026-05-09",
    "totalNotificacoes": 698175,
    "registrosAgregados": 10344,
    "geradoEm": "2026-07-29"
  },
  "dados": []
}
```

### Metadados

Os metadados permitem que o site apresente automaticamente:

- município;
- período coberto;
- total da base;
- quantidade de registros agregados;
- data de geração do arquivo.

---

## Atualização da base

Para atualizar o painel com uma nova versão do CSV:

1. Substitua o arquivo original por uma versão mais recente.
2. Mantenha o nome:

```text
casos_dengue_campinas.csv
```

3. Execute:

```bash
python gerar_json_agregado.py
```

4. O script gerará novamente:

```text
dados_dengue_campinas.json
```

5. Substitua o JSON antigo no servidor.
6. Recarregue a página.

O HTML não precisa ser alterado a cada atualização.

---

## Comportamento inicial

Ao abrir a página:

- somente o ano mais recente disponível fica selecionado;
- o mapa é centralizado em Campinas;
- os indicadores são recalculados a partir do filtro ativo;
- o período exibido é obtido diretamente dos metadados do JSON;
- os anos anteriores permanecem disponíveis para comparação.

---

## Interpretação do mapa

Cada círculo representa um estabelecimento de saúde associado às notificações.

O tamanho do círculo é proporcional ao número de registros vinculados ao estabelecimento durante o período selecionado.

O mapa permite consultar:

- nome do estabelecimento;
- rede de atendimento;
- total de notificações;
- distribuição mensal dos registros.

### Atenção

O ponto exibido no mapa não representa necessariamente:

- endereço de residência da pessoa notificada;
- bairro onde ocorreu a transmissão;
- local provável de infecção;
- local onde aconteceu o contato com o vetor.

O mapa mostra a localização do estabelecimento associado ao registro.

Por esse motivo, o painel utiliza o título:

> Notificações por estabelecimento de saúde

e não “incidência por bairro”.

---

## Sazonalidade

O gráfico mensal permite comparar o comportamento das notificações entre diferentes anos.

Ele pode ajudar a observar:

- início de períodos de crescimento;
- meses com maior concentração;
- redução do volume registrado;
- diferenças entre anos;
- períodos fora do comportamento mais comum.

A soma anual isolada pode esconder diferenças importantes na distribuição mensal. Por isso, o painel apresenta tanto os totais anuais quanto a curva de cada ano.

---

## Média e mediana

O painel também compara média e mediana mensal.

A média considera todos os anos selecionados e pode ser influenciada por períodos com números excepcionalmente altos.

A mediana representa o valor central e tende a ser menos sensível a anos epidêmicos muito intensos.

Uma diferença elevada entre as duas medidas pode indicar que alguns anos tiveram comportamento muito acima do restante da série.

---

## Limitações

As principais limitações são:

- notificações não equivalem necessariamente a casos confirmados;
- pode existir subnotificação;
- registros podem ser corrigidos posteriormente;
- datas ausentes ou inválidas podem afetar alguns totais;
- estabelecimentos podem ter cadastros duplicados ou coordenadas imprecisas;
- o local de atendimento não representa automaticamente o local de transmissão;
- diferenças nos processos de notificação podem afetar comparações;
- os dados refletem a última versão processada, não um fluxo em tempo real.

Essas limitações definem o que o painel pode e o que ele não pode responder.

---

## Fontes e referências

1. **BRASIL. Ministério da Saúde.** Notificações de casos suspeitos de dengue.  
   https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/d/dengue/casos-suspeitos/not-de-casos-suspeitos

2. **BRASIL. Ministério da Saúde.** Sistema de Informação de Agravos de Notificação — SINAN.  
   https://www.gov.br/saude/pt-br/composicao/svsa/sistemas-de-informacao/sinan

3. **BRASIL. Ministério da Saúde.** Cadastro Nacional de Estabelecimentos de Saúde — CNES.  
   https://www.gov.br/saude/pt-br/composicao/sectics/daf/ceaf/faq/o-que-e-o-cnes

4. **COELHO, Flávio Codeço; VACARO, Luã et al.** PySUS.  
   https://github.com/AlertaDengue/PySUS

5. **THE PANDAS DEVELOPMENT TEAM.** pandas-dev/pandas: Pandas. Zenodo.  
   DOI: 10.5281/zenodo.3509134  
   https://pandas.pydata.org/about/citing.html

6. **GOOGLE.** Google Colaboratory: perguntas frequentes.  
   https://research.google.com/colaboratory/faq.html?hl=pt-BR

7. **MAS-RODRIGUES.** Monitor da Dengue. GitHub.  
   https://github.com/Mas-Rodrigues/Monitor-da-Dengue

---

## Créditos técnicos

- [Leaflet](https://leafletjs.com/reference.html)
- [Chart.js](https://www.chartjs.org/docs/latest/)
- [Papa Parse](https://www.papaparse.com/docs)
- [OpenStreetMap](https://www.openstreetmap.org/copyright)
- [CARTO](https://carto.com/attributions)

As atribuições do mapa-base também são mantidas dentro do próprio mapa.

---

## Reprodutibilidade

As versões exatas das bibliotecas utilizadas devem permanecer registradas no notebook do Google Colab.

Exemplo:

```python
from importlib.metadata import version

print("PySUS:", version("pysus"))
print("pandas:", version("pandas"))
```

Também é recomendado registrar:

- data da coleta;
- intervalo temporal disponível;
- filtros aplicados;
- quantidade de registros antes e depois da limpeza;
- quantidade de unidades localizadas;
- quantidade de registros sem correspondência cadastral;
- data de geração do JSON agregado.

---

## Aviso de uso

Este repositório apresenta um estudo independente desenvolvido com dados públicos do Sistema Único de Saúde.

As informações disponibilizadas possuem finalidade educacional, acadêmica e exploratória. O painel não substitui sistemas oficiais de vigilância, análises epidemiológicas institucionais ou orientações das autoridades de saúde.
