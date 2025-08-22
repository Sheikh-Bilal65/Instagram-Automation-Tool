# Instagram Automation Tool

**Empower Your Automation Journey!**

If this tool has helped you understand or streamline your Instagram automation tasks, consider supporting its continued development. Your contribution, no matter how small, fuels the creation of more free, powerful, and feature-rich tools like this one. Let's build amazing things together!

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/bilalsheikh)

### 💸 Crypto Donation

If you’d like to support this project, you can donate via cryptocurrency!

#### **Option 1: Binance ID (Direct Transfer for Binance Users)**
- **Binance ID:** `150697028`
  - *(This allows instant transfers between Binance accounts. Just use my ID in the “Send via Binance ID” section!)*

#### **Option 2: Direct Wallet Address (BNB Smart Chain BEP20)**

**BNB (Binance Coin, BEP20):**  
- **Network:** BNB Smart Chain (BEP20)  
- **Wallet Address:**  
  `0xef6e84f601441439e809088fe0355ec63b9f0017`

---

**USDT (Tether USD, BEP20):**  
- **Network:** BNB Smart Chain (BEP20)  
- **Wallet Address:**  
  `0xef6e84f601441439e809088fe0355ec63b9f0017`

---

> **Note:**  
> Do not send NFTs to this address.  
> For other cryptocurrencies, or if you’d like an ERC20 or TRC20 address, reach out via email or GitHub!


---

This tool automates interactions on Instagram, specifically designed for liking posts, commenting, and viewing reels/stories. It leverages Selenium for browser automation and Python's multiprocessing to handle multiple accounts concurrently, making the process efficient and scalable.

### What it does
- Reads your Instagram accounts (username and password) from an Excel file (`account.xlsx`).
- Logs into Instagram using provided credentials.
- Navigates to a specified Instagram post, reel, or story URL.
- Performs actions such as liking posts, commenting, or viewing reels/stories.
- Handles multiple accounts in parallel for faster execution.
- Provides a summary of attempted and successful actions, including posts already liked.

### Quick Start

1)  **Install dependencies** (Python 3.9+ recommended):
    ```bash
    pip install -r requirements.txt
    ```

2)  **Prepare your accounts Excel file** (`account.xlsx`):
    Create an Excel file named `account.xlsx` in the same directory as the script. It must contain at least two columns:
    -   `username` (required)
    -   `password` (required)

    Example `account.xlsx` content:
    | username          | password   |
    |-------------------|------------|
    | your_username_1   | your_pass_1|
    | your_username_2   | your_pass_2|

3)  **Run the automation script**:
    Use the `instagram_automator.py` script with command-line arguments to specify the target URL and desired actions.

    **Example Usage:**
    -   **To like a post 5 times (using up to 5 unique accounts if available):**
        ```bash
        python instagram_automator.py --url "https://www.instagram.com/p/C2VPXLfyET3/" --likes 5
        ```
    -   **To comment on a post once:**
        ```bash
        python instagram_automator.py --url "https://www.instagram.com/p/C2VPXLfyET3/" --comments 1
        ```
    -   **To view a reel:**
        ```bash
        python instagram_automator.py --url "https://www.instagram.com/reel/C4Imaz-S8jw/" --reel-views 1
        ```
    -   **To view a reel for a specific duration (e.g., 60 seconds):**
        ```bash
        python instagram_automator.py --url "https://www.instagram.com/reel/C4Imaz-S8jw/" --reel-views 1 --reel-watch-time 60
        ```
        *The `--reel-watch-time` argument allows you to specify how long each account watches a reel (in seconds). The duration must be between 0 and 120 seconds. If a value greater than 120 is provided, it will default to 120 seconds. If a value less than or equal to 0 is provided, it will default to 45 seconds.*
    -   **To perform multiple actions (e.g., 2 likes and 1 comment):**
        ```bash
        python instagram_automator.py --url "https://www.instagram.com/reel/C2kE2gSyhe1/" --likes 2 --comments 1
        ```

    The script will automatically use available accounts in parallel (up to 2 concurrent processes by default) and provide a summary of actions performed.

### Output Summary

After execution, the script will print an "Automation Summary" to the console, detailing:
-   Requested actions (likes, comments, reel views, story views).
-   Number of accounts found.
-   Total likes attempted.
-   Breakdown of "New likes given" and "Posts already liked".
-   Total comments given, reel views performed, and story views performed.

### Important Notes on Functionality

Currently, the **liking posts** and **reel viewing** functionalities are robust and expected to work reliably. The **commenting** and **story viewing** features may experience occasional issues due to frequent changes in Instagram's web interface. I am continuously working to improve and stabilize these features for future updates.

If you encounter any problems or have suggestions, please don't hesitate to reach out! Your feedback is invaluable.

### About the Creator

Hello! I'm **Sheikh Bilal**, a passionate Java developer who loves coding and automation. This tool is a testament to that passion, designed to help you understand and explore Instagram automation.

Connect with me:
*   **GitHub**: [https://github.com/sheikh-bilal65](https://github.com/sheikh-bilal65)
*   **LinkedIn**: [https://www.linkedin.com/in/bilal-ahmad2](https://www.linkedin.com/in/bilal-ahmad2)
*   **Gmail**: [bilalahmadallbd@gmail.com](mailto:bilalahmadallbd@gmail.com)
*   **Instagram**: [https://www.instagram.com/sheikhh.bilal/](https://www.instagram.com/sheikhh.bilal/)


This tool is provided for **educational purposes only**. It demonstrates automation techniques and is not intended for violating Instagram's Terms of Service or any applicable laws. The creator, Sheikh Bilal, is not responsible for any misuse of this tool or any consequences that may arise from its use. Users are solely responsible for adhering to Instagram's policies and local regulations.
