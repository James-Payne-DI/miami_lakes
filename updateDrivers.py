import os, subprocess, json, requests, zipfile, platform, shutil
from selenium import webdriver
import config

def get_latest_stable_version():
    """Fetch the latest stable ChromeDriver version from Google's JSON API."""
    url = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["channels"]["Stable"]["version"]
    except requests.RequestException as e:
        print(f"Error fetching ChromeDriver version: {e}")
        return None

def get_download_url(version):
    """Determine the appropriate ChromeDriver download URL based on OS."""
    base_url = "https://storage.googleapis.com/chrome-for-testing-public/"
    os_map = {
        "Windows": "win32",
        "Darwin": "mac-x64",
        "Linux": "linux64"
    }

    system_os = platform.system()
    if system_os not in os_map:
        print(f"Unsupported OS: {system_os}")
        return None

    return f"{base_url}{version}/{os_map[system_os]}/chromedriver-{os_map[system_os]}.zip"

def update_chromedriver(location):
    """Download and replace ChromeDriver with the latest stable version."""
    version = get_latest_stable_version()
    if not version:
        return

    download_url = get_download_url(version)
    if not download_url:
        return

    zip_path = os.path.join(location, "chromedriver.zip")
    extracted_folder = os.path.join(location, "chromedriver_extracted")
    chromedriver_path = os.path.join(location, "chromedriver")

    try:
        print(f"Downloading ChromeDriver {version} from {download_url}...")
        response = requests.get(download_url, stream=True)
        response.raise_for_status()

        with open(zip_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)

        print("Extracting ChromeDriver...")
        os.makedirs(extracted_folder, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extracted_folder)

        # Locate the actual ChromeDriver binary
        extracted_driver_path = None
        for root, _, files in os.walk(extracted_folder):
            for file in files:
                if file == "chromedriver":
                    extracted_driver_path = os.path.join(root, file)
                    break

        if not extracted_driver_path:
            print("Error: ChromeDriver binary not found in extracted files.")
            return

        # Remove the old chromedriver if it exists
        if os.path.exists(chromedriver_path):
            print("Removing old ChromeDriver...")
            os.remove(chromedriver_path)

        # Move the new driver to the desired location
        shutil.move(extracted_driver_path, chromedriver_path)

        # Ensure executable permission
        os.chmod(chromedriver_path, 0o755)

        # Cleanup
        os.remove(zip_path)
        shutil.rmtree(extracted_folder)

        print(f"ChromeDriver updated successfully at {chromedriver_path}")
    
    except requests.RequestException as e:
        print(f"Error downloading ChromeDriver: {e}")
    except zipfile.BadZipFile:
        print("Error: Downloaded file is not a valid ZIP archive.")
    except PermissionError:
        print("Permission error: Run with appropriate privileges to modify ChromeDriver.")



def get_current_chromedriver_version():
    """Retrieve the version of the currently installed ChromeDriver."""
    try:
        result = subprocess.run(["./chromedriver", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.split()[1]  # Extract the version number
    except FileNotFoundError:
        pass  # No ChromeDriver found
    return None

def check_and_update_chromedriver():
    """Check if the ChromeDriver in the current folder is up-to-date. If not, update it."""
    latest_version = get_latest_stable_version()
    if not latest_version:
        print("Could not retrieve the latest ChromeDriver version.")
        return
    
    current_version = get_current_chromedriver_version()
    
    if current_version == latest_version:
        print("ChromeDriver is up-to-date.")
    else:
        print("Updating ChromeDriver...")
        update_chromedriver(os.getcwd())  # Update in the current directory

def test_chromedriver():
    """Perform a quick test by opening and closing a browser window using ChromeDriver."""
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode
        driver = webdriver.Chrome(executable_path=config.DRIVER_PATH, options=options)
        driver.get("https://www.google.com")
        print("ChromeDriver test successful.")
        driver.quit()
    except Exception as e:
        print(f"ChromeDriver test failed: {e}")
# Example usage
# save_location = "/Users/jimmypayne/Desktop/di-devsite-automation/drivers"
# update_chromedriver(save_location)
