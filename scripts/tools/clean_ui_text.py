with open("candidate-portal.html", "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace('placeholder="Search from 200+ roles (e.g. AI Systems Architect, Full Stack Engineer, SRE...)"', 'placeholder="Search target role (e.g. AI Systems Architect, Full Stack Engineer, SRE...)"')
html = html.replace('Specify your background and search from 200+ specialized career tracks.', 'Specify your background and select your target career track.')
html = html.replace('(200+ Roles Searchable)', '')
html = html.replace('(200+ Roles)', '')
html = html.replace('<!-- Search Dropdown with 200+ Roles Categorized -->', '<!-- Search Dropdown with Role Categories -->')

with open("candidate-portal.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Cleaned up all 200+ mentions from UI text!")
