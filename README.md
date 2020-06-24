heroku login

cd $APP_NAME

git init
git add .
git commit -m "wip"

heroku apps:create $APP_NAME-server
heroku addons:create heroku-postgresql --app $APP_NAME-server
heroku apps:create $APP_NAME-client --buildpack mars/create-react-app

git remote -v

git remote add heroku-server https://git.heroku.com/$APP_NAME-server.git
git remote add heroku-client https://git.heroku.com/$APP_NAME-client.git

git subtree push --prefix server heroku-server master
git subtree push --prefix client heroku-client master

heroku logs --tail --app $APP_NAME-server
heroku logs --tail --app $APP_NAME-client

// Redeploy
git add .
git commit -m "wip"
git subtree push --prefix server heroku-server master
git subtree push --prefix client heroku-client master

git remote rm remote-name