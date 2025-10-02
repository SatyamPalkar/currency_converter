#!/usr/bin/env python3
"""
Deployment helper script for Elite Currency Exchange
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"{description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"{description} failed")
        print(f"Error: {e.stderr}")
        return False

def check_git_status():
    """Check if we're in a git repository"""
    try:
        subprocess.run(["git", "status"], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("Elite Currency Exchange Deployment Helper")
    print("=" * 50)
    
    # Check if we're in a git repository
    if not check_git_status():
        print("\nNot in a git repository. Initializing...")
        if not run_command("git init", "Initialize git repository"):
            sys.exit(1)
    
    # Add all files
    if not run_command("git add .", "Add all files to git"):
        sys.exit(1)
    
    # Commit changes
    commit_message = input("\n📝 Enter commit message (or press Enter for default): ").strip()
    if not commit_message:
        commit_message = "Deploy Elite Currency Exchange"
    
    if not run_command(f'git commit -m "{commit_message}"', "Commit changes"):
        print("ℹ No changes to commit or commit failed")
    
    # Check if remote exists
    try:
        subprocess.run(["git", "remote", "get-url", "origin"], check=True, capture_output=True)
        has_remote = True
    except subprocess.CalledProcessError:
        has_remote = False
    
    if not has_remote:
        print("\nNo remote repository found.")
        print("Please create a repository on GitHub and run:")
        print("git remote add origin <your-repository-url>")
        print("git push -u origin main")
    else:
        # Push to remote
        if not run_command("git push origin main", "Push to remote repository"):
            print("Push failed. You may need to pull first or resolve conflicts.")
    
    print("\n Deployment preparation complete!")
    print("\nNext steps:")
    print("1. Go to https://share.streamlit.io")
    print("2. Connect your GitHub account")
    print("3. Select your repository")
    print("4. Choose 'app.py' as the main file")
    print("5. Click 'Deploy'")
    print("\n Your app will be available at: https://your-app-name.streamlit.app")

if __name__ == "__main__":
    main()
