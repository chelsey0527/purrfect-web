# Visualized ToDoList

## Introduction
The Visualized ToDoList is a modern web application designed to help users manage their tasks more effectively. With a visually appealing interface and intuitive user experience, this app goes beyond traditional to-do lists. The project is structured with a detached frontend and backend to promote scalability, easier maintenance, and better performance.

## Features
- Create, update, and delete tasks.
- Visual representation of tasks for easier prioritization.
- Responsive design for desktop and mobile use.
- Authentication system to secure user data.

## Technologies Used
- **Frontend:** Streamlit
- **Backend:** Flask, PostgresQL

## Getting Started

## Backend
```
python -m venv venv             
source venv/bin/activate        
pip install -r requirements.txt 
```

## Frontend
```
streamlit run app.py
```

## Contribution
Contributions are welcome! Please read the contribution guidelines for the process for submitting pull requests to us.

## Reflection
Reflecting on the development of the Visualized ToDoList, it's clear that separating the frontend and backend was a strategic decision that offered flexibility and a clear separation of concerns. This architecture not only facilitated independent development and testing of each part but also allowed us to incorporate a variety of technologies that were best suited for their respective tasks. One of the challenges encountered was ensuring seamless communication and data synchronization between the frontend and backend. However, through effective API design and state management practices, we were able to overcome these hurdles, resulting in a robust and user-friendly application.

### Future Directions
Moving forward, we aim to introduce more interactive features, such as drag-and-drop task prioritization, and expand our authentication system to support multiple user roles. Our experience with the Visualized ToDoList has been immensely rewarding, and we look forward to seeing how it evolves with contributions from the community.