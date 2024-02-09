import re 

with open("test17.txt") as f:
    text = f.read()

# print(text)

styles = list(set(re.findall(r"\{.*\}\n(\{.*\})\n\{.*\}", text)))
# print(len(styles))


styles.sort()

style_important = []
for s in styles:
    s_split = re.split(r"(-|_)", re.findall(r"font-family: (.*)\;", s)[0])

    if len(s_split) > 1:
        style_important.append(s_split[0])
    else:
        style_important.append(s_split[0])

style_important = list(set(style_important))

# print(len(style_important))

all_to_check = []
for style in style_important:
    check = re.findall("(\{.*\})\n(\{.*"+re.escape(style)+".*\})\n(\{.*\})", text)

    interest = []
    for c in check:
        if style in c[0] or style in c[2]:
            pass
        else:
            interest.append(c)
            all_to_check.append(c)
    # print(len(check))
    # print(len(interest))
    # print()


# print(len(all_to_check))

def extract_font_size(style):
    try:
        return re.search(r"font-size:(\d*)px", style).group(0)
    except AttributeError:
        return "font-size:-1px"

for a in all_to_check:
    if extract_font_size(a[0]) == extract_font_size(a[1]) or extract_font_size(a[1]) == extract_font_size(a[2]):
        print(a[0])
        print(a[1])
        print(a[2])
        print()

