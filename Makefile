D ?= podman

ENV_FILE=.env

.PHONY: init up down logs

init:
	@if [ ! -f $(ENV_FILE) ]; then \
		echo "🔑 Generando Fernet Key..."; \
		FERNET_KEY=$$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"); \
		echo "FERNET_KEY=$$FERNET_KEY" > $(ENV_FILE); \
		echo "✅ Archivo .env creado con Fernet Key"; \
	else \
		echo "⚠️  Ya existe un archivo .env, no se sobrescribe."; \
	fi

up:
	$(D) compose --env-file $(ENV_FILE) up -d

down:
	$(D) compose down --remove-orphans -v
