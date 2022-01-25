FROM caddy:2.4.6-builder-alpine AS builder

RUN xcaddy build --with github.com/caddy-dns/cloudflare@91cf700356a1cd0127bcc4e784dd50ed85794af5


FROM caddy:2.4.6-alpine as production

COPY --from=builder /usr/bin/caddy /usr/bin/caddy
COPY Caddyfile /etc/caddy/Caddyfile


FROM production AS staging

COPY Caddyfile.staging /etc/caddy/Caddyfile
