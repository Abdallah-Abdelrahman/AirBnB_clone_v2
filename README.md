# AirBnB clone - The Console

<b>The project aims to deploy a fully-fledged and sophisticated, yet simple, copy of the [AirBnB](https://www.airbnb.com/)
website on our server.</b>

<figure>
    <img src="https://drive.google.com/uc?export=view&id=1sWCzpc7sIY0VCsEOpQDmJPS5q7weRhj-" alt="AirBnB fancy logo">
</figure>


## The Console:

A command interpreter to manipulate data without a visual interface (perfect for development and debugging).<br />

+ create data model.
+ manage (create, update, destroy, etc) objects via a console / command interpreter.
+ store and persist objects to a file (JSON file).

The first piece is to manipulate a powerful storage system. This storage engine
will give us an abstraction between “My object” and “How they are stored and persisted”.
This abstraction will also allow us to change the type of storage easily without updating all of our codebase.<br />

The console will be a tool to validate this storage engine as the figure:

<figure>
    <img src="https://drive.google.com/uc?export=view&id=1Nq8qsHpLmrY6hihJdZaRTjoJWWnXWL6C" alt="The console">
</figure>

## Project structure

```
├── AUTHORS
├── console.py
├── models
│   ├── amenity.py
│   ├── base_model.py
│   ├── city.py
│   ├── engine
│   │   ├── file_storage.py
│   │   ├── __init__.py
│   ├── __init__.py
│   ├── place.py
│   ├── review.py
│   ├── state.py
│   └── user.py
├── README.md
└── tests
    ├── test_console.py
    ├── test_init.py
    └── test_models
        ├── __init__.py
        ├── test_amenity.py
        ├── test_base_model.py
        ├── test_city.py
        ├── test_engine
        │   ├── __init__.py
        │   └── test_file_storage.py
        ├── test_place.py
        ├── test_review.py
        ├── test_state.py
        └── test_user.py
```

## Table of Contents 
1. [Class Hierarchy in AirBnB Backend System](#class-hierarchy-in-airbnb-backend-system)
2. [How to use The Console](#how-to-use-the-console)
3. [How to Install and Run The Console](#how-to-install-and-run-the-console)
4. [How to contribute to the project](#how-to-contribute-to-the-project)
5. [License](#license)

## Class Hierarchy in AirBnB Backend System
The AirBnB backend system employs a structured class hierarchy centered around the foundational `BaseModel` class. Derived classes, including `User`, `State`, `City`, `Amenity`, `Place`, and `Review`, represent distinct entities within the application, such as users, geographic locations, amenities, rental properties, and user reviews. This interconnected model forms the backbone of the backend, providing a systematic framework for managing and organizing essential data in the AirBnB platform.

## How to use The Console

The console is designed to interact with instances of different classes, providing essential CRUD operations (Create, Read, Update, Delete) along with additional functionalities. The supported commands include `create`, `show`, `destroy`, `all`, and `update`.


 ### 1. `create`

Creates a new instance of a specified class (e.g., `BaseModel`), **saves it to a JSON file**, and **prints the generated ID**. If the class name is missing or doesn't exist, appropriate error messages are displayed.

     $ create BaseModel


### 2. `show`

**Prints the string representation of an instance** based on the provided class name and ID. Error messages are displayed if the class name is missing, the class doesn't exist, the ID is missing, or no instance is found for the given ID.

    $ show BaseModel e7f9cac8-0f53-4fbd-9b42-68541032f2c2
    
### 3. `destroy`

**Deletes an instance based on the class name and ID,** saving the change into the JSON file. Error messages are displayed for missing class name, non-existent class, missing ID, or when no instance is found for the given ID.

    $ destroy BaseModel 1234-1234-1234

### 4. `all`

Prints the string representation of **all instances based on the provided class name** or **all instances if no class name is specified**. Error message is displayed if the class doesn't exist.

    $ all BaseModel
    $ all

### 5. `update`

**Updates an instance based on the class name and ID** by adding or updating an attribute. The change is saved into the JSON file. Only simple attributes (string, integer, and float) can be updated. Error messages are displayed for missing class name, non-existent class, missing ID, missing attribute name, or missing attribute value.

    $ update BaseModel 1234-1234-1234 email "aibnb@mail.com"

### Rules and Assumptions:

-   Arguments are assumed to be in the correct order.
-   Each argument is separated by a space.
-   String arguments with spaces must be enclosed in double quotes.

Feel free to explore the capabilities of the console and manage instances seamlessly.

## How to Install and Run The Console

To install and run the AirBnB clone - The Console project, follow these simple steps:

### 1- Clone the Repository:
Clone the project repository from GitHub using the following command in your terminal:

    $ git clone https://github.com/Abdallah-Abdelrahman/AirBnB_clone.git

### 2- Navigate to Project Directory:
Change into the project directory:

    $ cd AirBnb_clone
    
### 3- Run the Console:
The console, which interacts with the backend system, can be executed using the following command:

    $ ./console

### 4- Explore Commands
Once the console is running, explore the available commands such as `create`, `show`, `destroy`, `all`, and `update` as outlined

    $ create BaseModel

### 5- Interact with the Backend:
Utilize the provided classes (`User`, `State`, `City`, `Amenity`, `Place`, and `Review`) to manage entities within the AirBnB system. Follow the described rules and functionalities to create, read, update, and delete instances.

## How to contribute to the project

We welcome contributions from the community to enhance the AirBnB clone project. Here's how you can contribute:
Fork the Repository, clone your forked repository to your local machine, and implement your changes and improvements in the code. Ensure that your modifications align with the project's coding standards, and eventually open a pull request from your fork to the original repository. Provide a detailed description of your changes and improvements.
And once your contribution is reviewed and approved, it will be merged into the main project. Congratulations on your successful contribution!

## License 
The AirBnB clone project is open-source and released under the MIT License. This license grants permission to anyone to use, modify, and distribute the software, subject to the conditions outlined in the license agreement.
