set shell := ["zsh", "-cu"]
set dotenv-load

python_dir := if os_family() == "windows" { "./.venv/Scripts" } else { "./.venv/bin" }
python := python_dir + if os_family() == "windows" { "/python.exe" } else { "/python3" }
system_python := if os_family() == "windows" { "py.exe -3.10" } else { "python3.10" }

run-main:
    {{ python }} -m app.main
