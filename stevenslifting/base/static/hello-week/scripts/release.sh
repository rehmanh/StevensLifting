set -e
echo "Current version:" $(grep version package.json | sed -E 's/^.*"(4[^"]+)".*$/\1/')
echo "Enter release version: "
read VERSION

read -p "Releasing v$VERSION - are you sure? (y/n)" -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
  echo "Releasing v$VERSION ..."

  npm run test
  npm run lint:js

  npm run build
  # generate the version so that the changelog can be generated too
  npm version --no-git-tag-version --no-commit-hooks --new-version $VERSION

  # changelog
  npm run changelog

  echo "Please check the git history and the CHANGELOG and press enter"
  read OKAY

  # commit and tag
  git add CHANGELOG.md package.json
  git commit -m "chore(release): v$VERSION"
  git tag "v$VERSION"

  # commit
  npm publish --tag next --new-version "$VERSION" --no-commit-hooks --no-git-tag-version

  # publish
  git push origin refs/tags/v$VERSION
  git push
fi
