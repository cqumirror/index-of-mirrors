Index of Mirror Site
===
A new back-end and new web pages of CQU Mirror Site.

##Features
###Web Pages
- [x] A list of entrances of all the mirrors.
- [x] Give a glance at sync-states of all the mirrors.
- [x] An entrance to quickly download some system isos or softwares.
- [ ] A list of some flows of server, like network-io...
- [x] Have better compatibility. Mobile support.

###Back End
- [x] Provide RESTful API for front-end to operate resources.
- [ ] Publish notices or news via github issue.
- [ ] Update mirrors, resources list via github issue.
- [ ] Auto backup database: dump database into json files and push to github with some rules, such as backup after each successful issue submit.

##Organization
- `actor/`: Flask APP sits here. **Actor** is the APP's name.
 - `domains.py`: Some data objects.
 - `views.py`: Routers and its implementation.
 - `static/`: Web pages are here!
 - `run_actor.py`: For debugging. Just `./run_actor.py` in the CLI.

##Quick Start for Dev.
It's free to try your ideas.
- Change into the project directory. Everything happens in it.
- Initialize a virtualenv with the command `virtualenv .pyenv && .pyenv/bin/pip install --upgrade -r requirements.txt --allow-external mysql-connector-python`.
- Create a database and restore it with `schema.sql`. We use `MariaDB` in production.
- Custom a `settings.cfg` with a copy of `example_settings.cfg`.
- Run the APP with the command `./run_actor.py` or `.pyenv/bin/python run_actor.py`.
- To know details of API, see [here](docs/mirror-site-api.md).
- To know details of web pages' description, see
 - [index](docs/mirror-site-web-pages-index.md)

##How to Deploy
`fab -u user -H host --port=port <pull|deploy|start>`

##License
MIT, see `LICENSE` for details.

