#!/bin/sh
mkdir -p ~/.streamlit
echo "[server]" > ~/.streamlit/config.toml
echo "headless = true" >> ~/.streamlit/config.toml
echo "enableCORS = false" >> ~/.streamlit/config.toml
echo "" >> ~/.streamlit/config.toml