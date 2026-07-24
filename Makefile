KICAD_CLI ?= /Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
PROJECT_DIR := hardware/kicad/RoyalNode
SCH := $(PROJECT_DIR)/RoyalNode.kicad_sch
PCB := $(PROJECT_DIR)/RoyalNode.kicad_pcb
FAB_DIR := hardware/fabrication

.PHONY: validate erc drc kicad-checks status

validate:
	python3 tools/validate_royalnode.py

erc:
	$(KICAD_CLI) sch erc --output $(FAB_DIR)/RoyalNode_erc.rpt $(SCH)

drc:
	$(KICAD_CLI) pcb drc --output $(FAB_DIR)/RoyalNode_drc.rpt $(PCB)

kicad-checks: erc drc

status:
	git status --short --branch

