SHELL := /bin/bash

DEFAULT_MODE := git
MODE ?= $(DEFAULT_MODE)

.DEFAULT_GOAL := help

sync:
	@echo "🔄 Running sync_git_deps.py with mode: $(MODE)"
	python3 sync_git_deps.py --mode "$(MODE)"

sync-dry-run:
	@echo "🔍 Dry-run sync for validation (mode: $(MODE))"
	python3 sync_git_deps.py --mode "$(MODE)" --dry-run

install-hooks:
	@echo "Installing git hooks..."
	@cp -f git-hooks/* .git/hooks/
	@chmod +x .git/hooks/*
	@echo "Git hooks installed!"

help:
	@echo ""
	@echo "Targets:"
	@echo "  make sync MODE=<git|local>      → sync git deps (default: git)"
	@echo "  make sync-dry-run MODE=<git|local> → validate deps without changing files"
	@echo "  install-hooks → install git hooks"
	@echo ""
