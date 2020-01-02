from pathlib import Path

pi_text = (Path(__file__).parent / "pi.txt").read_text()

cantarell = installFont("/tmp/Cantarell-VF.otf")

paper_format = "A4Landscape"
border = 25
gutter = border * 0.5
pageWidth, pageHeight = sizes(paper_format)
boxWidth = pageWidth - border * 2
boxHeight = pageHeight - border * 2

for wght in (100, 400, 800):
    newPage(paper_format)
    font(cantarell)
    fontVariations(wght=wght)
    if wght == 400:
        fontSize(12)
    else:
        fontSize(18)
    textBox(pi_text, (border, border, boxWidth, boxHeight))
