FROM public.ecr.aws/lambda/python:3.12

COPY lambda/parser/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY lambda/parser/index.py ${LAMBDA_TASK_ROOT}
COPY lambda/parser/news_parser.py ${LAMBDA_TASK_ROOT}
COPY lambda/parser/feeds.json ${LAMBDA_TASK_ROOT}

CMD [ "index.handler" ]
