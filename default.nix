let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-24.11";
  pkgs = import nixpkgs { config = {}; overlays = []; };
in
{
  nixos-updatechecker = pkgs.callPackage ./nix/pkgs/nixos-updatechecker.nix { };
}
