.PHONY: bootstrap dev test build smoke deploy rollback clean

bootstrap:
	bash scripts/bootstrap.sh

dev:
	bash scripts/dev.sh

test:
	bash scripts/test.sh

build:
	bash scripts/build.sh

smoke:
	bash scripts/smoke_test.sh

deploy:
	bash scripts/deploy_cloud_run.sh

rollback:
	bash scripts/rollback_cloud_run.sh

clean:
	rm -rf __pycache__ .pytest_cache .coverage coverage.xml htmlcov /tmp/styleai
