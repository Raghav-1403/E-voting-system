# E-voting system using Django
This project is about e-voting system using django and a centralized blockchain system. It can be further improved by maintaining a seperate database at the miners end which could provide us with a decentralized blockchain system. It consits of django-tenants which will be useful for create a unique domain for every creators in the system. 

Installations and requirments

The Python and pip should be installed

The Django and Django-tenants can be installed using the command

```bash
  pip install django django-tenants
```

For database the postgresql
  To install the database

```http
  https://www.postgresql.org/download/
```

In postgresql create user and mention in the src/exp/settings.py file
![image](https://github.com/Raghav-1403/E-voting-system/assets/116968337/5bb0455c-b07d-4b0d-81fb-ba00654827ae)

Now you have to apply these commands in the terminal

```bash
  cd exp
  cd src
```
```bash
  python manage.py makemigrations
```
```bash
  python manage.py migrate
```
To run
```bash
  python manage.py runserver
```
Now you can access your website in localhost or 127.0.0.1 with a host mentioned in the terminal
![Screenshot (47)](https://github.com/Raghav-1403/E-voting-system/assets/116968337/5ad59bde-bb6d-476a-8ae0-e0670cef8d13)





The project home page
![Screenshot 2023-12-16 002239](https://github.com/Raghav-1403/E-voting-system/assets/116968337/ed17d3e0-369f-4532-9f2c-48d6175b0ae0)

There are three different roles in the system which are Creator, Voter and Miner

Creator-Used to create the voters list under a organization name. The voters and miners will be intialized by the creators. (The future enhancment could randomly generating miners to the creators).

Voters-Used to vote to a person or a party under the name of organization. The user has restricted acess. The hash value will be generated against the vote.

Miner-The miner works differently here the miner uses to find out the name of the candidate from the hash value, Which is similar to password cracking in hash. The miner will run with every party or member and find out the exact party from the hash.

Creator Page(demo):


Voter Page(demo):


Miner Page(demo):




