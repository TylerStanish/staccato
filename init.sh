python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

export PYTHONPATH=`pwd`/music_server
read -p "Enter environment (development|production|testing):" FLASK_ENV
export FLASK_ENV
