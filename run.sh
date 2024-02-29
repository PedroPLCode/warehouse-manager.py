[ -d "$HOME/.local/bin" ] && PATH="$HOME/.local/bin:$PATH"
export PATH
export FLASK_ENV=development
flask run --debug --port 5000