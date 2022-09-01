FROM mysql:8.0.30-debian
ENV MYSQL_ROOT_PASSWORD password
ENV MYSQL_DATABASE billdb
ENV MYSQL_USER app 
ENV MYSQL_PASSWORD pass
RUN env
ADD Billing/db/billingdb.sql /docker-entrypoint-initdb.d
