# Statistics

UCU statistics coursework, organized like the linear algebra repository:

- `labs/task1/`: Task 1 assignment and starter notebooks
- `workshops/`: workshop exercises

## Environment setup

Use Python 3.12 or newer and one virtual environment at the repository root:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m ipykernel install --sys-prefix --name statistics-ucu --display-name "Python (.venv: statistics-ucu)"
```

To reproduce the initially installed versions, use `requirements-lock.txt` instead.
On each new terminal session, run `source .venv/bin/activate`.

## Task 1

```sh
source .venv/bin/activate
jupyter lab labs/task1
```

Select **Python (.venv: statistics-ucu)**. See [Task 1](labs/task1/README.md)
for the assignment outline. Notebooks contain setup code and TODO sections;
complete the exercises and explanations before submission.

## Personal Git identity

Origin uses `git@github-personal:hryhola/statistics-ucu.git`.
This checkout locally configures Vladyslav Hryhola <vladyslav.hryhola@gmail.com>,
the personal SSH key, and personal SSH commit signing. These local settings
are not transferred by cloning; configure them again on another checkout.
Global Git settings are left unchanged.
