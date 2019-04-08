# Restaurant Catalog
Best restaurants in Calgary by cuisines. Used trello for project management; https://trello.com/b/gxybDdor

## Database design
database setup script sets up a new database with some initial data. inser UML image here.

## Getting Started

Instructions to run a copy of this on your machine.

### Prerequisites

Python sqlalchemy. copy of cagrant

### Installing

You can install psql and python on your system or use a VM that already has these installed. (Recommended to use Vagrant as VM, you can use [this Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm/blob/master/vagrant/Vagrantfile) provided by Udacity to set up your virtual machine with a blank news database)

Download the project from github and create a folder named "LogAnalysis" and unzip the files.
Next, download the data for news database [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). You will need to unzip this file after downloading it. The file inside is called newsdata.sql. Put this file into the "LogAnalysis" folder you just created.

To load the data, cd into the vagrant directory and use the command below (Make sure you have a blank news database if you didn't use the Vagrantfile above)
```
psql -d news -f newsdata.sql
```

Here's what this command does:
```
psql — the PostgreSQL command line program

-d news — connect to the database named news (created by the vagrantfile, or by you if you are not using a VM)

-f newsdata.sql — run the SQL statements in the file newsdata.sql
```

Running this command will connect to your installed database server and execute the SQL commands in the downloaded file, creating tables and populating them with data. After this is completed go into the "LogAnalysis" folder on your console and type the command below to run the report;
```
python3 logs.py
```

## References / Authors

* **Kaan Eroglu** - *Initial work* - [kaan.ca](https://www.kaan.ca)
* **Udacity FSND Instructions** - *Installation instructions*


## License

This project is licensed under the MIT License 

## Acknowledgments

* Udacity mentors

