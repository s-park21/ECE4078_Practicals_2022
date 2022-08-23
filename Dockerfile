FROM tinsirius/ece4078_prac:ubuntu-60e7b60

RUN python3 -m pip install --no-cache-dir notebook jupyterlab ipympl

ARG NB_USER=ece4078
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV NB_UID ${NB_UID}
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}

COPY . ${HOME}
USER root
RUN chown -R ${NB_UID} ${HOME}

WORKDIR ${HOME}
USER ${NB_USER}
