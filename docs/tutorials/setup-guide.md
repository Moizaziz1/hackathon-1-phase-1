---
sidebar_position: 2
---

# Setup Guide

This guide will help you set up your development environment to work with the Physical AI & Humanoid Robotics book content and examples.

## Prerequisites

Before starting with the examples in this book, you'll need to install the following:

### System Requirements
- Operating System: Ubuntu 20.04+ (recommended), macOS, or Windows with WSL2
- RAM: 8GB minimum, 16GB recommended
- Storage: 20GB free space for development environment

### Software Requirements
- Node.js (v18 or higher)
- npm or yarn package manager
- Git version control system
- A code editor (VS Code recommended)

## Installing Node.js and Dependencies

### Option 1: Using Node Version Manager (Recommended)

```bash
# Install nvm (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Restart terminal or run:
source ~/.bashrc

# Install and use the latest LTS version of Node.js
nvm install --lts
nvm use --lts
```

### Option 2: Direct Installation

Visit [nodejs.org](https://nodejs.org/) and download the LTS version for your operating system.

## Setting Up the Book Repository

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/AI_Robotics.git
   cd AI_Robotics
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Start the development server:
   ```bash
   npm start
   # or
   yarn start
   ```

The book should now be accessible at `http://localhost:3000`.

## ROS 2 Setup (For Robotics Examples)

For the robotics-specific examples in this book, you'll need to install ROS 2. We recommend using ROS 2 Humble Hawksbill (LTS version).

### Ubuntu Installation

```bash
# Set locale
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# Add ROS 2 apt repository
sudo apt update && sudo apt install -y software-properties-common
sudo add-apt-repository universe

# Add the repository to your sources list
sudo apt update && sudo apt install -y curl gnupg lsb-release
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros-apt-repository-latest-focal.main -o /tmp/ros.APT
sudo apt install /tmp/ros.APT

# Install ROS 2 packages
sudo apt update
sudo apt install -y ros-humble-desktop
sudo apt install -y python3-rosdep2 python3-rosinstall python3-rosinstall-generator python3-wstool build-essential
```

### Other Operating Systems

For macOS and Windows users, we recommend using Docker with pre-built ROS 2 images or using the ROS Development Studio (RDS) cloud platform for the robotics examples.

## Python Environment Setup

Many examples in this book use Python. We recommend creating a virtual environment:

```bash
# Create virtual environment
python3 -m venv robotics_env

# Activate virtual environment
source robotics_env/bin/activate  # On Windows: robotics_env\Scripts\activate

# Install common robotics libraries
pip install numpy scipy matplotlib
```

## Verifying Your Setup

To verify that your environment is properly configured:

1. Check Node.js version:
   ```bash
   node --version
   # Should show v18.x.x or higher
   ```

2. Check npm version:
   ```bash
   npm --version
   # Should show version number
   ```

3. Test the book server:
   ```bash
   npm start
   # Should start the development server
   ```

## Troubleshooting

### Common Issues

**Issue**: Node.js version is too old
**Solution**: Update Node.js to v18 or higher using nvm or by downloading from nodejs.org

**Issue**: npm install fails with permission errors
**Solution**:
   ```bash
   # Change npm default directory
   mkdir ~/.npm-global
   npm config set prefix '~/.npm-global'
   # Add to your PATH in ~/.bashrc or ~/.zshrc:
   export PATH=~/.npm-global/bin:$PATH
   ```

**Issue**: ROS 2 installation fails
**Solution**: Check the official ROS 2 installation guide for your specific operating system and Ubuntu version.

## Next Steps

Once your environment is set up, you can:

1. Explore the book content at `http://localhost:3000`
2. Navigate to the ROS 2 Fundamentals module to begin with robotics concepts
3. Try the hands-on labs in each module
4. Work on the capstone project to integrate all concepts

Your development environment is now ready for the Physical AI & Humanoid Robotics book content!