# request-constraints

tests request constraints logic

## Run example web app

Requires Python 3.8 with conda:

```bash
conda create --name constraints python=3.8
conda install -c conda-forge tranquilizer
conda install -c conda-forge werkzeug==2.1.2
```

Open a shell and type:

```bash
make api_server
```

Open another shell and type:

```bash
make web_app
```

Now you should have two servie running:

- a Web application on http://locahost:8085
- a REST API server on <http://locahost:8086>

Open the browser on <http://locahost:8085> (or type `make open`).
