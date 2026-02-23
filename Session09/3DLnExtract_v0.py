# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.19.10",
#     "pyzmq>=27.1.0",
# ]
# ///

import marimo

__generated_with = "0.19.11"
app = marimo.App()


@app.cell
def _():
    #==============================================================================
    # Parameters adjustable by the user
    #==============================================================================
    reportList = 'pdfscreenedURLs.csv'          # Contains the list of reports to download
    #reportList = 'annual_reports_with_sp500.csv'   # Contains the list of reports to download
    col_name = 'URL' # Column name in the reportList file that contains the URLs

    # Set parameter for the 'year to download' 
    years = 2019 # 2023 # 2022  

    # Set keywords to search for in a report  
    keywords = ['water'] # ['air', 'water']  # ['pollution']  # ['segment', 'segments']   

    # Set parameter for the 'percentage (in decimal point) of reports to download' 
    pct2DL = 1    # .5    
    # [For debugging] Set parameter for reporting details of the page numbered 'DetailedPage'
    DetailedPage = 1   # Note: Python is 0-indexed; so DetailedPage = 1 means the second page of the report

    #==============================================================================
    # Unused parameters
    #==============================================================================
    #yearEnd = 2023
    #yearStart = 2014
    #years = [yearStart - i for i in range(yearStart - yearEnd + 1)]
    #==============================================================================
    return


@app.cell
def _(mo):
    mo.md(r"""
 
    """)
    return


@app.cell
def _():
    # Import the required libraries
    import os
    import subprocess
    from urllib.parse import urljoin, urlparse

    # Print all environment variables
    #for key, value in os.environ.items():
    #    print(f'{key}={value}')

    # Get the current working directory and create a local directory there
    current_directory = os.getcwd()
    print(f"current_directory: {current_directory}\n")


    #==================================================================================
    # Get the value of the RepositoryName environment variable
    repository_name = os.getenv('RepositoryName')

    # Find the position of the repository name in the current directory path
    repo_index = current_directory.find(repository_name)

    # Retain only the part of the path up to and including the repository name
    if repo_index != -1:
        repo_dir = current_directory[:repo_index + len(repository_name)]
    else:
        repo_dir = current_directory

    print(f"Repo directory: {repo_dir}\n")
    #==================================================================================


    # Path to the document directory  
    doc_dir = os.path.join(repo_dir, 'docArchive')
    # Create the directory if it does not exist
    os.makedirs(doc_dir, exist_ok=True)


    # Create three subfolders (if not already created)
    subfolders = ['DLdocs', 'pagesExtracted', 'Parsed'] # Define the subfolders to be created
    # Create the subfolders if they do not already exist
    for subfolder in subfolders:
        subfolder_path = os.path.join(doc_dir, subfolder)
        os.makedirs(subfolder_path, exist_ok=True)
        print(f"Subfolder created or already exists: {subfolder_path}")
    print(" ")

    # List contents in the document directory
    subprocess.run(['ls', '-la', doc_dir])
    return


if __name__ == "__main__":
    app.run()
