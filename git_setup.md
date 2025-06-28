
## Step 1: Install Git
On Windows:
1. Visit https://git-scm.com/download/win
2. Download and run the installer.
3. During installation:
   - Choose "Git from the command line and also from 3rd-party software"
   - Use default settings unless you have specific preferences
4. After installation, open Git Bash.

On macOS:
1. Open Terminal.
2. Type: git --version
3. If Git is not installed, macOS will prompt you to install Xcode Command Line Tools. Accept it.

## Step 2: Generate an SSH Key

1. Open Git Bash (Windows) or Terminal (macOS).
2. Run:
   ssh-keygen -t ed25519 -C "your_email@example.com"
   (Replace with your GitHub email)
3. Press Enter to accept the default file location.
4. Set a passphrase (optional but recommended).
5. Add the SSH key to the SSH agent:
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519

## Step 3: Add SSH Key to GitHub

1. Copy your public key:
   cat ~/.ssh/id_ed25519.pub
2. Copy the output (starts with ssh-ed25519).
3. Go to https://github.com → Settings → SSH and GPG keys.
4. Click "New SSH key", give it a title, and paste the key.

## Step 4: Clone a Repository

1. Go to the GitHub repository you want to clone.
2. Click the green "Code" button → Select "SSH".
3. Copy the SSH URL (e.g., git@github.com:username/repo.git).
4. In your terminal, run:
   git clone git@github.com:username/repo.git

You're all set!
