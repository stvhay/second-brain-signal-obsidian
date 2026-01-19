{
  description = "Second Brain development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    cherri.url = "github:electrikmilk/cherri";
  };

  outputs = { self, nixpkgs, cherri }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
    in
    {
      devShells = forAllSystems (system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in
        {
          default = pkgs.mkShell {
            buildInputs = with pkgs; [
              python3
              python3Packages.jinja2
              cherri.packages.${system}.default
              graphviz
              mermaid-cli
            ];

            shellHook = ''
              # Block direct nix develop usage, except in CI or direnv contexts
              # CI systems (GitHub Actions) set CI=true
              # DIRENV_IN_ENVRC is set when direnv is evaluating the .envrc
              if [ -z "$CI" ] && [ -z "$DIRENV_IN_ENVRC" ] && [ ! -t 0 ]; then
                echo "❌ ERROR: Direct nix develop usage is not supported."
                echo ""
                echo "This project uses direnv for environment management."
                echo "Please use your shell base environment with direnv."
                echo ""
                exit 1
              fi
            '';

          };
        });
    };
}
