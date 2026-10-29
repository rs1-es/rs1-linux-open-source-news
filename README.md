# RS1 Linux News

Javascript-free Linux/open source news aggregator.

This is the source code of https://news.rs1.es. A Python script parses feeds (RSS/Atom/RDF), joins them, sorts them by date and generates one static page per language and section (news, videos, more). It runs as an AWS Lambda function (container image) that uploads the pages to the S3 bucket serving the site.

### Layout

- `container/lambda/parser/news_parser.py`: feed list per language and HTML generation.
- `container/lambda/parser/index.py`: Lambda handler.
- `container/Dockerfile`, `container/serverless.yml`, `container/deploy.sh`: image build and deployment.
- `public/`: static files (CSS, about, 404, sitemap).

### Run locally

Requires `feedparser`, `pytz` and `func_timeout`. Set `OUTPUT_DIR` to write the pages to a local folder instead of uploading them to S3 (`boto3` is only needed without it):

```
cd container/lambda/parser
OUTPUT_DIR=../../../out python news_parser.py
```

### Deploy

Run `container/deploy.sh`: it builds the image with podman, pushes it to ECR, writes the new digest into `container/serverless.yml` and runs `serverless deploy` (use `--no-deploy` to skip the last step). Requires the AWS CLI with a valid session.

### Contribute

Create an issue if you want to add a page. Provide the feed link.
