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
- Important ! If you want to create chat with admin credentionals DON`t Forget to add image on user profile via /admin/site -> choose image 

## Screenshots:
![image](https://user-images.githubusercontent.com/102595649/226098831-abf7479b-cb6f-4602-8d23-cd387e560b65.png)
![image](https://user-images.githubusercontent.com/102595649/226098889-9c378c17-90c0-4a73-8edf-725a7458e1a5.png)
![image](https://user-images.githubusercontent.com/102595649/226098928-366e10de-f2eb-4fd5-886c-ec58dedbde07.png)
![image](https://user-images.githubusercontent.com/102595649/226099560-17733194-defe-47ce-b1d2-90b17b9b4c77.png)
![image](https://user-images.githubusercontent.com/102595649/226099830-318ce8c8-e0a3-4cd6-8995-46286c0ff730.png)
![image](https://user-images.githubusercontent.com/102595649/226103300-df6ee408-0c4b-47f1-a7f9-e42233699ddd.png)


