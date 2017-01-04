FROM django:onbuild
 RUN sed -i 's/http:\/\/archive\.ubuntu\.com\/ubuntu\//http:\/\/mirrors\.163\.com\/ubuntu\//g' /etc/apt/sources.list
 RUN apt-get clean
 RUN apt-get -y update && apt-get -y install upgrade
 RUN apt-get install postgresql postgresql-contrib

 USER postgres
 RUN /etc/init.d/postgresql start \
    && psql --command "CREATE USER pguser WITH SUPERUSER PASSWORD 'pguser';" \
    && createdb -O pguser pgdb

 USER root
 RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.3/main/pg_hba.conf
 RUN echo "listen_addresses='*'" >> /etc/postgresql/9.3/main/postgresql.conf
 EXPOSE 5432
 RUN mkdir -p /var/run/postgresql && chown -R postgres /var/run/postgresql
 VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]
 USER postgres
 CMD ["/usr/lib/postgresql/9.3/bin/postgres", "-D", "/var/lib/postgresql/9.3/main", "-c", "config_file=/etc/postgresql/9.3/main/postgresql.conf"]


 # Add crontab file in the cron directory
# ADD crontab /etc/cron.d/hello-cron
#
# # Give execution rights on the cron job
# RUN chmod 0644 /etc/cron.d/hello-cron
#
# # Create the log file to be able to run tail
# RUN touch /var/log/cron.log
#
# # Run the command on container startup
# CMD cron && tail -f /var/log/cron.log


 # build talib in docker
 RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
# ENV PYTHONUNBUFFERED 1
# RUN mkdir /code
# WORKDIR /code
 ADD requirements.txt /code/
 RUN pip install -r requirements.txt
 RUN pip install --trusted-host pypi.douban.com -i http://pypi.douban.com/simple/  Django \
      psycopg2 \
      scrapy \
      django_pandas \
      numpy \
#      TA-Lib \
      quandl

# ADD . /code/
 RUN python manage.py makemigrations --noinput
 RUN python manage.py migrate --noinput
 RUN python manage.py collectstatic --noinput

