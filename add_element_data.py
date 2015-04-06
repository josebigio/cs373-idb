from app import db, models
import re, os

def getTrivia(trivia):
    pattern = re.compile(r'@@(.+?)##', flags=re.DOTALL)
    result = pattern.findall(trivia)
    return result


def stripWikiCitations(str):
    pattern = re.compile(r'\[(.)\]')
    return re.sub(pattern, str, '')



def main():
    curdir = "/home/elementalists/cs373-idb/"
    generalinfo = "elements_info/general_info/"
    for i in range(1, 119):
        e = models.Element.query.get(i)
        symbol = e.symbol
        try:
            desc_file = ''
            for filename in os.listdir(curdir + generalinfo):
                if filename.startswith(symbol):
                    desc_file = filename
            if desc_file == '':
                desc = open(curdir + "elements_info/general_info/%s%s" % (symbol.strip(), ".txt"))
            else:
                desc = open(curdir + generalinfo + desc_file)
        except IOError as e:
            print("Missing descrption on element: " + symbol)
            print(e)
        else:
            desc_text = stripWikiCitations(desc.read())
            e.description = desc_text
            db.session.add(e)
            db.session.commit()
        try:
            triv_file = ''
            for filename in os.listdir(curdir + generalinfo):
                if filename.startswith(symbol):
                    triv_file = filename
            if desc_file == '':
                trivia = open(curdir + "elements_info/trivia/%s%s" % (symbol.strip(), ".txt"))
            else:
                trivia = open(curdir + generalinfo + triv_file)
        except IOError as e:
            print("Missing trivia for element: " + symbol)
            print(e)
        finally:
            trivia_text = stripWikiCitations(trivia.read())
            if trivia_text is not None and trivia_text != "":
                trivia_list = getTrivia(trivia_text)
                for trivia_snippet in trivia_list:
                    t = models.Trivia(description=trivia_snippet, element_number=i)
                    db.session.add(t)
                    db.session.commit()



if __name__ == "__main__":
    main()
