{
  python3Packages,
  pkgs,
}:

python3Packages.buildPythonApplication {
  pname = "nixos-updatechecker";
  version = "1.0.0";
  pyproject = true;

  src = ../..;

  build-system = with python3Packages; [
    poetry-core
  ];
  nativeBuildInputs = with pkgs; [
    wrapGAppsHook3
    gobject-introspection
  ];
  buildInputs = with pkgs; [
    libappindicator
  ];
  propagatedBuildInputs = with python3Packages; [
    pygobject3
  ];
}
