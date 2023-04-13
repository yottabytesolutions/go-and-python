FROM golang:1.20

WORKDIR /app

COPY . /app/
RUN go mod download
RUN go build -o upstream_app

ENV GIN_MODE=release
CMD ["/app/upstream_app"]
