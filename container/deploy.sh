#!/bin/bash
# Empaqueta la Lambda en un zip y la despliega (crea el rol y la función si no
# existen). Con --no-deploy sólo genera function.zip.
set -euo pipefail
cd "$(dirname "$0")"

REGION=eu-west-1
FUNCTION=news-rs1-es-parser
ROLE=news-rs1-es-parser
BUCKET=news.rs1.es
RUNTIME=python3.12
MEMORY=1024
TIMEOUT=300

rm -rf build function.zip
pip install -q --no-cache-dir --target build -r lambda/parser/requirements.txt
cp lambda/parser/index.py lambda/parser/news_parser.py lambda/parser/feeds.json build/
find build -name __pycache__ -prune -exec rm -rf {} +
(cd build && zip -qr ../function.zip .)
echo "function.zip: $(du -h function.zip | cut -f1)"

[ "${1:-}" = "--no-deploy" ] && exit 0

ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
ROLE_ARN=arn:aws:iam::$ACCOUNT:role/$ROLE

# Rol de ejecución: logs y acceso al bucket
if ! aws iam get-role --role-name $ROLE >/dev/null 2>&1; then
    aws iam create-role --role-name $ROLE --assume-role-policy-document '{
      "Version": "2012-10-17",
      "Statement": [{"Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]
    }' >/dev/null
    aws iam attach-role-policy --role-name $ROLE \
        --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
    aws iam put-role-policy --role-name $ROLE --policy-name s3-bucket --policy-document '{
      "Version": "2012-10-17",
      "Statement": [{"Effect": "Allow", "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
                     "Resource": "arn:aws:s3:::'$BUCKET'/*"}]
    }'
    sleep 10  # propagación del rol
fi

if aws lambda get-function --region $REGION --function-name $FUNCTION >/dev/null 2>&1; then
    aws lambda update-function-code --region $REGION --function-name $FUNCTION \
        --zip-file fileb://function.zip >/dev/null
    aws lambda wait function-updated --region $REGION --function-name $FUNCTION
    aws lambda update-function-configuration --region $REGION --function-name $FUNCTION \
        --runtime $RUNTIME --memory-size $MEMORY --timeout $TIMEOUT >/dev/null
else
    aws lambda create-function --region $REGION --function-name $FUNCTION \
        --runtime $RUNTIME --handler index.handler --role $ROLE_ARN \
        --memory-size $MEMORY --timeout $TIMEOUT --zip-file fileb://function.zip \
        --tags project=news-rs1-es >/dev/null
fi
aws lambda wait function-updated --region $REGION --function-name $FUNCTION

# Archivos estáticos. Sin --delete y sin las páginas que genera la Lambda
aws s3 sync ../public s3://$BUCKET --exclude "index.html" --exclude "*/index.html"
echo "Desplegado: $FUNCTION"
