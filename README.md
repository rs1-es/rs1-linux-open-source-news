# RS1 Linux News

Javascript-free Linux/open source news aggregator.

This is the source code of https://news.rs1.es. A Python script parses feeds (RSS/Atom/RDF), joins them, sorts them by date and generates one static page per language and section (news, videos, more). It runs as an AWS Lambda function (zip package, Python 3.12) that uploads the pages to the S3 bucket serving the site.

### Layout

- `container/lambda/parser/news_parser.py`: feed download and HTML generation.
- `container/lambda/parser/feeds.json`: feeds per language and section (`news`, `videos`, `more`).
- `container/lambda/parser/requirements.txt`: pinned dependencies.
- `container/lambda/parser/index.py`: Lambda handler.
- `container/deploy.sh`: builds the zip package and deploys it.
- `public/`: static files (CSS, about, 404, sitemap).

### Run locally

Run `pip install -r container/lambda/parser/requirements.txt`. Set `OUTPUT_DIR` to write the pages to a local folder instead of uploading them to S3 (`boto3` is only needed without it):

```
cd container/lambda/parser
OUTPUT_DIR=../../../out python news_parser.py
```

### Deploy

Run `container/deploy.sh`: it installs the dependencies, builds `function.zip`, creates the IAM role and the Lambda function if they don't exist (or updates their code and configuration), and syncs `public/` to S3. Use `--no-deploy` to only build the zip. Requires the AWS CLI with a valid session. The schedule trigger is configured in the AWS console and must point to the function `news-rs1-es-parser`.

### Contribute

Create an issue if you want to add a page, providing the feed link, or open a pull request adding it to `container/lambda/parser/feeds.json`:

```
{"url": "https://example.com/feed", "name": "Example", "home": "https://example.com/"}
```
