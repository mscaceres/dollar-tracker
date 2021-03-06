FROM python:3.7

RUN mkdir -p /usr/src/app/wheelhouse && mkdir -p /usr/src/app/dollar-tracker && mkdir -p /root/.config/dollar-tracker
WORKDIR /usr/src/app/dollar-tracker

RUN pip install --upgrade pip
RUN pip install wheel==0.29.0 && pip install pytest

COPY . /usr/src/app/dollar-tracker
COPY ./resources/logs.json /root/.config/dollar-tracker
RUN pip wheel --wheel-dir=/usr/src/app/wheelhouse .
RUN pip install --prefer-binary --no-index --find-links=/usr/src/app/wheelhouse dollar-tracker
RUN rm -fr /usr/src/app/dollar-tracker/dollar_tracker \
    /usr/src/app/dollar-tracker/*.py \
    /usr/src/app/dollar-tracker/Dockerfile \
    /usr/src/app/dollar-tracker/HOWTO \
    /usr/src/app/dollar-tracker/resources \
    /usr/src/app/wheelhouse


VOLUME /usr/src/app/dollar-tracker

ENTRYPOINT ["dollar-tracker"]
