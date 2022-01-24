FROM caddy:2.4.6-alpine as production

COPY Caddyfile /etc/caddy/Caddyfile


FROM production AS staging

COPY Caddyfile.staging /etc/caddy/Caddyfile
