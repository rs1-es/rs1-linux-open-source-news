FROM public.ecr.aws/lambda/python:3.12

RUN pip install --no-cache-dir feedparser pytz func_timeout

COPY lambda/parser/index.py ${LAMBDA_TASK_ROOT}
COPY lambda/parser/news_parser.py ${LAMBDA_TASK_ROOT}

CMD [ "index.handler" ]
