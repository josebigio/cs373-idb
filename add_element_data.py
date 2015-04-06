from app import db, models
import re

def getTrivia(trivia):
    pattern = re.compile(r'@@(.+?)##', flags=re.DOTALL)
    result = pattern.findall(trivia)
    return result



def main():
    curdir = "/home/elementalists/cs373-idb/"
    for i in range(1, 119):
        e = models.Element.query.get(i)
        symbol = e.symbol
        try:
            desc = open(curdir + "elements_info/general_info/%s%s" % (symbol.strip(), ".*"))
        except IOError as e:
            print("Missing descrption on element: " + symbol)
            print(e)
        else:
            desc_text = desc.read()
            e.description = desc_text
            db.session.add(e)
            db.session.commit()
        try:
            trivia = open(curdir + "elements_info/trivia/%s%s" % (symbol.strip(), ".*"))
        except IOError as e:
            print("Missing trivia for element: " + symbol)
            print(e)
        finally:
            trivia_text = trivia.read()
            if trivia_text is not None and trivia_text != "":
                trivia_list = getTrivia(trivia_text)
                for trivia_snippet in trivia_list:
                    t = models.Trivia(description=trivia_snippet, element_number=i)
                    db.session.add(t)
                    db.session.commit()



if __name__ == "__main__":
    main()
