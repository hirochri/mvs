FROM nginx
#Install npm
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get install -y gnupg2 && \
    curl -sL https://deb.nodesource.com/setup_10.x | bash - && \
    apt-get install -y nodejs
#Grab nginx config
COPY modified_nginx.conf /etc/nginx/nginx.conf
#Grab main index file
COPY mvs_website/index.html /usr/share/nginx/html/index.html
#Do npm stuff
COPY mvs_website/package.json /mvs_website/package.json
WORKDIR /mvs_website
RUN npm install
#Move website over (except stuff in .dockerignore)
COPY mvs_website/src /mvs_website/src/
COPY mvs_website/webpack.config.js /mvs_website/webpack.config.js
#Build website
RUN npm run build && \
    cp -r dist/ /usr/share/nginx/html/dist/
