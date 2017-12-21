# CS 440 MPs
Repo for CS440 MPs

## Running Python files

When running Python scripts in shell, remember to add the project root
(the one you're seeing right now) to `PYTHONPATH`. Like so:
```bash
export PYTHONPATH=$(pwd)
```
You can also add this line to the end of your `~/.bash_profile`
(`~/.bashrc` on Linux) so it will be automatically added to your environment
when shell starts.

## Notes on committing to GitHub

* Create a new branch from this branch: `git checkout -b {NAME}`
* Add all changes: `git add . -A`
* Commit changes: `git commit -m "Commit message"`
* Push to remote: `git push origin {branch}`
