Why I Chose to Develop the Web-Based Movie Discovery and Management System
The inspiration for my web-based movie discovery and management system stems from my coursework in CS 411, a software engineering class. While the project was not a requirement for my course, it provided a perfect opportunity to apply and extend the theoretical knowledge gained in class with practical, self-taught skills in HTML, CSS, JavaScript, and advanced Python. (This website is heavily based on HTML&Algorithm applied by Python)
As a co-founder of the Global Association, which aims to bridge cultural gaps, I recognized a significant opportunity to promote Chinese cinema—a rich, yet underrepresented facet of global culture. Many people outside of China are unfamiliar with the nuances of Chinese films and the deep cultural heritage they represent. This gap in cultural exchange sparked my motivation to use my software development skills to create a platform that not only introduces these films to a wider audience but also encourages interactive engagement through user comments and discussions.
Personally, I have a keen interest in war movies, which often carry profound historical significance and storytelling depth. By including a feature that allows users to write and share comments, the website fosters a community of movie enthusiasts who can exchange insights, recommendations, and cultural perspectives.
This project was my way of stepping beyond the classroom to make a tangible impact using the intersection of technology and culture. It not only allowed me to deepen my technical skills but also to contribute to cultural appreciation and understanding on a global scale.
Acknowledgments
I extend my heartfelt gratitude to the following institutions and their contributions, which have been instrumental in the development of my Web-Based Movie Discovery and Management System:
Tsinghua University Open Source Software Mirror Site (TUNA): My sincere thanks to Tsinghua University for providing a robust and reliable mirror site for Anaconda, a crucial tool in scientific computing and data analysis that supports my application's backend processing. The comprehensive access to updated repositories including conda-forge and pytorch, among others, significantly enhanced the development environment.
Massachusetts Institute of Technology (MIT): I am thankful for the MIT License under which I have used the "Hello, Flask!" framework. This license has facilitated a free and open-source approach, allowing me to modify and distribute the software needed for my project without restriction.







Project Technical Overview

Secure User Authentication: I integrated GitHub OAuth to authenticate users securely, which allowed for personalized user sessions and enhanced security. I managed user sessions with Flask, maintaining state across web requests.

Advanced Database Design: I designed and implemented a complex relational database schema in SQLite to efficiently handle data involving movies, users, categories, and reviews. My SQL expertise ensured robust data manipulation and integrity.

Dynamic API Development: I developed RESTful APIs that enabled real-time data interactions between the frontend and the database, supporting features like movie searches, managing favorites, and user reviews to boost engagement.

Responsive User Interface: I crafted the frontend using HTML5, CSS3, and JavaScript, focusing on a mobile-first design to ensure the application was accessible on various devices. My use of CSS for custom layouts and animations significantly enhanced the visual appeal and user experience.

Flask Template Rendering: I leveraged Flask’s templating engine to dynamically render web pages based on user interactions and data, seamlessly integrating backend logic with the frontend.

Session Management and Personalization: I configured Flask to effectively manage user sessions, which allowed for personalized content delivery like showing user-specific favorite movies and profile details.

Database Connectivity and Management: I engineered the database connectivity using SQLAlchemy, facilitating robust data management and manipulation. I automated repetitive database tasks such as migrations and seeding, which enhanced my development efficiency.

User Feedback and Interaction: I designed interactive elements such as movie favoriting and commenting systems using JavaScript and AJAX, providing instant feedback and interactive experiences without page reloads.
