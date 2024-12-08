flake: { config, lib, pkgs, ...}:

let
  cfg = config.service.nixos-updatechecker;
  inherit (flake.packages.${pkgs.stdenv.hostPlatform.system}) nixos-updatechecker;
in {
  options.service.nixos-updatechecker = {
    enabled = lib.mkOption {
        description = "Enable periodic update checker daemon";
        type = lib.types.bool;
        default = false;
    };
    always-active = lib.mkOption {
        description = "If true, icon will be active and visible also if there's noting to update";
        type = lib.types.bool;
        default = false;
    };
    preview-command = lib.mkOption {
        description = "Command to view available updates, use {} to present changes file path, defaults to konsole";
        type = lib.types.str;
        default = "konsole -e bash -c \"cat {} && read\"";
    };
    recheck-interval = lib.mkOption {
      description = "Re-check interval in seconds (defaults to 12 hours)";
      type = lib.types.int;
      default = 3600 * 12;
    };
    icon-no-updates = lib.mkOption {
      description = "Icon that will be shown when there's no update available";
      type = lib.types.str;
      default = "software-updates-inactive";
    };
    icon-updates = lib.mkOption {
      description = "Icon that will be shown when there's an update";
      type = lib.types.str;
      default = "software-updates-updates";
    };
    icon-pending = lib.mkOption {
      description = "Icon that will be shown when update check is in process";
      type = lib.types.str;
      default = "task-recurring";
    };
  };

  config = lib.mkIf (cfg.enabled) {
    systemd.user.services.nixos-updatechecker = {
      Unit = {
        Description = "Periodically check for available NixOS updates.";
      };
      Install = {
        WantedBy = [ "graphical-session.target" ];
      };
      Service = {
        ExecStart = "${nixos-updatechecker}/bin/nixos-updatechecker";
        Restart = "always";
      };
    };

    xdg.configFile."nixos-updatechecker.json" = {
      enable = true;
      text = builtins.toJSON cfg;
    };
  };
}
