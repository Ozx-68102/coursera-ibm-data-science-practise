import importlib
import subprocess
import sys
import time
import warnings

PACKAGES = ["pandas", "dash", "httpx", "plotly"]


def install_packages() -> None:
    total = 0
    success = 0
    failed = 0
    exist = 0

    if not PACKAGES:
        print("No packages to install.")
        return None

    print("Begin to install packages.")
    print("=" * 40)
    time.sleep(0.5)
    for package in PACKAGES:
        try:
            importlib.import_module(package)
            print(f"{total + 1}. {package} is already installed.")
            exist += 1
        except ImportError:
            try:
                result = subprocess.run(args=[sys.executable, "-m", "pip", "show", package], stdout=subprocess.DEVNULL,
                                        stderr=subprocess.DEVNULL)
                if result.returncode == 0:
                    print(f"{total + 1}. {package} is already installed.")
                    exist += 1
                    continue

                raise subprocess.CalledProcessError(result.returncode, result.args)
            except subprocess.CalledProcessError:
                try:
                    print(f"{total + 1}. {package} is not installed. So installation will begin soon...")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                    success += 1
                except subprocess.CalledProcessError:
                    warning_msg = f"Failed to install {package}. Please check your internet connection or Python environment."
                    warnings.warn(warning_msg)
                    failed += 1
                    continue

        total += 1

    time.sleep(0.5)
    print("=" * 40)
    print(f"Success: {success}, failed:{failed}, existed:{exist}. Total: {total}.")
    print("Accomplished.")
    return None


if __name__ == "__main__":
    install_packages()
