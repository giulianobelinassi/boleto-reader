# Instale o pyinstaller com:
# $ pip3 install pyinstaller
#
PYINSTALLER_PATH=$(HOME)/.local/bin/pyinstaller

binary:
	$(PYINSTALLER_PATH) --onefile --noconsole boleto-reader.py

clean:
	rm -rf build __pycache__ dist boleto-reader.spec
