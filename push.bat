call heroku plugins:install heroku-builds
call heroku builds:cancel
call heroku restart
call git add .
call git commit -m %1
call git push heroku master