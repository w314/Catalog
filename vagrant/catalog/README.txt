# Catalog App

## Description

The app is a catalog with different categories. Users can add, edit or delete items they added to the cagetories after logging in. All visitors can view categories and items in categories. All can reach the details in json format too.

## Setup

1. Install **VirtualBox**.
    Virtaul Box will run your virtaul machine. [You can download it here.](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
1. Install **Vagrant**.
    Vagrant will configure the virtual machine. [You can download it here.](https://www.vagrantup.com/downloads.html.)
1. Run the virtual machine. In your terminal change directory to fullstack/vagrant and run `vagrant up`.
1. Log into the virtual machine with `vagrant ssh`
2. Change directory to /vagrant with `cd /vagrant/catalog`.
3. Set up the database by running `python catalog_db_setup.py`.
4. Populate the database by running `python populate_catalog_db.py`.
5. Run the database by running 'python catalog.py'.
6. To use the app open your browser and go to `localhost:8000'

## Instructions
### To view all categories
Visit the home page by going to `localhost:8000'. The home page here will show you all the categories and the last 1o added items. You can always return to the home page by pressing the home page button in the top left corner of any page.

### To view a specific category
Go to the home page by clicking the home page button at the top left corner of the page.
Click on the name of the category you'd like to see. It will take you to a category page that shows all the items in that category.

### To vew a specific item
Click on the name of the item either on the home page or any category page.

### To log into the app
To add, edit or delete an item you have to log in. You have to have a google id to log in. If you don't have one [you can create onehere](https://www.google.com/). To log in press the login button in the top right corner of the page. It will take you to google where you can safely sign in.

### To log out
To log out press the log-out button in the top right corner of the page.

### To add an item
To create a new item in the catalog use the "+ New Item" button on the home page or any category page. Be creative with your items name. Categories are not allowed to have two item with the same name.:)

### To edit an item
Users can only edit items they have created. To edit an item either click on it on the home page and use the edit button when the item is displayed or go to it's category page and use the edit button you find next to the item's name.

### To delete an item
Users can only delete items they have created. To delet an item either click on it on the home page and use the delete button when the item is displayed or go to it's category page and use the delete button you find next to the item's name. 


## Attribution

The app uses Google's OAuth API for the user sign-in.
Udacity provided the configuration of the virtual machine.