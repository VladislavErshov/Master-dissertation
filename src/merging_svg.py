from svglib.svglib import svg2rlg
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.renderSVG import SVGCanvas, draw

folder_path = "./result/Meso/img/img"
svg_1 = svg2rlg(f"{folder_path}_1.svg")
svg_2 = svg2rlg(f"{folder_path}_28.svg")
svg_3 = svg2rlg(f"{folder_path}_42.svg")
svg_4 = svg2rlg(f"{folder_path}_56.svg")
svg_5 = svg2rlg(f"{folder_path}_102.svg")
svg_6 = svg2rlg(f"{folder_path}_153.svg")
# svg_1 = svg2rlg("./result/Configurations/img_1.svg")
# svg_2 = svg2rlg("./result/Configurations/img_2.svg")
# svg_3 = svg2rlg("./result/Configurations/img_3.svg")
# svg_4 = svg2rlg("./result/Configurations/img_4.svg")
# svg_5 = svg2rlg("./result/Configurations/img_5.svg")
# svg_6 = svg2rlg("./result/Configurations/img_6.svg")

width = 3 * svg_1.width
height = 2 * svg_1.height
d = Drawing(width, height)

svg_1.scale(1, 1)
svg_2.scale(1, 1)
svg_3.scale(1, 1)
svg_4.scale(1, 1)
svg_5.scale(1, 1)
svg_6.scale(1, 1)

svg_1.translate(0, svg_1.height)
svg_2.translate(svg_1.width, svg_1.height)
svg_3.translate(2 * svg_1.width, svg_1.height)
svg_4.translate(0, 0)
svg_5.translate(svg_1.width, 0)
svg_6.translate(2 * svg_1.width, 0)

d.add(svg_1)
d.add(svg_2)
d.add(svg_3)
d.add(svg_4)
d.add(svg_5)
d.add(svg_6)

c = SVGCanvas((d.width, d.height))
draw(d, c, 0, 0)
c.save("./result/merging_svg.svg")
