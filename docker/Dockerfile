
FROM node:10.22

USER root
WORKDIR /var/
RUN mkdir /var/sbgn-rest-renderer
COPY . /var/sbgn-rest-renderer

WORKDIR /var/sbgn-rest-renderer
RUN npm install
EXPOSE 80

CMD npm run debug-build