FROM squidfunk/mkdocs-material:9.5.49 AS builder
WORKDIR /docs
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY mkdocs.yml .
COPY docs ./docs
RUN mkdocs build --strict

FROM nginx:1.27-alpine
COPY --from=builder /docs/site /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
