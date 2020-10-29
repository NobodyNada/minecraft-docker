#!/usr/bin/python3
import os
import requests
import sys
import urllib

def log(string):
    print("run.py: " + string)

version = os.getenv("MINECRAFT_VERSION", "release")
jvm_opts = os.getenv("JVM_OPTS")
log("Using version " + version)


# Download the manifest file
manifest_url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
log("Downloading " + manifest_url)
manifest = requests.get(manifest_url).json()

# If we have a channel name, find the latest version of that channel
resolved_version = manifest["latest"].get(version)
if resolved_version is not None:
    version = resolved_version
    log("Resolved version " + version)

# Find the elemnt of the versions array whose ID is the version we're looking for
version_manifest = None
try:
    version_manifest = next(v for v in manifest["versions"] if v["id"] == version)
except StopIteration:
    log("Could not find version or channel " + version)
    log("Available versions: ")
    for v in manifest["versions"]:
        log("    " + v["id"] + " [" + v["type"] + "]")
    log("Available channels: ")
    for (k, v) in manifest["latest"].items():
        log("    " + v + " [" + k + "]")
    sys.exit(1)

meta_url = version_manifest["url"]
log("Downloading " + meta_url)
metadata = requests.get(meta_url).json()
download = metadata["downloads"]["server"]
sha1 = download["sha1"]
url = download["url"]
filename = "/minecraft/jars/" + sha1 + ".jar"

# If we've already downloaded the jar, don't download again
if os.path.exists(filename):
    log("Using cached download " + filename)
else:
    log("Downloading " + url)
    urllib.request.urlretrieve(url, filename)

os.chdir("/minecraft/data")
args = ["-jar", filename] + sys.argv[1:]
if jvm_opts is not None and jvm_opts != "":
    args = jvm_opts.split(" ") + args
args = ["java"] + args
log("Executing: " + " ".join(args))
os.execvp(args[0], args)
