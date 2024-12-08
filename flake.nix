{
  description = ''
    Simple update checker for NixOS with tray indicator.
  '';

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    let
      # Declare nixos-updatechecker package for every architecture
      packagesConfig = flake-utils.lib.eachDefaultSystem (system: let
        pkgs = import nixpkgs { inherit system; };
      in {
        packages.nixos-updatechecker = pkgs.callPackage ./nix/pkgs/nixos-updatechecker.nix { };
      });

    in {

      nixosModules.nixos-updatechecker = { config, ... }: {
        config.home-manager.sharedModules = [(import ./nix/modules/home.nix self)];
      };

    } // packagesConfig;
}
