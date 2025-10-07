D ?= podman

up:
	$(D) compose up 

down:
	$(D) compose down --remove-orphans -v
