
set -x
screen -dmS clock bash -c "cd /home/saujix/clock/ &&  source venv/bin/activate && python3 clock.py"
