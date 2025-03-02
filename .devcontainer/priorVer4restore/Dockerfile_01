# Use the official image as a parent image 
FROM rocker/r-ver:4.4.2

# Install Python and radian
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

# Create a virtual environment and install required Python packages
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install \
    radian \
    pandas \
    pytesseract \
    nltk \
    PyMuPDF \
    llama_parse \
    pyppeteer \
    playwright \
    rclone \
    jupyter \
    ipykernel \
    notebook

# Set the virtual environment as the default Python environment
ENV PATH="/opt/venv/bin:$PATH"

# Create a Jupyter kernel for the virtual environment
RUN /opt/venv/bin/python -m ipykernel install --user --name=venv --display-name "Python (venv)"

# Clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Install git, sudo, ..., and groff (for pdfroff as a pdf_engine)
RUN apt-get update && apt-get install -y git sudo curl nano groff texlive-latex-base pandoc

# Install rclone
RUN sudo -v ; curl https://rclone.org/install.sh | sudo bash

# Create the necessary groups
RUN groupadd ssh && \
    groupadd hugo && \
    groupadd nvm && \
    groupadd nvs && \
    groupadd conda && \
    groupadd php && \
    groupadd rvm && \
    groupadd sdkman && \
    groupadd docker && \
    groupadd golang && \
    groupadd oryx && \
    groupadd python && \
    groupadd pipx

RUN ls -la /home

# Create the codespace user and set up its home directory
RUN useradd -m -s /bin/bash codespace

RUN ls -la /home

# Add the codespace user to various groups
RUN usermod -aG ssh,hugo,nvm,nvs,conda,php,rvm,sdkman,docker,golang,oryx,python,pipx codespace

# Grant sudo privileges to the codespace user without requiring a password
RUN echo 'codespace ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Set the appropriate permissions for the home directory
RUN chown -R codespace:codespace /home/codespace

# Install aptitude
RUN apt-get update && apt-get install -y aptitude

# Install libfontconfig1-dev with aptitude, instead of apt-get
RUN aptitude update && aptitude install -y \
    pkg-config \
    libfontconfig1-dev || true
# Find the location of the libfontconfig1-dev package    
RUN dpkg -L libfontconfig1-dev || true
# Set the PKG_CONFIG_PATH environment variable to ensure finding the fontconfig.pc file
ENV PKG_CONFIG_PATH=/usr/lib/x86_64-linux-gnu/pkgconfig:/usr/share/pkgconfig:/usr/lib/x86_64-linux-gnu/pkgconfig

# Install additional Ubuntu packages as root
RUN apt-get update && apt-get install -y \
#    curl \
    libnss3 \ 
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxcomposite1 \
    libxrandr2 \
    libxdamage1 \
    libxfixes3 \
    libxext6 \
    libxi6 \
    libxtst6 \
    libxrender1 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxkbcommon0 \
    libasound2-data \
    libharfbuzz-dev \
    libfribidi-dev \
    libpng-dev \
    libtiff5-dev \
    libjpeg-dev \
    libssl-dev \
    libxml2-dev \
    libcurl4-openssl-dev \
    libfreetype-dev || true && \
    libfreetype6-dev || true 
# Note: Adding  || true && allows the Dockerfile to continue processing even if there are errors during the installation of libfreetype-dev and libfreetype6-dev.

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && \
    sudo apt-get install -y nodejs

# Add npm global installation path to PATH
ENV PATH=/usr/lib/node_modules/.bin:$PATH

# Set NODE_PATH to include global node_modules
ENV NODE_PATH=/usr/lib/node_modules

# Install globally required npm packages
RUN npm install -g \
    yarn \
    puppeteer \
    puppeteer-extra \
    puppeteer-extra-plugin-stealth \
    user-agents

# Install additional npm package using yarn
RUN yarn add puppeteer-extra-plugin-user-preferences

# Change ownership of the virtual environment directory to the codespace user
RUN chown -R codespace:codespace /opt/venv

# Change ownership of the venv site-packages directory to the codespace user
RUN chown -R codespace:codespace /opt/venv/lib/python3.*/site-packages/

# Change ownership of the global node_modules directory to the codespace user
RUN chown -R codespace:codespace /usr/lib/node_modules

# Change ownership of the R library directory to the codespace user
RUN mkdir -p /usr/local/lib/R/site-library && \
    chown -R codespace:codespace /usr/local/lib/R/site-library

# Switch to the codespace user
USER codespace

# Install Chrome browser for Puppeteer
#RUN npx puppeteer install chrome --platform=linux --install-deps
#RUN npx puppeteer browsers install chrome # This command is not working in the Dockerfile

# Install Playwright browsers in venv
RUN /opt/venv/bin/playwright install
RUN /opt/venv/bin/playwright install-deps 

# Install R packages
RUN ls -la /usr/local/lib/R/site-library && \
    ls -la /usr/local/lib && \
    R -e 'print(getwd()); install.packages(c("languageserver", "tidyverse", "lubridate", "kableExtra"), repos="http://cran.rstudio.com/")' && \
    ls -la /usr/local/lib/R/site-library 

#===============================================================================
# Below is an example of how to chain commands in a single RUN command using ';' and '&&' and use  \ to continue the command on the next line. However, the command cannot serve the purpose of creating R_Library for installing the packages there because it was created in a container for preparing a container image for the actual container creation later. 
# 
# Note: R_Library should be created using a post-create command in the devcontainer.json file. 
#===============================================================================
#RUN R -e 'print(getwd()); repo_path <- "/workspaces/BBM104"; lib_path <- file.path(repo_path, "R_Library"); dir.create(lib_path, recursive = TRUE, showWarnings = FALSE); system(paste("sudo chown -R vscode:vscode", lib_path)); system(paste("sudo chmod -R 777", lib_path)); .libPaths(c(lib_path, .libPaths())); install.packages(c("withr"), lib=lib_path, repos="http://cran.rstudio.com/")' && \
#    ls -la /workspaces/BBM104/R_Library 
#===============================================================================
# !!!Note: Each RUN command in a Dockerfile is executed in a separate shell, and variables are not persisted between them. Therefore, the lib_path variable is not available in a second RUN command. To avoid this issue, you can combine the two RUN commands into a single command as shown below:
#===============================================================================