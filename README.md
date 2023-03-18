# Chat on websockets
- Chat service for communicate written in Django + JS

## Feauters:
- Web Socket on channels
- Messages appear without site restart
- Answer on comments 
- Captha validation on create message
- Add txt , image files by websockets
- Preview image by clicking 
- Validate images format and text 
- Advansed filtering using FormSet
- Pagination
- Сaching main page ( 1 minute )

## Env variables sense: 
- POSTGRES_USER=your database username
- POSTGRES_PASSWORD=your database password
- POSTGRES_DB=your database name
- POSTGRES_HOST=select database image here
- POSTGRES_PORT=5432

## Installing using GitHub:
```python
git clone https://github.com/DevSpaciX/spa_chat.git
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
docker-compose up
```
## Getting access:
- Registration on site
### Admin data:
- If you want to access by admin user - just login by this data ```Login:adminuser Password:admin```
