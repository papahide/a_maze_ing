# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: clalfons <clalfons@student.42madrid.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/05/20 16:29:17 by clalfons          #+#    #+#              #
#    Updated: 2026/05/20 16:29:23 by clalfons         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

PYTHON = python3
MAIN   = a_maze_ing.py
CONFIG = configuration.txt

OS := $(shell uname -s)
ifeq ($(OS), Linux)
    DISTRO := $(shell . /etc/os-release && echo $$ID)
else
    DISTRO := unknown
endif

.PHONY: install run debug lint lint-strict clean

install:
	@echo "Installing dependencies..."
ifeq ($(DISTRO), fedora)
	$(PYTHON) -m pip install mlx-2_2-py3-fedora-any.whl
else
	$(PYTHON) -m pip install mlx-2_2-py3-ubuntu-any.whl
endif
	@echo "Done."

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores \
	       --ignore-missing-imports \
	       --disallow-untyped-defs \
	       --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -name "*.pyc" -delete
	@echo "Cleaned."