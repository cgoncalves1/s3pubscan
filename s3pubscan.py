import requests
import argparse
import xml.etree.ElementTree as ET

def loadXML(url):
    response = requests.get(url, verify=args.insecure)
    xml = response.content
    return xml

def parseXML(xml):
    root = ET.fromstring(xml)
    ns = '{http://s3.amazonaws.com/doc/2006-03-01/}'
    result = []

    for item in root.iter('%sContents' % ns):
        result.append(item.find('%sKey' % ns).text)

    return(result, root.find('%sIsTruncated' % ns).text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scan for files in public S3 buckets.')
    parser.add_argument('URL', metavar='url', type=str, help='S3 url')
    parser.add_argument('-i',
                        '--insecure',
                        action='store_false',
                        help='ignore certificate errors')
    args = parser.parse_args()
    url = urldown = args.URL

    items = []
    truncated = "true"
    while(truncated == "true"):
        if(len(items) > 0):
            urldown = url + "?marker=" + items[-1]

        print("Recuperando URL ", urldown)
        result, truncated = parseXML(loadXML(urldown))
        items = items + result
        print("Itens identificados: ", len(result), " | TOTAL: ", len(items))

        f=open('result.txt', 'a')
        for l in items:
            f.write(url + l + '\n')

        f.close()
