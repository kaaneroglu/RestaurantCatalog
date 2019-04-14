# Restaurant Catalog
Best restaurants in Calgary by cuisines. 
This application uses Flask to demonstrate CRUD functionality on a sqlite database.
Used trello for project management; https://trello.com/b/gxybDdor

## Database design
db_setup.py sets up a new database with some initial data. If you want to start with a fresh database, delete "yycrestaurants.db" and run this db_setup code first. Alternatively, you can use the database that's included here as is.
![vagrant --version](https://trello-attachments.s3.amazonaws.com/5caab4d54719c833bde0d5e0/946x486/1fea2f09e0853f3d04895b5504bc185d/database.jpg)
## Getting Started

Instructions to run a copy of this on your machine.

### Prerequisites

Virtualbox and vagrant with sqlalchemy and python libraries. Please see instructions at https://github.com/udacity/fullstack-nanodegree-vm#installation to get your environment setup.

### Installing

Once you have the Vagrant up and running, copy this project (or clone with git) into /vagrant/catalog/ and run the application by typing 
`python3 catalog.py`

### JSON Endpoints
For example;
* http://localhost:5000/cuisines/3/JSON (gets all restaurants under cuisine with id=3)
* http://localhost:5000/cuisines/3/restaurant/1/JSON (get the specified restaurant with restaurant_id=1)

## References / Authors

* **Kaan Eroglu** - *Initial work* - [kaan.ca](https://www.kaan.ca)
* **Udacity FSND Instructions** - *Installation instructions*


## License

This project is licensed under the MIT License 

## Acknowledgments

* Udacity mentors

