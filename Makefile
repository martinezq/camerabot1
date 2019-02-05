HOST=raspberrypi.local
USER=pi
PASSWORD=raspberry
PROJECT=camerabot1

# If the first argument is "run"...
ifeq (run,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

ssh:
	sshpass -p $(PASSWORD) ssh -o StrictHostKeyChecking=no $(USER)@$(HOST)

upload:
	sshpass -p $(PASSWORD) scp -o StrictHostKeyChecking=no -rp src/* $(USER)@$(HOST):~/projects/$(PROJECT)

download:
	sshpass -p $(PASSWORD) scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -rp $(USER)@$(HOST):~/projects/$(PROJECT)/* src/

run: upload
	sshpass -p $(PASSWORD) ssh -t -Y -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $(USER)@$(HOST) 'python ~/projects/$(PROJECT)/track1.py -d 1'

run-nd: upload
	sshpass -p $(PASSWORD) ssh -t -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $(USER)@$(HOST) 'python ~/projects/$(PROJECT)/track1.py -d 0'	