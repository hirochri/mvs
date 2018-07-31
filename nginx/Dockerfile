FROM nginx
#Install npm
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get install -y gnupg2 && \
    curl -sL https://deb.nodesource.com/setup_10.x | bash - && \
    apt-get install -y nodejs
#Create folder for videos/images
RUN mkdir /usr/share/nginx/media
#Grab nginx/babel/webpack configs
COPY modified_nginx.conf /etc/nginx/nginx.conf
COPY mvs_website/.babelrc /mvs_website/.babelrc
COPY mvs_website/webpack.config.js /mvs_website/webpack.config.js
#Do npm stuff
COPY mvs_website/package.json /mvs_website/package.json
WORKDIR /mvs_website
RUN npm install
#Grab main index file
COPY mvs_website/index.html /mvs_website/index.html
#Move website over (except stuff in .dockerignore)
COPY mvs_website/src /mvs_website/src/
#Build website
RUN npm run build && \
    cp -r dist/ /usr/share/nginx/html/dist/ && \
    cp index.html /usr/share/nginx/html/index.html
