#!/bin/bash

# Function to check if command was successful
check_status() {
    if [ $? -eq 0 ]; then
        echo "✅ $1"
    else
        echo "❌ $1 failed"
        exit 1
    fi
}

# Function to print section headers
print_header() {
    echo -e "\n📌 $1"
    echo "----------------------------------------"
}

# Get environment name from argument or use default
ENV_NAME=${1:-"myenv"}

print_header "Setting up Python Virtual Environment: $ENV_NAME"

# 1. Create virtual environment
print_header "Creating virtual environment: $ENV_NAME"
python3 -m venv $ENV_NAME
check_status "Virtual environment creation"

# 2. Activate virtual environment
print_header "Activating virtual environment"
source $ENV_NAME/bin/activate
check_status "Virtual environment activation"

# 3. Upgrade pip in virtual environment
print_header "Upgrading pip in virtual environment"
python3 -m pip install --upgrade pip
check_status "Pip upgrade"

# 4. Install requirements if requirements.txt exists
if [ -f "requirements.txt" ]; then
    print_header "Installing requirements from requirements.txt"
    python3 -m pip install -r requirements.txt
    check_status "Requirements installation"
else
    print_header "No requirements.txt found - skipping dependencies installation"
fi

# Print environment information
print_header "Environment Information"
echo "Python Version:"
python3 --version
echo -e "\nPip Version:"
pip --version
echo -e "\nPython Path:"
which python3
echo -e "\nVirtual Environment Location:"
echo $VIRTUAL_ENV

print_header "Setup Complete! ✨"
echo "To activate this environment later, run:"
echo "source $ENV_NAME/bin/activate"
echo -e "\nTo deactivate, run:"
echo "deactivate"
