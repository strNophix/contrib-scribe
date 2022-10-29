# contrib-scribe
Your contribution heatmap is a canvas for creativity.

## Prerequisites
- systemd
- python (>=3.10)
- git

## Usage
```sh
# Start
cp config.ini.sample config.ini

./scripts/install.sh
# or manually without systemd
python content_scribe.py config.ini

# Stop
./scripts/uninstall.sh
```
