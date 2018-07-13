FROM nginx
COPY modified_nginx.conf /etc/nginx/nginx.conf
#Install npm
RUN apt-get update
RUN apt-get install -y curl
RUn apt-get install -y gnupg2
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get install -y nodejs
COPY mvs_website/  /mvs_website/
WORKDIR /mvs_website/
RUN sh static_setup.sh
