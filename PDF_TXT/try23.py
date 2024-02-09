import re
test = "(font-family: AdvOT46dcae81; font-size:8px|font-family: fb; font-size:8px)"

sizes = list(set(re.findall(r"font-size:(\d+)px", test)))
extra_fonts = ["fb", "20"]

print(sizes)

for s in sizes:
    for font in extra_fonts:
        print(f"font-family: {font}; font-size:{s}px")

