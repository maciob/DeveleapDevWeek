FROM mysql:8.0.30-debian
ENV MYSQL_ROOT_PASSWORD password \
    MYSQL_USER app \
    MYSQL_PASSWORD pass
RUN env
ADD billingdb.sql /docker-entrypoint-initdb.d