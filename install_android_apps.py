import sys
import csv
import requests
import atexit
import signal
import os
import subprocess
from enum import Enum

class Arguments(Enum):
  FDROID_CSV_PATH = 1
  URL_CSV_PATH = 2


def install_android_apps():
  check_res = subprocess.run(["adb devices", "-l"], shell=True, check=True, capture_output=True, text=True)
  adb_output = check_res.stdout.splitlines()
  if len(adb_output) <= 1:
    print(check_res.stdout)
    print("No devices detected with adb. Aborting...")
    sys.exit(0)

  apk_paths = []

  def exit_handler():
    for path in apk_paths:
      os.remove(path)

  def kill_handler(*args):
    sys.exit(0)

  atexit.register(exit_handler)
  signal.signal(signal.SIGINT, kill_handler)
  signal.signal(signal.SIGTERM, kill_handler)

  apk_paths += download_from_fdroid()
  apk_paths += download_from_url_csv()

  for path in apk_paths:
    print("Install " + path)
    subprocess.run(["adb install ./" + path ], shell=True)

def download_from_fdroid() -> list[str]:
  apk_paths = []
  fdroid_csv_path = sys.argv[Arguments.FDROID_CSV_PATH.value]
  if not fdroid_csv_path: 
      print('No FDroid csv given.')
      return apk_paths
  
  filename_template = "<package_name>_<version_code>.apk"

  with open(fdroid_csv_path, mode="r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
      filename = filename_template.replace("<package_name>", row["packageName"]).replace("<version_code>", row["versionCode"])
      apk_paths.append(download_file("https://f-droid.org/repo/" + filename, filename))

  return apk_paths

def download_from_url_csv() -> list[str]:
  apk_paths = []
  url_csv_path = sys.argv[Arguments.URL_CSV_PATH.value]
  if not url_csv_path: 
      print('No url csv given.')
      return apk_paths

  with open(url_csv_path, mode="r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
      apk_paths.append(download_file(row["url"], row["packageName"] + ".apk"))
  
  return apk_paths

def download_file(url: str, filename: str) -> str:
    res = requests.get(url, headers={"Content-Type": "application/vnd.android.package-archive"}, allow_redirects=True)
    with open(filename, 'wb') as f:
      f.write(res.content)
    return filename
  

if __name__ == "__main__":
  if len(sys.argv) == 0:
    print("Usage: `python install_default_apps.py <path_to_fdroid_csv> <path_to_download_csv>`") 
  install_android_apps()