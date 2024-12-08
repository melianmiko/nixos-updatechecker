import os
import tempfile
import subprocess
import socket

CONFIG_DIR = "/etc/nixos"
IGNORED_PKGS = [
  "source"
]


def get_changes():
  with tempfile.TemporaryDirectory() as temp_path:
    # Create new flake file
    new_flake = f"{temp_path}/new_flake.nix"
    subprocess.check_output([
      f"nix", "flake", "update",
      "--output-lock-file", new_flake,
      "--flake", CONFIG_DIR
    ])
    assert os.path.isfile(new_flake)

    # Check is there any difference between old and new flakes
    with open(new_flake, "r") as f:
      new_flake_data = f.read()
    with open(f"{CONFIG_DIR}/flake.lock", "r") as f:
      current_flake_data = f.read()
    if new_flake_data == current_flake_data:
      return []

    # Create temporary system
    new_system = f"{temp_path}/system"
    subprocess.check_output([
      "nix", "build",
      "--no-write-lock-file",
      "--reference-lock-file", new_flake,
      "--out-link", new_system,
      f"{CONFIG_DIR}#nixosConfigurations.{socket.gethostname()}.config.system.build.toplevel"
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
    if line.split(": ")[0] in IGNORED_PKGS:
      continue
    if line == "":
      continue

    changes.append(line)

  return changes
