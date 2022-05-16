FROM python:3.8.2 as package_maker
RUN pip install -U pip && pip install setuptools==46.1.1 wheel==0.34.2 pip_tools==4.5.1
COPY ./requirements.txt /
# RUN pip-compile /requirements.txt

FROM python:3.8.2-alpine
COPY --from=package_maker /requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt --no-cache-dir && rm -rf /requirements.txt
COPY ./code /code
WORKDIR /code
ENTRYPOINT python3 main.py
