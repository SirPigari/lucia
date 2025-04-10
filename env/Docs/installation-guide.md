Installation Guide
------------------

Welcome to the installation guide for Lucia! You can install the Lucia programming language using one of two methods:

*   Using [**Git Clone**](#method-1-git-clone) method
*   Using the [**Installer from GitHub**](#method-2-installer-from-github) method

### Method 1: Git Clone

To install Lucia via Git, follow these steps:

1. Open a terminal window.
    
2. Clone the Lucia repository by running the following command:

    ```bash
    git clone https://github.com/username/lucia.git lucia
    ```    

3. Navigate to the directory where the repository is cloned:
    ```bash
    cd lucia
    ```
   
4. Activate the language by running (requires Python 3.11 or higher):
    
    ```bash
    ./env/activate.py
    ```
    
5. After installation, you can verify that Lucia was successfully installed by running:
    
    ```bash
    lucia --version
    ```
    

### Method 2: Installer from GitHub

You can also install Lucia using an installer provided on GitHub:

1.  Go to the [Lucia GitHub repository](https://github.com/SirPigari/lucia).
    
2.  Download the latest installer for your operating system (Windows, macOS, or Linux).
    
3.  Run the installer and follow the on-screen instructions to complete the installation.
    
4.  After installation, open a terminal and type:
    
    ```bash
    lucia -v
    ```
    
    to verify that the installation was successful.
    

### Post-Installation Setup

After installing Lucia, make sure you have the necessary dependencies or environment variables set up. You may need to add Lucia to your system's PATH variable if the installer did not do this automatically.

### Next Steps

Once installed, you can start writing and running Lucia programs. For a simple introduction, follow the [Getting Started](language-syntax.md) guide.

If you run into any issues during installation, check the [Lucia GitHub Issues](https://github.com/SirPigari/lucia/issues) page for troubleshooting or report a new issue.