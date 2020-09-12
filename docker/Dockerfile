
FROM debian:buster-slim

USER root

RUN apt-get update -qq && apt install -y --no-install-recommends \
      curl git python3-pip chromium-driver apache2 libapache2-mod-wsgi-py3 \
    && curl -sL https://deb.nodesource.com/setup_12.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get clean -y

RUN pip3 install flask selenium requests

WORKDIR /var/
RUN mkdir /var/sbgn-rest-renderer
COPY app /var/sbgn-rest-renderer/app
COPY api /var/sbgn-rest-renderer/api
# COPY node_modules /var/sbgn-rest-renderer/node_nodules
COPY package.json LICENSE.md server.js index.html templatelibsbgn.xslt scripts/apache_config.sh /var/sbgn-rest-renderer/

WORKDIR /var/sbgn-rest-renderer
RUN npm install \
   && npm run build-bundle-js
   

RUN a2enmod wsgi \
   && /bin/sh apache_config.sh \
   && a2dissite 000-default \
   && a2ensite sbgn_rest

RUN mkdir static \
   && chown -R www-data:www-data static \
   && echo '{"status": "true"}' > static/status

EXPOSE 80

# CMD bash -c "service apache2 start && service apache2 reload & npm run watch-server"
# CMD apachectl -D FOREGROUND
CMD bash -c "tail -f /dev/null"
