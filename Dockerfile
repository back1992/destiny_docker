FROM django:onbuild
 RUN sed -i 's/http:\/\/archive\.ubuntu\.com\/ubuntu\//http:\/\/mirrors\.163\.com\/ubuntu\//g' /etc/apt/sources.list
 RUN apt-get clean
 RUN apt-get update && apt-get -y install cron

 # Add crontab file in the cron directory
 ADD crontab /etc/cron.d/hello-cron

 # Give execution rights on the cron job
 RUN chmod 0644 /etc/cron.d/hello-cron

 # Create the log file to be able to run tail
 RUN touch /var/log/cron.log

 # Run the command on container startup
 CMD cron && tail -f /var/log/cron.log
# ENV PYTHONUNBUFFERED 1
# RUN mkdir /code
# WORKDIR /code
 ADD requirements.txt /code/
 RUN pip install -r requirements.txt
 RUN pip install --trusted-host pypi.douban.com -i http://pypi.douban.com/simple/ -U Django
 RUN pip install --trusted-host pypi.douban.com -i http://pypi.douban.com/simple/ -U psycopg2
 RUN pip install --trusted-host pypi.douban.com -i http://pypi.douban.com/simple/ -U scrapy
 RUN pip install --trusted-host pypi.douban.com -i http://pypi.douban.com/simple/ -U django_pandas
# ADD . /code/
 RUN python manage.py makemigrations --noinput
 RUN python manage.py migrate --noinput
 RUN python manage.py collectstatic --noinput

