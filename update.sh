#!/usr/bin/env bash
set -euo pipefail

# Packages to update: "name platform owner_or_project spec_file package_type"
# - platform: github | gitlab
# - package_type: release | git
packages=(
  "eww-git github elkowar/eww SPECS/eww-git/eww-git.spec git"
  "matugen-git github InioX/matugen SPECS/matugen-git/matugen-git.spec git"
  "niri-git github niri-wm/niri SPECS/niri-git/niri-git.spec git"
  "quickshell-git github quickshell-mirror/quickshell SPECS/quickshell-git/quickshell-git.spec git"
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
    fi
  else
    echo "[✘] Could not fetch latest tag"
  fi

  # For git packages: update commit0 and commitdate
  if [ "$type" = "git" ]; then
    # Get the default branch dynamically
    if json_repo="$(curl -fsSL "$api" 2>/dev/null)" && [ -n "$json_repo" ]; then
      case "$platform" in
        github) def_branch="$(echo "$json_repo" | jq -r '.default_branch // "main"')" ;;
        gitlab) def_branch="$(echo "$json_repo" | jq -r '.default_branch // "master"')" ;;
      esac
    else
      # Fallback
      case "$platform" in
        github) def_branch="main" ;;
        gitlab) def_branch="main" ;;
      esac
    fi

    echo "[ℹ] Using default branch: $def_branch"

    case "$platform" in
      github) commits_url="$api/commits?sha=$def_branch&per_page=1"; commit_field='.[0].sha'; date_field='.[0].commit.committer.date' ;;
      gitlab) commits_url="$api/repository/commits?ref_name=$def_branch&per_page=1"; commit_field='.[0].id'; date_field='.[0].committed_date' ;;
    esac

    if json_commits="$(curl -fsSL "$commits_url" 2>/dev/null)" && [ -n "$json_commits" ]; then
      newCommit="$(echo "$json_commits" | jq -r "$commit_field // empty")"
      newCommitDate="$(echo "$json_commits" | jq -r "$date_field // empty" | cut -d'T' -f1 | tr -d '-')"

      if [ -n "$newCommit" ]; then
        sed -Ei 's@^(%global|%define) commit0 .*@\1 commit0 '"$newCommit"'@' "$spec"
        echo "[✔] Set commit0 to $newCommit on branch $def_branch"
      fi

      if [ -n "$newCommitDate" ]; then
        sed -Ei 's@^(%global|%define) commitdate .*@\1 commitdate '"$newCommitDate"'@' "$spec"
        echo "[✔] Set commitdate to $newCommitDate"
      fi

    else
      echo "[✘] Could not fetch latest commit from branch $def_branch"
    fi
  fi
done

echo -e "\n======================================="
echo "Spec update run complete"
echo "======================================="
