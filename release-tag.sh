version=`python setup.py --version`
eval "$(ssh-agent -s)" #start the ssh agent
chmod 400 ./openfisca_bot
ssh-add ./openfisca_bot
git remote set-url origin git@github.com:openfisca/openfisca-france.git
git tag $version
git push --tags
