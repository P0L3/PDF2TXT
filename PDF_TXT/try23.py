import re
test = "font-size:[789]px"

sizes = list(set(re.findall(r"font-size:\[*(\d+)\]*px", test)))
extra_fonts = ["fb", "20"]

if len(sizes) == 1:
    if len(sizes[0]) > 2:
        sizes = [s for s in sizes[0]]
print(sizes)


for s in sizes:
    for font in extra_fonts:
        print(f"font-family: {font}; font-size:{s}px")

