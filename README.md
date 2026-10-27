# rpm-packages

[![ci](https://github.com/Giftpilz0/rpm-packages/actions/workflows/ci.yml/badge.svg)](https://github.com/Giftpilz0/rpm-packages/actions/workflows/ci.yml)
[![copr](https://github.com/Giftpilz0/rpm-packages/actions/workflows/update.yml/badge.svg)](https://github.com/Giftpilz0/rpm-packages/actions/workflows/update.yml)
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Spec files for Fedora packages built on COPR [giftpilz0/misc](https://copr.fedorainfracloud.org/coprs/giftpilz0/misc/):
matugen-git, niri-git, waypipe-git.

## Usage

```sh
sudo dnf copr enable giftpilz0/misc
sudo dnf install niri-git
```

## Development

`update.yml` updates the specs daily and triggers the COPR builds. Locally: `just update` (specs),
`just build` (mock), `just deploy` (trigger COPR, needs `COPR_WEBHOOK_ID` and `COPR_WEBHOOK_UUID`).
Run `just` for all recipes and `just check` before committing. Conventions: [Giftpilz0/shared](https://github.com/Giftpilz0/shared).

## License

The spec files and scripts are [MIT](LICENSE). The packaged software keeps its own license
(`License:` in each spec).
