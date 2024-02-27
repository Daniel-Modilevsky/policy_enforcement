# Policy Enforcement Assessment

This repository contains a simple HTTP API server application written in Python that...

## API Endpoints

- GET '/get' - returns the current counter value, 0 by default.
- POST '/increase' - adds 1 to the counter value and returns it.



### Running the Application
The application is dockerized and can be easily run using docker-compose.

Run the following command to start the API server:

```bash
- Clone the repository to your local machine.

- Get the .env file for the connection string params (from author).

- Open a terminal window and navigate to the root directory of the cloned repository.

  $ docker-compose up
  
- This command will start the application server and the database. 
- Open the browser and navigate to http://localhost:5050.

python3 -m venv venv
. venv/bin/activate
```

