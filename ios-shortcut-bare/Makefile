.PHONY: all clean build compile install help

CHERRI := cherri
BUILD_DIR := build
OUTPUT_DIR := output

all: compile

help:
	@echo "iOS Shortcuts Build System"
	@echo ""
	@echo "Usage:"
	@echo "  make          - Build and compile all shortcuts"
	@echo "  make build    - Generate .cherri files from templates"
	@echo "  make compile  - Compile .cherri to .shortcut files"
	@echo "  make install  - Open output folder (for AirDrop)"
	@echo "  make clean    - Remove generated files"
	@echo ""
	@echo "Workflow:"
	@echo "  1. Edit config.json with your API settings"
	@echo "  2. Run 'make'"
	@echo "  3. Run 'make install' and AirDrop to your device"

# Generate .cherri files from templates
build:
	@mkdir -p $(BUILD_DIR)
	@python3 build.py

# Compile all .cherri files to .shortcut
compile: build
	@mkdir -p $(OUTPUT_DIR)
	@for f in $(BUILD_DIR)/*.cherri; do \
		if [ -f "$$f" ]; then \
			name=$$(basename "$$f" .cherri); \
			echo "Compiling: $$name"; \
			$(CHERRI) "$$f" -o="$(OUTPUT_DIR)/$$name.shortcut" || exit 1; \
		fi \
	done
	@echo ""
	@echo "Shortcuts ready in $(OUTPUT_DIR)/"

# Open output folder for AirDrop
install: compile
	@open $(OUTPUT_DIR)

clean:
	rm -rf $(BUILD_DIR) $(OUTPUT_DIR)
	@echo "Cleaned build and output directories"
