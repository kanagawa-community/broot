# Preview hook for .github/scripts/render-previews.sh: broot runs in a headless
# tmux pane with each skin on this repository, with sizes and dates shown
# and a search typed, so the tree, file kinds, matches and status line show.
# Requires: broot, tmux, rsync, unshare.
# shellcheck shell=bash
name=broot

setup() {
  # broot shows the full path of its root, so it runs in its own mount namespace
  # with an empty /home that holds a copy with one timestamp. Owners are hidden.
  rsync -a --exclude=.git "$root"/ "$work/copy"/
  cat >"$work/run.sh" <<RUN
mount -t tmpfs none /home
d=/home/kanagawa-community/$(basename "$root")
mkdir -p "\$d"
cp -a "$work/copy/." "\$d"
find "\$d" -exec touch -h -d '2026-11-07 11:13' {} +
cd "\$d"
exec broot --conf "$work/skin.toml" -ds .
RUN
}

cleanup() {
  tmux -L kanagawa-preview kill-server 2>/dev/null || true
}

capture() {
  cleanup
  sleep 0.5
  cp "$root/themes/kanagawa-$1.toml" "$work/skin.toml"
  tmux -L kanagawa-preview new-session -d -s s -x 100 -y 24 -c "$work" \
    -e XDG_CONFIG_HOME="$work/cfg" -e COLORTERM=truecolor -e TERM=xterm-256color -e LC_ALL=C.UTF-8 \
    "unshare -Urm bash $work/run.sh"
  sleep 1.5
  tmux -L kanagawa-preview send-keys -t s -l "the"
  sleep 1
  tmux -L kanagawa-preview capture-pane -p -e -t s >"$2"
}
