cats = open('/srv/www/hntagged/hn/fixtures/cats.txt', 'r').read()
cats = cats.split('\n')
cats.sort()
cats = [cat for cat in cats if cat]
f=open('/srv/www/hntagged/hn/fixtures/initial_data.json', 'w')
f.write('[\n')
last = len(cats)-1
for i, cat in enumerate(cats):
    f.write('    {\n')
    f.write('        "model": "hn.category",\n')
    f.write('        "pk":%s,\n' % i)
    f.write('        "fields": {\n')
    f.write('            "name": "%s" \n' % cat)
    f.write('        }\n')
    if last == i:
        f.write('    }')
    else:
        f.write('    },\n')

   
f.write(']')
f.close()
