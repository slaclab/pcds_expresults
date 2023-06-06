MONGOREADER_SECRET_PATH ?= secret/lcls/psdm/psdm-mongoreader

secrets:
	mkdir -p etc/.secrets/
	for i in username password hosts; do vault kv get -format=table --field=$$i $(MONGOREADER_SECRET_PATH) > etc/.secrets/$$i; done

clean-secrets:
	rm -rf etc/

run-apply:
	kubectl apply -k .

apply: secrets run-apply clean-secrets

run-delete:
	kubectl delete -k .

delete: secrets run-delete clean-secrets

run-dump:
	kubectl kustomize .

dump: secrets run-dump clean-secrets