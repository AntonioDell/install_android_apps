# install_android_apps.py

This script is used to install android apps based on csv files via adb onto an android phone.
The sources of these apps need to be F-Droid or similar open APK repositories.
Apps installed via Google Play Store can be synced using Google services.

## Why?

When you try to avoid using Google, it is sometimes necessary to get apps as APK files from different sources.
Migrating to another device can be tedious in such a situation.
This script enables you, to collect your sources in a CSV file manually once and then install them on the device.

## Requirements

- Install python 3
- Enable developer mode on android device
- In Settings -> Developer Settings enable [USB-Debugging](https://www.makeuseof.com/tag/what-is-usb-debugging-mode-on-android-makeuseof-explains/)
- [Install adb](https://www.makeuseof.com/tag/new-adb-make-process-simple-easy/) on your computer
- Connect android device to computer

## Usage

For all apps installed via F-Droid you can use the export functionality of F-Droid to get a CSV list of your apps (see [F-Droid reference file](./sample/sample_fdroid_apps.csv)). It is important that the column `packageName` actually contains the valid package name. 

For other apps you need to create a CSV file based on the format in the [url apps reference file](./sample/sample_url_apps). Use APK repos like [apkure](https://apkpure.com/) to get a direct link to a direct download for a APK file of your desired app and add them to CSV. Put the url inside paranthesis like this: "https://some-url.com". The column `packageName` in this file is not important, since the `url` column is used directly to download the APK file

Execute the script like this:
`python install_android_apps.py path/to/fdroid/file.csv path/to/url/file.csv`

If you don't use F-Droid, you can use empty paranthesis instead:
`python install_android_apps.py "" path/to/url/file.csv`

## License

[Creative Commons License](https://en.wikipedia.org/wiki/Creative_Commons_license), essentially do what you want, but no warranties of any kind!
