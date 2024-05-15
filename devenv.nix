{ pkgs, ... }:

{
  packages = with pkgs; [
    nodePackages.pyright
  ];

  languages.python = {
    enable = true;
    venv = {
      enable = true;
      requirements = ./requirements.txt;
    };
  };

  services.postgres = {
    enable = true;
    listen_addresses = "127.0.0.1";
    initialDatabases = [
      { name = "psrdb"; }
    ];
  };

  pre-commit.hooks = {
    black.enable = true;
    flake8.enable = true;
  };
}
