#!/usr/bin/env python3
"""Write themes/kanagawa-<variant>.toml (broot skins) from the shared palette.

Usage: scripts/generate.py [path/to/palette.json]   (default: ../.github/palette.json)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VARIANTS = ["wave", "dragon", "lotus"]

# broot skin entry -> (fg role, bg role, attribute). None is the terminal default.
SKIN = {
    "tree": ("ui.nontext", None, ""),
    "file": (None, None, ""),
    "directory": ("syn.fun", None, "bold"),
    "exe": ("term.green", None, ""),
    "link": ("term.cyan", None, ""),
    "pruning": ("ui.nontext", None, "italic"),
    "perm__": ("ui.nontext", None, ""),
    "perm_r": ("syn.constant", None, ""),
    "perm_w": ("vcs.removed", None, ""),
    "perm_x": ("term.green", None, ""),
    "owner": ("ui.nontext", None, ""),
    "group": ("ui.nontext", None, ""),
    "dates": ("syn.comment", None, ""),
    "sparse": (None, None, ""),
    "git_branch": ("ui.special", None, ""),
    "git_insertions": ("vcs.added", None, ""),
    "git_deletions": ("vcs.removed", None, ""),
    "git_status_current": (None, None, ""),
    "git_status_modified": ("vcs.changed", None, ""),
    "git_status_new": ("vcs.added", None, ""),
    "git_status_ignored": ("ui.nontext", None, ""),
    "git_status_conflicted": ("diag.error", None, ""),
    "git_status_other": ("diag.error", None, ""),
    "selected_line": (None, "ui.bg_p2", ""),
    "char_match": ("syn.string", None, "underlined"),
    "file_error": ("diag.error", None, "italic"),
    "flag_label": (None, None, ""),
    "flag_value": ("syn.constant", None, "bold"),
    "input": (None, None, ""),
    "status_error": ("diag.error", "ui.bg_m3", ""),
    "status_job": ("ui.special", "ui.bg_m3", "bold"),
    "status_normal": (None, "ui.bg_m3", ""),
    "status_italic": ("syn.constant", "ui.bg_m3", ""),
    "status_bold": ("ui.special", "ui.bg_m3", "bold"),
    "status_code": ("ui.special", "ui.bg_m3", ""),
    "status_ellipsis": (None, "ui.bg_m3", ""),
    "scrollbar_track": ("ui.bg_p1", None, ""),
    "scrollbar_thumb": ("ui.nontext", None, ""),
    "help_paragraph": (None, None, ""),
    "help_bold": ("ui.special", None, "bold"),
    "help_italic": ("ui.special", None, "italic"),
    "help_code": ("ui.special", "ui.bg_p1", ""),
    "help_headers": ("syn.fun", None, ""),
    "help_table_border": ("ui.nontext", None, ""),
    "preview_title": ("ui.fg_dim", "ui.bg", ""),
    "staging_area_title": ("ui.fg_dim", "ui.bg", ""),
}
# Disk use, from free to full. The palette has no gradient, so each third of
# the scale takes one diagnostic role.
GOOD_TO_BAD = ["diag.ok"] * 4 + ["diag.warning"] * 3 + ["diag.error"] * 3
SKIN |= {f"good_to_bad_{i}": (role, None, "") for i, role in enumerate(GOOD_TO_BAD)}


def roles(variant):
    """Map each role to its hex color; a role missing from the palette raises KeyError later."""
    return {role: c["hex"] for c in variant["colors"].values() for role in c["usage"]}


def rgb(h):
    return "rgb(" + ", ".join(str(int(h[i : i + 2], 16)) for i in (1, 3, 5)) + ")"


def theme(variant, colors):
    def color(role):
        return rgb(colors[role]) if role else "none"

    out = [f"# Kanagawa {variant.capitalize()}", "# https://github.com/kanagawa-community/broot", "", "[skin]"]
    out.append(f'default = "{color("ui.fg")} {color("ui.bg")} / {color("ui.fg_dim")} {color("ui.bg")}"')
    for key, (fg, bg, attr) in SKIN.items():
        out.append(f'{key} = "{" ".join(x for x in (color(fg), color(bg), attr) if x)}"')
    return "\n".join(out) + "\n"


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / ".github" / "palette.json"
    variants = json.loads(path.read_text())["variants"]
    for v in VARIANTS:
        out = ROOT / "themes" / f"kanagawa-{v}.toml"
        out.parent.mkdir(exist_ok=True)
        out.write_text(theme(v, roles(variants[v])))
        print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
