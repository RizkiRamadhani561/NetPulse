FROM python:3.14-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 HOME=/tmp
WORKDIR /opt/snmpsim
RUN python -m pip install --no-cache-dir snmpsim==1.2.2 \
    && groupadd --system --gid 10001 snmpsim \
    && useradd --system --uid 10001 --gid snmpsim --home-dir /tmp --shell /usr/sbin/nologin snmpsim \
    && mkdir -p /opt/snmpsim/data \
    && chown -R snmpsim:snmpsim /opt/snmpsim /tmp
COPY --chown=snmpsim:snmpsim fixtures/snmp/system.snmprec /opt/snmpsim/data/system.snmprec
USER 10001:10001
EXPOSE 1161/udp
CMD ["snmpsimd.py", "--agent-udpv4-endpoint=0.0.0.0:1161", "--data-dir=/opt/snmpsim/data", "--logging-method=stdout"]
