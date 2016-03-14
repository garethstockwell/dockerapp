# Makefile

first: default

path_makefile = $(lastword $(MAKEFILE_LIST))
path_top = $(abspath $(dir $(call path_makefile)))

dockerapp = $(call path_top)/bin/dockerapp

APPS :=

app_config = \
	$(call path_top)/apps/$1/Dockerfile \
	$(call path_top)/apps/$1/app.yaml

define app_add
$(eval \
APPS += $1

$1-build: $(call app_config,$1)
	$(call dockerapp) build $1

.PHONY: $1-build
)
endef

$(foreach app,$(patsubst apps/%,%,$(wildcard apps/*)),$(call app_add,$(app)))

default: build

build: $(foreach app,$(APPS),$(app)-build)

.PHONY: \
	build \

