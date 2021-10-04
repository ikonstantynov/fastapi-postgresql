DATABASE=db

ifndef ALEMBIC_CONFIG
ALEMBIC_CONFIG := "./configs/alembic.ini"
endif

start: ## Start services
	@printf "\n=> Startings containers\n\n"
	@docker-compose up -d $(DATABASE)
	@docker-compose up

stop: ## Stop services
	@printf "\n=> Stopping containers\n\n"
	@docker-compose stop

clean:
	@printf "\n=> Removing containers and images\n\n"
	@docker-compose down --remove-orphans
	@docker-compose rm --stop --force -v $(DATABASE)
	@docker image prune -af

autorevision:
	@printf "\n=> Generating revision\n\n"
	@alembic -c $(ALEMBIC_CONFIG) revision --autogenerate
	@alembic upgrade head
	@printf "\n=> Finished generating revision"
