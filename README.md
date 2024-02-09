# AthenaAI

AthenaAI introduces an interactive chatbot experience, leveraging dynamic content processing and state-of-the-art AI to engage users in meaningful conversations. This project enhances interactivity and responsiveness, offering a unique platform for both entertainment and utility purposes.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Usage](#usage)
  - [Installation Guide](#installation-guide)
- [FAQ](#faq)
- [Credits](#credits)
- [Disclaimer](#disclaimer)
- [Contributing](#contributing)
  - [How to Contribute](#how-to-contribute)
- [Badges](#badges)
- [Dependencies](#dependencies)
- [License](#license)

## Overview

AthenaAI is designed to provide an engaging chatbot experience, allowing users to interact with a virtual character powered by advanced AI. This project integrates dynamic content processing capabilities, making conversations more relevant and engaging.

## Features

- **Interactive Chat Sessions:** Engage in continuous dialogue with the AI, with the ability to process commands dynamically.
- **Input Validation:** Ensures that user inputs are well-formed and prompts for corrections when necessary.
- **Enhanced Message Management:** Tracks and logs interactions for a comprehensive chat history.
- **External API Integration:** Seamlessly interacts with external services and APIs for a richer user experience.
- **User Experience Enhancements:** Includes processing animations and timeout mechanisms to keep users engaged.
- **Robust Error Handling:** Gracefully manages exceptions and errors, ensuring uninterrupted conversations.
- **Advanced Data Processing:** Parses and combines JSON responses, tailoring content to user inputs.

## Usage

### Installation Guide

1. **Download AthenaAI:**
   - Visit the AthenaAI GitHub repository.
   - Click "Code" > "Download ZIP", then save and extract it to your desired location.

2. **Extract the Project:**
   - Locate the downloaded ZIP file and extract its contents.

3. **Set Up the Environment:**
   - Navigate to the AthenaAI project directory.
   - Run `execute.bat` by double-clicking on it. This script creates a virtual environment, installs required packages, and starts the setup script.

4. **Terminate the Script:**
   - Close the running script by typing `!exit` or using the `CTRL+C` shortcut.

5. **Data Extraction Mode:**
   - Open your command line interface and navigate to the AthenaAI project directory.
   - Execute `call py startup.py --tags dataex` to enter data extraction mode.

6. **Login to Dreamgen:**
   - Go to "dreamgen.com/app", log in or register a new account.

7. **Prepare for Data Extraction:**
   - Click "Discover", enter any chat with an AI model, and press `F12` to open developer tools.
   - Select the arrow icon pointing to the right, then go to the "Network" tab.
   - Click "Clear network log", and send a message in the chat with the AI while keeping the network tab open.

8. **Extract API Data:**
   - After sending a message, right-click on any item in the network log, select "Copy" > "Copy all as PowerShell" (ensure you choose the "ALL" option).

9. **Process Extracted Data:**
   - Close the browser developer tools and return to the AthenaAI window.
   - Paste the copied text into the program and click "Process" to extract relevant information.

10. **Copy Results for Configuration:**
    - Copy the output, typically including `auth_session`, `auth_organization`, and `referer` values, to a notepad for later use.

11. **Configuration Mode:**
    - In the command line interface, execute `call py startup.py --tags ce` to open the configuration editor.

12. **Update Configuration:**
    - In the configuration editor, fill in the fields with the data you extracted. For example, under the Credentials section, input your name, email, password, and a description.

13. **Specific Configuration Details:**
    - Based on the extracted data, update the following in your configuration:
        - **REFERER:** Replace with the full URL you got, e.g., `https://dreamgen.com/app/rp/scenarios/sessions/912378a2-329f-4f...`.
        - **ORGANIZATION:** Replace with your `auth_organization` value.
        - **TOKEN:** Use your `auth_session` value here.
        - In the IDENTIFICATION section, change "SESSION_ID" to match the session ID from your URL.

    Example:
    If your extracted data includes:
    ```
    auth_session=pjcgs16xyibog9l1...
    auth_organization=f92607ae-9a1d-4cf...
    referer=https://dreamgen.com/app/rp/scenarios/sessions/912378a2-329f-4f...
    ```
    Configure these in the respective fields as described.

14. **Save Configurations:**
    - Click "File" > "Save" or use `CTRL+S` to save your changes.

15. **Close Configuration Editor:**
    - Exit the configuration editor and return to the command line interface.

16. **Start AthenaAI:**
    - Execute `call py startup.py --tags start` to launch the fully configured AI model.

## FAQ

**Q: How does AthenaAI use the Dreamgen API to interact with users?**  
A: AthenaAI sends user input to the Dreamgen API along with configuration settings and awaits a response. This process allows AthenaAI to dynamically generate interactive content based on the user's input.

**Q: Are there any limits on the number of requests to the Dreamgen API that a user can make with AthenaAI?**  
A: Yes, there is a limit of 50,000 characters per month for API requests. This is determined by the quota provided by the Dreamgen API.

**Q: Does AthenaAI support languages other than English?**  
A: Currently, AthenaAI supports only English for processing user inputs and generating responses.

**Q: What privacy measures are implemented in AthenaAI to protect user data?**  
A: As of now, specific privacy measures have not been detailed. Users are encouraged to be mindful of the information they share during interactions with AthenaAI.

**Q: Can users customize the AI character they are conversing with?**  
A: Users can start separate sessions with a preconfigured AI character. However, the possibility for customizing the name, gender, or conversation style of the AI character is not directly supported in the current version.

**Q: How can I report a bug or submit feedback about AthenaAI?**  
A: Users can report bugs or submit feedback through the GitHub issues tab on the project's repository page.

**Q: Are there any educational resources or guides available for new users of AthenaAI?**  
A: The primary source of guidance for new users is the README.md file included in the project, which provides instructions on how to get started with AthenaAI.

**Q: Will AthenaAI be supporting additional platforms beyond Windows in the future?**  
A: There are no current plans to support platforms other than Windows.

**Q: What are the future development plans for AthenaAI? Are there any new features or improvements in the works?**  
A: The future development plans for AthenaAI are currently undefined. Users are encouraged to follow the project's GitHub repository for updates.

**Q: Is there a community or user forum for AthenaAI where I can share experiences with others?**  
A: As of now, there is no dedicated community or forum for AthenaAI users. However, users can use the GitHub issues section for discussions and sharing experiences.

## Credits

- **VermiNew:** Project Author and Lead Developer.

- **Dreamgen:** For providing the API used in AthenaAI.

## Disclaimer

This software and guide are provided 'as is', without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

Please be aware that "DreamGen" and the "Opus" model are not my creations, but I use them in this project. My project is designed to interface with these technologies and extend their functionality. The use of "DreamGen" and "Opus" is subject to their respective terms of use and licensing agreements. Users of this software should ensure they comply with such terms.

Users are responsible for their use of "DreamGen", "Opus", and this project. It is important to respect the intellectual property and privacy rights of others, and to use these technologies legally and ethically.

## Contributing

Contributions to this project are welcome! Whether you're fixing a bug, improving the documentation, or adding a new feature, your assistance can help make this project better for everyone.

### How to Contribute

1. **Fork the Repository**  
   Start by forking the repository to your GitHub account. This will be your workspace for making changes.

2. **Clone Your Fork**  
   Clone your forked repository to your local machine to start working on the changes.

3. **Create a New Branch**  
   For each set of changes or new feature, create a new branch. Naming the branch something relevant to the changes you plan to make can help keep things organized.

4. **Make Your Changes**  
   With your new branch checked out, you can start making changes. If you're adding a new feature or substantial changes, it's a good idea to discuss it in the issues section first.

5. **Commit Your Changes**  
   Commit your changes with clear and detailed commit messages. This helps others understand the purpose and scope of your changes.

6. **Push Changes to GitHub**  
   Push your changes to your fork on GitHub.

7. **Submit a Pull Request**  
   Once you've pushed your changes, submit a pull request from your fork to the main repository. Provide a detailed description of the changes and reference any related issues.

8. **Code Review**  
   After submitting a pull request, the project creator will review your changes. Be open to feedback and ready to make additional tweaks or clarifications.

## Badges

[![License](https://img.shields.io/github/license/VermiNew/AthenaAI.svg?style=flat-square)](LICENSE)
[![Batch](https://img.shields.io/badge/Platform-Batch-blue.svg)](https://en.wikipedia.org/wiki/Batch_file)
[![Java](https://img.shields.io/badge/Platform-Java-red.svg)](https://www.java.com/)
[![Build Status](https://img.shields.io/travis/com/VermiNew/AthenaAI/master.svg?style=flat-square)](https://travis-ci.com/VermiNew/AthenaAI)
[![Coverage Status](https://img.shields.io/codecov/c/github/VermiNew/AthenaAI/master.svg?style=flat-square)](https://codecov.io/gh/VermiNew/AthenaAI)
[![Stable Release](https://img.shields.io/badge/Release-Stable-darkgreen.svg)](https://github.com/VermiNew/AthenaAI/releases/tag/stable)
[![Contributor Friendly](https://img.shields.io/badge/Contributions-Welcome-darkgreen.svg)](https://github.com/VermiNew/AthenaAI/blob/main/CONTRIBUTING.md)
[![GitHub Issues](https://img.shields.io/github/issues/VermiNew/AthenaAI.svg?style=flat-square)](https://github.com/VermiNew/AthenaAI/issues)
[![GitHub Stars](https://img.shields.io/github/stars/VermiNew/AthenaAI.svg?style=social&label=Stars)](https://github.com/VermiNew/AthenaAI/stargazers)

## Dependencies

- Windows Machine
- Batch
- Python
- DreamGen Access

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
