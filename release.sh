version=`python setup.py --version`
python setup.py compile_catalog
git tag $version
git push --tags
python setup.py bdist_wheel upload
