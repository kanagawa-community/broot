#!/usr/bin/env bash
# Install the Kanagawa themes for broot: every variant, or only the ones named.
# ./uninstall.sh takes the same arguments and removes them again.
#
# Usage: ./install.sh [all|wave|dragon|lotus ...]
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
config="${XDG_CONFIG_HOME:-$HOME/.config}"
# Print "<file in this repository>\t<folder it goes in>" for one variant.
items() { printf "themes/kanagawa-%s.toml\t%s\n" "$1" "$config/broot/skins"; }
after() { :; }

uninstall=false
if [[ "${1:-}" == --uninstall ]]; then
  uninstall=true
  shift
fi
selected=""
add() { case " $selected " in *" $1 "*) ;; *) selected="$selected $1" ;; esac; }
for arg in "${@:-all}"; do
  case "$arg" in
    all) add wave; add dragon; add lotus ;;
    wave | dragon | lotus) add "$arg" ;;
    *) echo "usage: $0 [all|wave|dragon|lotus ...]" >&2; exit 2 ;;
  esac
done

for v in $selected; do
  # Remove first, so a reinstall drops files the repository no longer has.
  while IFS=$'\t' read -r src dir; do
    rm -rf "${dir:?}/$(basename "$src")"
    if [[ "$uninstall" == false ]]; then
      mkdir -p "$dir"
      cp -R "$src" "$dir/"
    fi
  done < <(items "$v")
  [[ "$v" == shared ]] && continue
  if [[ "$uninstall" == true ]]; then echo "Removed kanagawa-$v"; else echo "Installed kanagawa-$v"; fi
done
after
