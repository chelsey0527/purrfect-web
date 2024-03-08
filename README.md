# Visualized ToDoList

## Introduction
The Visualized ToDoList is a modern web application designed to help users manage their tasks more effectively with a visually appealing interface and intuitive user experience.
[VISIT SITE](https://techin510-final-frontend.azurewebsites.net/)
[DEMO VIDEO](https://youtu.be/NP9R93W7f40)

## Features
- Create, update, and delete tasks.
- Visual representation of tasks for easier prioritization.
- Authentication system to secure user data.

## Technologies Used
- **Frontend:** Streamlit
- **Backend:** Flask, PostgresQL

## Getting Started

### Backend
```
python -m venv venv             
source venv/bin/activate        
pip install -r requirements.txt 
```

### Frontend
```
streamlit run app.py
```

## Reflection
Reflecting on the development of the Visualized ToDoList, it's clear that separating the frontend and backend was a strategic decision that offered flexibility and a clear separation of concerns. This architecture not only facilitated independent development and testing of each part but also allowed us to incorporate a variety of technologies that were best suited for their respective tasks. One of the challenges encountered was ensuring seamless communication and data synchronization between the frontend and backend. However, through effective API design and state management practices, we were able to overcome these problems, resulting in a robust and user-friendly application.

### Future Directions
Moving forward, we aim to introduce more interactive features, such as drag-and-drop task prioritization, and expand our authentication system to support multiple user roles. Our experience with the Visualized ToDoList has been immensely rewarding, and we look forward to seeing how it evolves with contributions from the community.

