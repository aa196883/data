# ------ Init
MUSYPHER_REPO_ADDR := https://gitlab.inria.fr/skrid/data-ingestion.git
MUSYPHER_DIR := Musypher

DB_FOLDERS := $(filter-out $(MUSYPHER_DIR)/ venv/,${wildcard */})
ALL_CQL := ${DB_FOLDERS:%/=%/load_DB.cql}

MEI_DIR := mei
CYPHER_DIR := cypher

REQUIRED_TOOLS := git pip python sed realpath

# ------ Tool checks
.PHONY: check-tools
check-tools:
	@for tool in $(REQUIRED_TOOLS); do \
		command -v $$tool >/dev/null 2>&1 || { \
			echo "Missing required tool: $$tool"; \
			exit 1; \
		}; \
	done

# ------ Rules
.PHONY: all
all: load_all_DB.cql

# --- Get Musypher from repo
$(MUSYPHER_DIR): check-tools
	git clone $(MUSYPHER_REPO_ADDR) $@
	cd $@ && pip install -r requirements.txt

# --- Run the makefile in each folder to generate the makefile,
# --- and make the cypher dumps with Musypher
%/load_DB.cql: $(MUSYPHER_DIR) check-tools
	@echo "Creating files for collection $* ..."
	cd "$*" && make
	@echo "======================================="
	@echo "Converting the MEI files to cypher dump"
	@echo "======================================="
	@python $(MUSYPHER_DIR)/main.py -nv -o $*/$(CYPHER_DIR)/ -q $@ $*/$(MEI_DIR)/*.mei

# --- Aggregate all cql files in another cql file.
load_all_DB.cql: $(ALL_CQL) | check-tools
	@echo "Generating file $@."
	@echo "CALL apoc.cypher.runFiles([" > $@
	@for k in $^; do \
		echo "'$$(realpath $$k)', " >> $@; \
	done
	@sed '$$ s/, $$//' $@ > tmp
	@rm $@
	@mv tmp $@
	@echo "], {statistics: false});" >> $@

# --- Clean
.PHONY: clean
clean:
	@echo "Cleaning."
	@rm -f load_all_DB.cql
	@for collection in $(DB_FOLDERS); do \
		cd "$$collection" && make clean && cd ..; \
	done
