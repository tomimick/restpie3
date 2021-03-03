# this is /etc/profile
# - a login script when running the interactive shell inside the container

export PYTHONPATH=/app/py
export PYSRV_CONFIG_PATH=/app/conf/server-config.json
export FLASK_ENV=development
alias l='ls'
alias ll='ls -l'

