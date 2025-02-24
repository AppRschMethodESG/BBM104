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

# Create the codespace user and set up its home directory
RUN useradd -m -s /bin/bash codespace

# Add the codespace user to various groups
RUN usermod -aG ssh,hugo,nvm,nvs,conda,php,rvm,sdkman,docker,golang,oryx,python,pipx codespace

# Grant sudo privileges to the codespace user without requiring a password
RUN echo 'codespace ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Set the appropriate permissions for the home directory
RUN chown -R codespace:codespace /home/codespace

# Switch to the codespace user
USER codespace

# Set the working directory
#WORKDIR /home/codespace


# Install additional Ubuntu packages
RUN apt-get update && apt-get install -y \
    libharfbuzz-dev \
    libfribidi-dev \
    libpng-dev \
    libtiff5-dev \
    libjpeg-dev \
    libssl-dev \
    libxml2-dev \
    libcurl4-openssl-dev \
    libfreetype-dev || true && \
    libfreetype6-dev || true && \
    dpkg-query -L libharfbuzz-dev libfribidi-dev libpng-dev libtiff5-dev libjpeg-dev libssl-dev libxml2-dev libcurl4-openssl-dev libfreetype-dev libfreetype6-dev || true 

# Change ownership of the R library directory to the codespace user
RUN sudo mkdir -p /usr/local/lib/R/site-library && \
    sudo chown -R codespace:codespace /usr/local/lib/R/site-library

# Install R packages
RUN ls -la /usr/local/lib/R/site-library && \
    ls -la /usr/local/lib && \
    R -e 'print(getwd()); install.packages(c("withr", "xml2", "languageserver"), repos="http://cran.rstudio.com/")' && \
    ls -la /usr/local/lib/R/site-library && \
    ls -la /usr/local/lib/R/


#USER vscode

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


