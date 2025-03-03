# BBM104 Applied Research Methods in ESG - Demo codes

### Installation

- To set up R and install the required packages (e.g., tidyverse for R 4.4.2) in a Github Codespaces / Lightning.ai Studio created from this repo,
   - execute the two commands below in a terminal (bash shell) of the Codespaces / Studio (after replacing the filename **`SetupRunOnce.sh`** accordingly):

`chmod +x SetupRunOnce.sh`  
`./SetupRunOnce.sh`

---

**!!! Note**: 

- For Github _**Codespaces**_:
   - Replace `SetupRunOnce.sh` with `SetupRunOnce_Codespaces.sh`

- For Lightning.ai _**Studio**_ (click [here](https://lightning.ai/pricing) to sign up for a free-tier account using your school email address):
   - After logging on Lightning.ai, create a new Studio by clicking the `+ New Studio` button on the upper right corner of the webpage on Lightning.ai; then select `Code` and click `Start`
   - After the Studio is loaded, do the following :
      - Click on the auto-generated name of Studio and change it to `AppRschMethodESG`; then hit `Enter` key to accept the change
      - Click the cell right below the upper middle edge of the Studio environment and select `Show and Run Commands >` from the dropdown menu
      - Type `Git: Clone` and select exactly this choice from the dropdown list
      - Type `https://github.com/AppRschMethodESG/BBM104.git` when asked `Provide repository URL or pick a repository source`; then hit `Enter` key and click `ok`
      - Click `Open` to the GitHub repo when asked `Would you like to open the cloned repository, or add it to the current workspace?`
      - After the Studio is reloaded, click `Terminal` on the dropdown menu; select `New Terminal`
      - In the terminal, execute the two commands by replacing `SetupRunOnce.sh` with `SetupRunOnce_Lightning.ai.sh`
      - When being asked to select another Python interpreter, click the cell right below the upper middle edge of the Studio environment and select `Show and Run Commands >` from the dropdown menu
      - Type `Python: Select Interpreter` and select exactly this choice (i.e., the first) from the dropdown list; then select from the next dropdown list the entry ended with the `Recommended` indication
      - Similarly, when prompted to select from a list of `Python Environments`, select the entry ended with the `Recommended` indication
   - When opening a `.ipynb` file, click the `Python` button near the upper right corner and select from the dropdown list the entry ended with the `Recommended` indication

- Can use the following command to _**log the output and error to files**_ while also displaying them in the terminal (after replacing the filename `SetupRunOnce.sh` accordingly):
   - `./SetupRunOnce.sh > >(tee script_output.log) 2> >(tee script_error.log >&2)`

