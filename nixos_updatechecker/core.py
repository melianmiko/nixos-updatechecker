import os
import tempfile
import subprocess
import socket

from nixos_updatechecker.config import APP_CONFIG
from nixos_updatechecker.utils import get_config_dir, get_locks


def get_changes():
  with tempfile.TemporaryDirectory() as temp_path:
    # Create new flake file
    config_dir = get_config_dir()
    new_flake = f"{temp_path}/new_flake.lock"
    subprocess.check_output([
      f"nix", "flake", "update",
      "--output-lock-file", new_flake,
      "--flake", config_dir
    ])
    assert os.path.isfile(new_flake)

    # Check is there any difference between old and new flakes
    new_lock_metadata = subprocess.check_output([
      "nix", "flake", "metadata",
      "--json",
      "--reference-lock-file", new_flake,
      config_dir,
    ]).decode("utf-8")
    current_lock_metadata = subprocess.check_output([
      "nix", "flake", "metadata",
      "--json",
      config_dir,
    ]).decode("utf-8")
    if get_locks(new_lock_metadata) == get_locks(current_lock_metadata):
      return []

    # Create temporary system
    new_system = f"{temp_path}/system"
    subprocess.check_output([
      "nix", "build",
      "--no-write-lock-file",
      "--reference-lock-file", new_flake,
      "--out-link", new_system,
      f"{config_dir}#nixosConfigurations.{socket.gethostname()}.config.system.build.toplevel"
    ])
    assert os.path.islink(new_system)

    # Create diff report
    diff_report = subprocess.check_output([
      "nix", "store", "diff-closures", "/nix/var/nix/profiles/system", new_system
    ]).decode("utf-8")

  changes = []
  for line in diff_report.split("\n"):
    if line.startswith("nixos"):
      continue
    if line.split(": ")[0] in APP_CONFIG["ignored-pkgs"]:
      continue
    if line == "":
      continue

    changes.append(line)

  return changes
