
TARGETS = \
	tmp/Pomax/nihongoresources.com/giongo.txt \
	tmp/ku21fan/COO-Comic-Onomatopoeia/COO-data/M4C_feature/Onomatopoeia_train_vocab_set.txt \
	tmp/nsk.sh/tools/jp-onomatopoeia/onomatopoeia.jsonnl \
	tmp/surasura/term_bank_1.jsonnl

all: $(TARGETS)

tmp/Pomax/nihongoresources.com/giongo.txt:
	mkdir -p $(dir $@)
	wget -O $@ https://raw.githubusercontent.com/Pomax/nihongoresources.com/master/giongo.txt

tmp/ku21fan/COO-Comic-Onomatopoeia/COO-data/M4C_feature/Onomatopoeia_train_vocab_set.txt:
	mkdir -p $(dir $@)
	wget -O $@ https://github.com/ku21fan/COO-Comic-Onomatopoeia/raw/main/COO-data/M4C_feature/Onomatopoeia_train_vocab_set.txt

tmp/nsk.sh/tools/jp-onomatopoeia/onomatopoeia.json:
	mkdir -p $(dir $@)
	wget -O $@ https://nsk.sh/tools/jp-onomatopoeia/onomatopoeia.json

tmp/nsk.sh/tools/jp-onomatopoeia/onomatopoeia.jsonnl: tmp/nsk.sh/tools/jp-onomatopoeia/onomatopoeia.json
	cat tmp/nsk.sh/tools/jp-onomatopoeia/onomatopoeia.json | jq -c '. | to_entries[]' > $@

tmp/MarvNC/yomichan-dictionaries/surasura.zip:
	mkdir -p $(dir $@)
	wget -O $@ https://github.com/MarvNC/yomichan-dictionaries/raw/master/dl/%5BMonolingual%5D%20surasura.zip

tmp/surasura/term_bank_1.json: tmp/MarvNC/yomichan-dictionaries/surasura.zip
	mkdir -p $(dir $@)
	unzip -d $(dir $@) tmp/MarvNC/yomichan-dictionaries/surasura.zip

tmp/surasura/term_bank_1.jsonnl: tmp/surasura/term_bank_1.json
	cat tmp/surasura/term_bank_1.json | jq -c '.[] | {key: .[0],  value: .[5][0]["content"][0]["content"]}' > $@