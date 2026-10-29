#!/bin/bash
# Construye la imagen, la sube a ECR, actualiza el digest en serverless.yml
# y despliega. Con --no-deploy se detiene antes de "serverless deploy".
set -euo pipefail
cd "$(dirname "$0")"

REGION=eu-west-1
REPO=news-rs1-es
ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
REGISTRY=$ACCOUNT.dkr.ecr.$REGION.amazonaws.com

aws ecr get-login-password --region $REGION | podman login --username AWS --password-stdin $REGISTRY

# Crea el repositorio si no existe
aws ecr describe-repositories --region $REGION --repository-names $REPO >/dev/null 2>&1 ||
    aws ecr create-repository --region $REGION --repository-name $REPO --image-scanning-configuration scanOnPush=true

podman build -t $REPO .
podman tag $REPO:latest $REGISTRY/$REPO:latest
podman push $REGISTRY/$REPO:latest

# Digest de lo que acaba de quedar en ECR
DIGEST=$(aws ecr describe-images --region $REGION --repository-name $REPO \
    --image-ids imageTag=latest --query 'imageDetails[0].imageDigest' --output text)
echo "Digest: $DIGEST"

sed -i -E "s#^( *image: ).*#\1$REGISTRY/$REPO@$DIGEST#" serverless.yml

if [ "${1:-}" != "--no-deploy" ]; then
    serverless deploy
fi
