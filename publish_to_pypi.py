#!/usr/bin/env python3
"""
Publishing Helper Script for Documents to Markdown

This script helps automate the process of publishing to PyPI.
Run this script to get step-by-step guidance.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command, description=""):
    """Run a command and return success status."""
    print(f"\n🔄 {description}")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ Success!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False


def check_prerequisites():
    """Check if all prerequisites are installed."""
    print("🔍 Checking prerequisites...")
    
    required_packages = ['build', 'twine']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        install_cmd = f"pip install {' '.join(missing_packages)}"
        if not run_command(install_cmd, "Installing required packages"):
            return False
    
    return True


def clean_build_artifacts():
    """Clean previous build artifacts."""
    print("\n🧹 Cleaning build artifacts...")
    
    dirs_to_clean = ['build', 'dist', 'documents_to_markdown.egg-info']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ Removed {dir_name}/")
        else:
            print(f"ℹ️  {dir_name}/ doesn't exist")


def build_package():
    """Build the package."""
    print("\n🔨 Building package...")
    return run_command("python -m build", "Building wheel and source distribution")


def check_package_contents():
    """Check what's included in the package."""
    print("\n📋 Checking package contents...")
    
    # Find the tar.gz file
    dist_files = list(Path('dist').glob('*.tar.gz'))
    if not dist_files:
        print("❌ No source distribution found!")
        return False
    
    tar_file = dist_files[0]
    print(f"📦 Contents of {tar_file.name}:")
    
    return run_command(f"tar -tzf {tar_file}", "Listing package contents")


def upload_to_testpypi():
    """Upload to TestPyPI."""
    print("\n🧪 Uploading to TestPyPI...")
    print("⚠️  Make sure you have configured your TestPyPI credentials!")
    print("   See PUBLISHING_GUIDE.md for setup instructions.")
    
    response = input("\nDo you want to upload to TestPyPI? (y/N): ")
    if response.lower() != 'y':
        print("⏭️  Skipping TestPyPI upload")
        return True
    
    return run_command("twine upload --repository testpypi dist/*", "Uploading to TestPyPI")


def test_testpypi_installation():
    """Test installation from TestPyPI."""
    print("\n🔬 Testing TestPyPI installation...")
    print("This will create a temporary virtual environment to test the installation.")
    
    response = input("Do you want to test TestPyPI installation? (y/N): ")
    if response.lower() != 'y':
        print("⏭️  Skipping TestPyPI installation test")
        return True
    
    # Create test environment
    test_env = "test_pypi_env"
    if os.path.exists(test_env):
        shutil.rmtree(test_env)
    
    commands = [
        f"python -m venv {test_env}",
        f"{test_env}/Scripts/activate && pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ documents-to-markdown" if os.name == 'nt' else f"source {test_env}/bin/activate && pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ documents-to-markdown",
        f"{test_env}/Scripts/activate && python -c \"from documents_to_markdown import DocumentConverter; print('✅ TestPyPI installation successful!')\"" if os.name == 'nt' else f"source {test_env}/bin/activate && python -c \"from documents_to_markdown import DocumentConverter; print('✅ TestPyPI installation successful!')\""
    ]
    
    for cmd in commands:
        if not run_command(cmd, f"Running: {cmd}"):
            print("❌ TestPyPI installation test failed!")
            return False
    
    # Cleanup
    shutil.rmtree(test_env)
    print("✅ TestPyPI installation test passed!")
    return True


def upload_to_pypi():
    """Upload to PyPI."""
    print("\n🚀 Uploading to PyPI...")
    print("⚠️  This will make your package publicly available!")
    print("⚠️  Make sure you have configured your PyPI credentials!")
    
    response = input("\nAre you ready to upload to PyPI? (y/N): ")
    if response.lower() != 'y':
        print("⏭️  Skipping PyPI upload")
        return True
    
    return run_command("twine upload dist/*", "Uploading to PyPI")


def main():
    """Main publishing workflow."""
    print("=" * 60)
    print("🚀 Documents to Markdown - PyPI Publishing Helper")
    print("=" * 60)
    
    steps = [
        ("Check Prerequisites", check_prerequisites),
        ("Clean Build Artifacts", clean_build_artifacts),
        ("Build Package", build_package),
        ("Check Package Contents", check_package_contents),
        ("Upload to TestPyPI", upload_to_testpypi),
        ("Test TestPyPI Installation", test_testpypi_installation),
        ("Upload to PyPI", upload_to_pypi),
    ]
    
    for step_name, step_func in steps:
        print(f"\n{'='*20} {step_name} {'='*20}")
        
        if not step_func():
            print(f"\n❌ Step '{step_name}' failed!")
            print("Please check the error messages above and try again.")
            return 1
        
        print(f"✅ Step '{step_name}' completed successfully!")
    
    print("\n" + "=" * 60)
    print("🎉 Publishing process completed!")
    print("=" * 60)
    
    print("\n📋 Next Steps:")
    print("1. Check your package on PyPI: https://pypi.org/project/documents-to-markdown/")
    print("2. Test installation: pip install documents-to-markdown")
    print("3. Update your GitHub repository with release notes")
    print("4. Share your package with the community!")
    
    print("\n📚 Resources:")
    print("- PyPI Project: https://pypi.org/project/documents-to-markdown/")
    print("- GitHub Repository: https://github.com/ChaosAIs/DocumentsToMarkdown")
    print("- Publishing Guide: PUBLISHING_GUIDE.md")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
