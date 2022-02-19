FROM ubuntu:18.04

RUN apt-get update

WORKDIR /root/

RUN DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends \
    vim \
    wget \
    nginx \
    php-fpm \
&& rm -rf /var/lib/apt/lists/* && mkdir -p /run/php/

ADD ./nginx_default_site /etc/nginx/sites-available/default
ADD ./php_fpm_pool_config /etc/php/7.2/fpm/pool.d/www.conf

RUN useradd -ms /bin/bash --uid 31337 chall && sed -i 's/www-data/chall/' /etc/nginx/nginx.conf

WORKDIR /home/chall/service

CMD php-fpm7.2 && nginx -g 'daemon off;'
