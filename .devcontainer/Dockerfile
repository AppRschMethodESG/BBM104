# Use the official image as a parent image 
FROM rocker/r-ver:4.4.2

# Install Python and radian
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

# Create a virtual environment and install radian
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install radian

# Set the virtual environment as the default Python environment
ENV PATH="/opt/venv/bin:$PATH"

# Clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Install git
RUN apt-get update && apt-get install -y git

# Create the vscode user and set it as the default user
RUN useradd -ms /bin/bash vscode

# Grant sudo privileges to the vscode user
RUN apt-get update && apt-get install -y sudo && \
    echo "vscode ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER vscode

# Create the library directory
RUN mkdir -p /usr/local/lib/R/site-library

# Set the library path and install the packages
RUN R -e "repo_path <- normalizePath(getwd()); lib_path <- file.path(repo_path, 'R_Library'); .libPaths(c(lib_path, .libPaths()))"

# Install multiple R packages
RUN R -e "install.packages(c('tidyverse'), repos='http://cran.rstudio.com/')"

#RUN R -e "install.packages(c('tidyverse', \
## 'lubridate', \
#'kableExtra'), repos='http://cran.rstudio.com/')"