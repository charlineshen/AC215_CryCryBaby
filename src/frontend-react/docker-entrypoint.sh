#!/bin/sh

echo "frontend-react container is running"

nginx_server() {
    nginx -g 'daemon off;'
}

nginx_server