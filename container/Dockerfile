FROM public.ecr.aws/lambda/python:3.9

RUN yum update -y

RUN pip3.9 install feedparser datetime pytz func_timeout

COPY lambda/parser/index.py ${LAMBDA_TASK_ROOT}
COPY lambda/parser/parser.py ${LAMBDA_TASK_ROOT}

CMD [ "index.handler" ]
