{
  description = "dev environment for mxp";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/22.05";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    system = "x86_64-linux";
    overlays = [];
    pkgs = import nixpkgs {inherit system overlays;};
  in let
    mypython = pkgs.python39.withPackages (p: [
      p.olefile
      p.pandas
      p.natsort
    ]);
  in {
    devShell.x86_64-linux = pkgs.mkShell {
      nativeBuildInputs = [
        mypython
      ];
    };
  };
}
