import urllib.request

with open('./imgUrls.txt', 'r') as uf:
    urls = uf.readlines()
    num = 0
    for url in urls:
        num += 1
        response = urllib.request.urlopen(url)
        pic = response.read()

        with open('./img/' + str(num) + '.JPG', 'wb') as f:
            f.write(pic)