#!/usr/bin/env bash
# This script sets up web servers for the deployment of web_static.

# Install Nginx if not already installed
install_nginx() {
    if ! command -v nginx &> /dev/null; then
        apt-get update
        apt-get install -y nginx
    fi
}

# Create necessary folders if they don't exist
create_folders() {
    local folders=("/data" "/data/web_static" "/data/web_static/releases" "/data/web_static/shared" "/data/web_static/releases/test")
    for folder in "${folders[@]}"; do
        mkdir -p "$folder"
    done
}

# Create a fake HTML file
create_fake_html() {
    local content="<html><body>Test HTML file</body></html>"
    echo "$content" > "/data/web_static/releases/test/index.html"
}

# Create or recreate symbolic link
create_symbolic_link() {
    local current_dir="/data/web_static/current"
    if [ -L "$current_dir" ]; then
        rm "$current_dir"
    fi
    ln -s "/data/web_static/releases/test" "$current_dir"
}

# Set ownership recursively
set_ownership() {
    chown -R ubuntu:ubuntu "/data"
}

# Update Nginx configuration
update_nginx_config() {
    local config_file="/etc/nginx/sites-available/default"
    local location_block="location /hbnb_static {\n    alias /data/web_static/current/;\n}\n"
    sed -i '/location \/hbnb_static {/,/}/d' "$config_file"
    sed -i "/server {/a $location_block" "$config_file"
}

# Restart Nginx
restart_nginx() {
    service nginx restart
}

# Main function
main() {
    install_nginx
    create_folders
    create_fake_html
    create_symbolic_link
    set_ownership
    update_nginx_config
    restart_nginx
}

# Run the main function
main

