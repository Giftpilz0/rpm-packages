#!/usr/bin/env bash
set -euo pipefail

# Packages to update: "name platform owner_or_project spec_file package_type"
# - platform: github | gitlab
# - package_type: release | git
packages=(
  "eww-git github elkowar/eww SPECS/eww-git/eww-git.spec git"
  "hyprgraphics github hyprwm/hyprgraphics SPECS/hyprgraphics/hyprgraphics.spec release"
  "hypridle github hyprwm/hypridle SPECS/hypridle/hypridle.spec release"
  "hyprland-protocols github hyprwm/hyprland-protocols SPECS/hyprland-protocols/hyprland-protocols.spec release"
  "hyprland-qt-support github hyprwm/hyprland-qt-support SPECS/hyprland-qt-support/hyprland-qt-support.spec release"
  "hyprlang github hyprwm/hyprlang SPECS/hyprlang/hyprlang.spec release"
  "hyprlock github hyprwm/hyprlock SPECS/hyprlock/hyprlock.spec release"
  "hyprpaper github hyprwm/hyprpaper SPECS/hyprpaper/hyprpaper.spec release"
  "hyprutils github hyprwm/hyprutils SPECS/hyprutils/hyprutils.spec release"
  "hyprwayland-scanner github hyprwm/hyprwayland-scanner SPECS/hyprwayland-scanner/hyprwayland-scanner.spec release"
  "matugen-git github InioX/matugen SPECS/matugen-git/matugen-git.spec git"
  "niri-git github YaLTeR/niri SPECS/niri-git/niri-git.spec git"
  "waypipe-git gitlab mstoeckl%2Fwaypipe SPECS/waypipe-git/waypipe-git.spec git"
  "yolk-git github elkowar/yolk SPECS/yolk-git/yolk-git.spec git"
)

echo -e "\n======================================="
echo "Updating RPM spec files from GitHub/GitLab"
echo "======================================="

for entry in "${packages[@]}"; do
  read -r name platform repo spec type <<< "$entry"

  echo -e "\n--- Processing $name"
  [ ! -f "$spec" ] && { echo "[✘] Spec file not found: $spec"; continue; }

  case "$platform" in
    github) api="https://api.github.com/repos/$repo" ;;
    gitlab) api="https://gitlab.freedesktop.org/api/v4/projects/$repo" ;;
    *) echo "[✘] Unknown platform: $platform"; continue ;;
  esac

  case "$platform" in
    github) tags_url="$api/tags?per_page=1" ;;
    gitlab) tags_url="$api/repository/tags?per_page=1" ;;
  esac

  if json_tags="$(curl -fsSL "$tags_url" 2>/dev/null)" && [ -n "$json_tags" ]; then
    tag_name="$(echo "$json_tags" | jq -r '.[0].name // empty')"
    newTag="${tag_name#v}"

    if [ -n "$newTag" ]; then
      sed -Ei "s/^(Version:[[:space:]]*)[^%[:space:]]+/\1${newTag}/" "$spec"
      echo "[✔] Set Version to $newTag"

      if [ "$type" = "release" ]; then
        sed -Ei 's/^(Release:[[:space:]]*)[0-9]+/\11/' "$spec"
        echo "[✔] Reset Release to 1"
      fi
    fi
  else
    echo "[✘] Could not fetch latest tag"
  fi

  # For git packages: update commit0 and reset bumpver
  if [ "$type" = "git" ]; then
    def_branch="main"
    [ "$platform" = "gitlab" ] && def_branch="master"

    case "$platform" in
      github) commits_url="$api/commits?sha=$def_branch&per_page=1"; commit_field='.[0].sha' ;;
      gitlab) commits_url="$api/repository/commits?ref_name=$def_branch&per_page=1"; commit_field='.[0].id' ;;
    esac

    if json_commits="$(curl -fsSL "$commits_url" 2>/dev/null)" && [ -n "$json_commits" ]; then
      newCommit="$(echo "$json_commits" | jq -r "$commit_field // empty")"

      if [ -n "$newCommit" ]; then
        sed -Ei 's@^([[:space:]]*%[[:space:]]*(global|define)[[:space:]]+commit0[[:space:]]+)[0-9a-fA-F]{7,40}([[:space:]]*)(#.*)?$@\1'"$newCommit"'\3\4@' "$spec"
        echo "[✔] Set commit0 to $newCommit on branch $def_branch"
      fi
    else
      echo "[✘] Could not fetch latest commit"
    fi

    sed -Ei 's/^(bumpver[[:space:]]*)[0-9]+/\1 0/' "$spec"
    echo "[✔] Reset bumpver to 0"
  fi
done

echo -e "\n======================================="
echo "Spec update run complete"
echo "======================================="
