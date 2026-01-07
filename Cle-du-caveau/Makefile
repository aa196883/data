# ------ Init
# - Name of the collection folder
COLLECTION := Clef-du-caveau

# - Directories
MEI_DIR := mei
MSCZ_DIR := mscz
MID_DIR := mid
LY_DIR := ly
SVG_DIR := svg
PDF_DIR := pdf
ARCHIVES_DIR := archives
CYPHER_DIR := cypher

DIRS := $(MEI_DIR) $(MSCZ_DIR) $(MID_DIR) $(LY_DIR) $(SVG_DIR) $(PDF_DIR) \
	$(ARCHIVES_DIR) $(CYPHER_DIR)

# - Sources
SOURCES := $(wildcard $(MEI_DIR)/*.mei)
MEI_OBJECTS := $(SOURCES)
MSCZ_OBJECTS := $(patsubst $(MEI_DIR)/%.mei, $(MSCZ_DIR)/%.mscz, $(SOURCES))
MID_OBJECTS := $(patsubst $(MEI_DIR)/%.mei, $(MID_DIR)/%.mid, $(SOURCES))
LY_OBJECTS := $(patsubst $(MEI_DIR)/%.mei, $(LY_DIR)/%.ly, $(SOURCES))
SVG_OBJECTS := $(patsubst $(MEI_DIR)/%.mei, $(SVG_DIR)/%.svg, $(SOURCES))
PDF_OBJECTS := $(patsubst $(MEI_DIR)/%.mei, $(PDF_DIR)/%.pdf, $(SOURCES))

ARCHIVES := $(ARCHIVES_DIR)/$(COLLECTION)_FilesAll.zip \
	$(ARCHIVES_DIR)/$(COLLECTION)_FilesSvg.zip \
	$(ARCHIVES_DIR)/$(COLLECTION)_FilesMei.zip \
	$(ARCHIVES_DIR)/$(COLLECTION)_FilesMid.zip \
	$(ARCHIVES_DIR)/$(COLLECTION)_FilesPdf.zip
# $(ARCHIVES_DIR)/$(COLLECTION)_FilesLy.zip

# ------ Helpers

define ensure-dir
	@echo "Creating folder \"$@\""
	@mkdir -p $@
	@echo "*" > $@/.gitignore
endef

# ------ Tool checks
.PHONY: check-tools check-verovio check-mscore check-rsvg-convert check-zip

check-tools: check-verovio check-mscore check-rsvg-convert check-zip

check-verovio:
	@command -v verovio >/dev/null 2>&1 || { echo "Missing required tool: verovio"; exit 1; }

check-mscore:
	@command -v mscore >/dev/null 2>&1 || { echo "Missing required tool: mscore"; exit 1; }

check-rsvg-convert:
	@command -v rsvg-convert >/dev/null 2>&1 || { echo "Missing required tool: rsvg-convert"; exit 1; }

check-zip:
	@command -v zip >/dev/null 2>&1 || { echo "Missing required tool: zip"; exit 1; }

# ------ Rules
.PHONY: all
# all: $(DIRS) mid-obj svg-obj mscz-obj pdf-obj ly-obj archives-obj $(CYPHER_DIR)
all: $(DIRS) mid-obj svg-obj mscz-obj pdf-obj $(CYPHER_DIR)

# TODO: support the ly files

# --- MIDI
$(MID_DIR):
	$(ensure-dir)

.PHONY: mid-obj
mid-obj: $(MID_DIR) $(MID_OBJECTS)
	@echo "======================="
	@echo "Converted to MIDI files"
	@echo "======================="

$(MID_DIR)/%.mid: $(MEI_DIR)/%.mei | check-verovio
	@verovio $^ -t midi -o $@

# --- SVG
$(SVG_DIR):
	$(ensure-dir)

.PHONY: svg-obj
svg-obj: $(SVG_DIR) $(SVG_OBJECTS)
	@echo "======================"
	@echo "Converted to SVG files"
	@echo "======================"

$(SVG_DIR)/%.svg: $(MEI_DIR)/%.mei | check-verovio
	@verovio $^ -t svg -o $@

# --- MSCZ
$(MSCZ_DIR):
	$(ensure-dir)

.PHONY: mscz-obj
mscz-obj: $(MSCZ_DIR) $(MSCZ_OBJECTS)
	@echo "======================="
	@echo "Converted to MSCZ files"
	@echo "======================="

$(MSCZ_DIR)/%.mscz: $(MEI_DIR)/%.mei | check-mscore
	mscore $^ -o $@ || echo "Error while converting $^ to $@"

# --- PDF
$(PDF_DIR):
	$(ensure-dir)

.PHONY: pdf-obj
pdf-obj: $(PDF_DIR) $(PDF_OBJECTS)
	@echo "======================"
	@echo "Converted to PDF files"
	@echo "======================"

# Conversion SVG -> PDF avec rsvg-convert
$(PDF_DIR)/%.pdf: $(SVG_DIR)/%.svg | check-rsvg-convert
	@echo "Converting $< to $@"
	@rsvg-convert -f pdf -o "$@" "$<"

# --- Ly
$(LY_DIR):
	$(ensure-dir)

.PHONY: ly-obj
ly-obj: $(LY_DIR) $(LY_OBJECTS)
	@echo "==========================="
	@echo "Converted to Lilypond files"
	@echo "==========================="

$(LY_DIR)/%.ly: $(MEI_DIR)/%.mei | check-verovio
	@verovio $^ -t ly -o $@

# --- Archives
$(ARCHIVES_DIR):
	$(ensure-dir)

.PHONY: archives-obj
archives-obj: $(ARCHIVES_DIR) $(ARCHIVES)
	@echo "================="
	@echo "Archives created."
	@echo "================="

$(ARCHIVES_DIR)/$(COLLECTION)_FilesAll.zip: $(MSCZ_OBJECTS) $(MEI_OBJECTS) $(SVG_OBJECTS) $(PDF_OBJECTS) $(MID_OBJECTS) | check-zip
	@echo "All ..."
	@zip -9 -y -r -q $@ $^

$(ARCHIVES_DIR)/$(COLLECTION)_FilesSvg.zip: $(SVG_OBJECTS) | check-zip
	@echo "SVG ..."
	@zip -9 -y -r -q $@ $^

$(ARCHIVES_DIR)/$(COLLECTION)_FilesMei.zip: $(MEI_OBJECTS) | check-zip
	@echo "MEI ..."
	@zip -9 -y -r -q $@ $^

$(ARCHIVES_DIR)/$(COLLECTION)_FilesLy.zip: $(LY_OBJECTS) | check-zip
	@echo "Lilypond ..."
	@zip -9 -y -r -q $@ $^

$(ARCHIVES_DIR)/$(COLLECTION)_FilesMid.zip: $(MID_OBJECTS) | check-zip
	@echo "midi ..."
	@zip -9 -y -r -q $@ $^

$(ARCHIVES_DIR)/$(COLLECTION)_FilesPdf.zip: $(PDF_OBJECTS) | check-zip
	@echo "pdf ..."
	@zip -9 -y -r -q $@ $^

# --- Cypher dir
$(CYPHER_DIR):
	$(ensure-dir)

# --- Clean
.PHONY: clean
clean:
	@echo "======================="
	@echo "Cleaning $(COLLECTION)"
	@echo "======================="
	@rm -rf $(CYPHER_DIR)/*.cypher
	@rm -rf $(PDF_OBJECTS)
	@rm -rf $(SVG_OBJECTS)
	@rm -rf $(MSCZ_OBJECTS)
	@rm -rf $(LY_OBJECTS)
	@rm -rf $(MID_OBJECTS)
	@rm -rf $(ARCHIVES_DIR)/*.zip
	@rm -rf load_DB.cql
