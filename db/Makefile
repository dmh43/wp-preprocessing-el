include ../.env
VER=$(shell git rev-parse HEAD)

up:
	@echo ''
	@echo '-------------------'
	@echo '-- Creating database `$(EL_DBNAME)` --'
	@echo '-------------------'
	@echo ''
	mysql -u"$(DBUSER)" --host "$(DBHOST)" -e "CREATE DATABASE IF NOT EXISTS $(EL_DBNAME)"

	@echo ''
	@echo '-------------------'
	@echo '-- Creating tables --'
	@echo '-------------------'
	@echo ''
	mysql -u"$(DBUSER)" --host "$(DBHOST)" "$(EL_DBNAME)" < create_tables.sql

	@echo ''
	@echo '-------------------'
	@echo '-- Creating views --'
	@echo '-------------------'
	@echo ''
	mysql -u"$(DBUSER)" --host "$(DBHOST)" "$(EL_DBNAME)" < create_views.sql

	@echo ''
	@echo '-------------------'
	@echo '-- Recording script version --'
	@echo '-------------------'
	@echo ''
	mysql -u"$(DBUSER)" --host "$(DBHOST)" "$(EL_DBNAME)" -e "drop table if exists info"
	mysql -u"$(DBUSER)" --host "$(DBHOST)" "$(EL_DBNAME)" -e "create table if not exists info (version varchar(255))"
	mysql -u"$(DBUSER)" --host "$(DBHOST)" "$(EL_DBNAME)" -e "insert into info values ('$(VER)')"

down:
	@echo ''
	@echo '-------------------'
	@echo '-- Dropping tables --'
	@echo '-------------------'
	@echo ''
	mysql -u"$(DBUSER)" --host "$(DBHOST)" "$(EL_DBNAME)" < drop_tables.sql

	@echo ''
	@echo '-------------------'
	@echo '-- Dropping views --'
	@echo '-------------------'
	@echo ''
	mysql -u"$(DBUSER)" --host "$(DBHOST)" "$(EL_DBNAME)" < drop_views.sql

.PHONY: help el
