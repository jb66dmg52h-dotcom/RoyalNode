KICAD_CLI ?= /Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
PROJECT_DIR := hardware/kicad/RoyalNode
SCH := $(PROJECT_DIR)/RoyalNode.kicad_sch
PCB := $(PROJECT_DIR)/RoyalNode.kicad_pcb
FAB_DIR := hardware/fabrication

.PHONY: validate generate-capture generate-placement generate-routes erc drc check-reports summarize-unrouted export-draft-quote kicad-checks full-check layout-status status

generate-capture:
	python3 tools/generate_kicad_capture.py

generate-placement:
	python3 tools/generate_pcb_placement.py

generate-routes:
	python3 tools/generate_initial_routes.py

validate:
	python3 tools/validate_royalnode.py

erc:
	$(KICAD_CLI) sch erc --output $(FAB_DIR)/RoyalNode_erc.rpt $(SCH)

drc:
	$(KICAD_CLI) pcb drc --refill-zones --save-board --output $(FAB_DIR)/RoyalNode_drc.rpt $(PCB)

check-reports:
	python3 tools/check_kicad_reports.py

summarize-unrouted:
	python3 tools/summarize_unrouted.py

export-draft-quote:
	python3 tools/export_draft_quote_package.py

kicad-checks: erc drc

full-check: validate erc drc check-reports

layout-status: full-check summarize-unrouted

status:
	git status --short --branch
