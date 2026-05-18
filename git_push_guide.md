# 🚀 Stress Detector AI - GitHub Push & Sharing Guide

This guide will walk you through the steps to successfully push your **Stress Detector AI** project to your new GitHub repository, and how your friend can clone, set up, and run it.

> [!NOTE]
> **What has already been done for you:**
> 1. **Removed Local Virtual Environment from Git Tracking:** We unstaged the `code/venv/` folder so that you do not push thousands of heavy local files to GitHub.
> 2. **Created a `.gitignore`:** Configured the repository to automatically ignore temporary files, python caches (`__pycache__`), local virtual environments, and very large ZIP/image assets.
> 3. **Updated the Remote URL:** Pointed your local project directly to your new repository: `https://github.com/NamrataSancheti/stress_detector_AI.git`.
> 4. **Committed Your Changes:** Created a clean local commit containing all your updated code, templates, and reports.

---

## 🔑 Part 1: Authenticating and Pushing to GitHub

Since GitHub **no longer supports account passwords** for Git operations, you must authenticate using a **Personal Access Token (PAT)**. Follow these simple steps:

### Step 1.1: Generate a GitHub Personal Access Token (PAT)
1. Go to [GitHub.com](https://github.com) and log in.
2. In the top-right corner, click your profile photo, then select **Settings**.
3. Scroll down the left sidebar and click **Developer settings**.
4. Click **Personal access tokens** -> **Tokens (classic)**.
5. Click **Generate new token** -> **Generate new token (classic)**.
6. Configure the token settings:
   - **Note:** Give it a name (e.g., `stress-detector-push-token`).
   - **Expiration:** Choose an expiration (e.g., 30 days, or No expiration).
   - **Scopes:** Select the **`repo`** checkbox (this gives permission to push to your repositories).
7. Scroll to the bottom and click **Generate token**.
8. **CRITICAL:** Copy the generated token (it starts with `ghp_...`). *You won't be able to see it again!*

---

### Step 1.2: Push to GitHub using your Token
To push your local code using your new token, open your **PowerShell** or **Command Prompt** in `c:\stress_detector\Stress_Detector` and run either of these two options:

#### Option A: One-time Push command (Recommended)
Replace `<YOUR_TOKEN>` with the token you copied (e.g. `ghp_abcdef123456...`):
```bash
git push https://<YOUR_TOKEN>@github.com/NamrataSancheti/stress_detector_AI.git master
```

#### Option B: Save the Token to Git Configuration (Permanent)
Run this to embed the token into your remote URL so you never have to type it again:
```bash
git remote set-url origin https://<YOUR_TOKEN>@github.com/NamrataSancheti/stress_detector_AI.git
```
Then simply push normally:
```bash
git push -u origin master
```

> [!WARNING]
> If your GitHub repository was initialized with a **README** or **License** online, your push might be rejected due to different histories. If this happens, force push to overwrite the remote repository with your local code:
> ```bash
> git push -u origin master --force
> ```

---

## 👥 Part 2: How Your Friend Can Set Up and Run the Project

Once you have successfully pushed the code, send your repository link `https://github.com/NamrataSancheti/stress_detector_AI.git` to your friend. They can run the project locally by following these steps:

### Step 2.1: Clone the Repository
Your friend should open a terminal and run:
```bash
git clone https://github.com/NamrataSancheti/stress_detector_AI.git
cd stress_detector_AI
```

### Step 2.2: Create a Virtual Environment (Recommended)
This keeps dependencies isolated and clean.

* **On Windows:**
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```
* **On macOS/Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### Step 2.3: Install Dependencies
They should install the exact packages required for this stress detector:
```bash
pip install -r requirements.txt
```

### Step 2.4: Run the Application
Start the Flask web app:
```bash
python code/app.py
```
Open a browser and navigate to `http://127.0.0.1:5000/` to test it!

---

## 🌐 Part 3: Deploying the Application

If your friend wants to deploy this application to the cloud, here are the two most popular options for Flask apps:

| Platform | Deployment Difficulty | Best For | How it works |
| :--- | :--- | :--- | :--- |
| **Render.com** (Free tier) | **Easy** (1-click from GitHub) | Flask web applications | Link Render to your GitHub repo, select **Python** environment, set Build command to `pip install -r requirements.txt`, and Start command to `gunicorn code.app:app` (already specified in your `requirements.txt`). |
| **PythonAnywhere** | **Easy** (Built-in Python hosting) | Python scripts & web apps | Upload/pull code, set up a web app panel pointing to `code/app.py`. |

---

### Need Help?
If you or your friend run into any issues with git or setting up the code, just ask! You are 1 step away from having this online! 🎉
