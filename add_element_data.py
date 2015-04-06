from app import db, models
import re

def getTrivia(trivia):
    pattern = re.compile(r'@@(.+?)##', flags=re.DOTALL)
    result = pattern.findall(trivia)
    return result



def main():
    for i in range(1, 119):
        e = models.Element.query.get(i)
        symbol = e.symbol
        desc = open("element_info/general_info/%s%s" % (symbol, ".txt"))
        trivia = open("element_info/trivia/%s%s" % (symbol, ".txt"))
        desc_text = desc.readlines()
        trivia_text = trivia.readlines()
        e.description = desc_text
        trivia_list = getTrivia(trivia_text)
        db.session.add(e)
        db.commit()
        print("Element: " + str(i) + " has " + str(len(trivia_list)) + " snippets of trivia.")
        for trivia_snippet in trivia_list:
            t = models.Trivia(description=trivia_snippet, element_number=i)
            db.session.add(t)
            db.commit()



if __name__ == "__main__":
    main()
