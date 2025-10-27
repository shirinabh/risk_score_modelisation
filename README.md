# risk_score_modelisation

Personal project to modelise a risk score from open data 

## publics open datasets

https://webstat.banque-france.fr/fr/themes/entreprises/defaillances-entreprises/

données affacturage
https://webstat.banque-france.fr/fr/catalogue/diren/


## python env creation
`sudo apt update && sudo apt upgrade -y`

`sudo apt install python3 python3-pip python3-venv -y`

`python3 -m venv risk`

`source risk/bin/activate`


## install and config big query 

`pip install google-cloud-bigquery google-cloud-bigquery-storage pyarrow pandas`

`gcloud auth application-default revoke -q || true`

`gcloud auth application-default login --no-launch-browser \`
  `--scopes=https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/bigquery`

`gcloud auth application-default print-access-token >/dev/null && echo " ADC OK"`


## dataset creation big query
bq --location=europe-west9 mk -d --description "Ddataset de defaillance entreprises" webstat
bq --location=europe-west9 mk -d --description "Ddataset de entreprises" insee

bq load \
  --location=europe-west9 \
  --replace \
  --source_format=CSV \
  --skip_leading_rows=1 \
  --field_delimiter=';' \
  --encoding=UTF-8 \
  --schema="business_failure_code_bq:STRING,region_name:STRING,period_scope:STRING,sector_name:STRING,business_failure_code:STRING,business_failure_description:STRING" \
  primal-context-476216-k1:webstat.bdf_business_failures_codes \
  /home/ubuntu/risk_project/codes.csv


bq load \
  --location=europe-west9 \
  --replace \
  --source_format=CSV \
  --skip_leading_rows=1 \
  --field_delimiter=';' \
  --encoding=UTF-8 \
  --schema="business_failure_code_bq:STRING,region_name:STRING,period_scope:STRING,sector_name:STRING,business_failure_code:STRING,business_failure_description:STRING" \
  primal-context-476216-k1:webstat.bdf_business_failures_codes \
  /home/ubuntu/risk_project/codes.csv


bq load \
--location=europe-west9 \
--replace \
--source_format=CSV \
--skip_leading_rows=1 \
--field_delimiter=';' \
--encoding=UTF-8 \
--autodetect \
primal-context-476216-k1:webstat.bdf_business_failures \
/home/ubuntu/risk_project/nettoyage_defaillances.csv


bq load \
  --location=europe-west9 \
  --replace \
  --source_format=CSV \
  --skip_leading_rows=1 \
  --field_delimiter=';' \
  --encoding=UTF-8 \
  --autodetect \
  primal-context-476216-k1:insee.insee_companies \
  /home/ubuntu/risk_project/A21REG_UL.csv

bq load \
  --location=europe-west9 \
  --replace \
  --source_format=CSV \
  --skip_leading_rows=1 \
  --field_delimiter=';' \
  --encoding=UTF-8 \
  --schema="A21:STRING,sector_name:STRING" \
  primal-context-476216-k1:insee.a21_codes \
  /home/ubuntu/risk_project/a21_codes.csv


bq load \
  --location=europe-west9 \
  --replace \
  --source_format=CSV \
  --skip_leading_rows=1 \
  --field_delimiter=';' \
  --encoding=UTF-8 \
  --schema="REG:STRING,Region:STRING" \
  primal-context-476216-k1:insee.regions_codes \
  /home/ubuntu/risk_project/regions_codes.csv


  