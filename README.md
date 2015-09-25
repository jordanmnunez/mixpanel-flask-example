# Mixpanel Server Side Example

Using flask, you will be able to build a simple server side implementation
This will go to the mixpanel-flash project (760063)

## Library Dependencies

Flask:
```bash
pip install flask
```
mixpanel:
```bash
pip install mixpanel
``` 

## SME Practical Task List

1. Implement Log-In functions
  * check 'DB' to see if user already exists (dont worry about pasword, only ask for email)
  * track a log-in incremental function, update their last seen
    - Don't forget about IP
  * pass user information through to the home.html page so that JS can identify
    - what do you do when someone registers vs logs in??
2. Remeber their Genre
  * track and store their favourite genre to the 'DB'
  * create a customized homepage with a song relating to their favourite genre
  * track a song play of this dynamic song 
